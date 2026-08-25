from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import httpx
from pydantic import BaseModel

from app.config import get_settings
from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/ai", tags=["ai"])


def _validate_base_url(base_url: str) -> None:
    """仅允许转发到服务端白名单内的 AI 服务，防止借代理探测内网（SSRF）"""
    parsed = urlparse(base_url.strip())
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="base_url 必须是 http(s) 地址",
        )
    host = (parsed.hostname or "").lower()
    allowed = {
        h.strip().lower()
        for h in get_settings().AI_ALLOWED_HOSTS.split(",")
        if h.strip()
    }
    if host not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"AI 服务地址 {host or '(空)'} 不在服务端允许列表，如需使用请在 .env 的 AI_ALLOWED_HOSTS 中追加",
        )


class FetchModelsRequest(BaseModel):
    base_url: str
    api_key: str


class ChatStreamRequest(BaseModel):
    base_url: str
    api_key: str
    model: str
    messages: list[dict[str, Any]]
    temperature: float = 0.7


def _build_url(base_url: str, endpoint: str) -> str:
    cleaned = base_url.strip().rstrip("/")
    if cleaned.endswith("/v1"):
        return f"{cleaned}/{endpoint.lstrip('/')}"
    if "/v1/" in cleaned:
        return f"{cleaned}/{endpoint.lstrip('/')}"
    return f"{cleaned}/v1/{endpoint.lstrip('/')}"


@router.post("/models")
async def fetch_models(payload: FetchModelsRequest, _user: User = Depends(get_current_user)):
    _validate_base_url(payload.base_url)
    target_url = _build_url(payload.base_url, "models")
    clean_key = payload.api_key.strip()

    headers = {
        "Authorization": f"Bearer {clean_key}",
        "x-api-key": clean_key,
        "api-key": clean_key,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=False) as client:
            resp = await client.get(target_url, headers=headers)
            
            # 如果 404，尝试不带 /v1 的直接路径
            if resp.status_code == 404 and "/v1/" in target_url:
                alt_url = target_url.replace("/v1/models", "/models")
                resp = await client.get(alt_url, headers=headers)

            if resp.status_code != 200:
                err_text = resp.text
                try:
                    err_json = resp.json()
                    err_text = err_json.get("message") or err_json.get("error") or str(err_json)
                except Exception:
                    pass
                raise HTTPException(
                    status_code=resp.status_code,
                    detail=f"中转站验证未通过 ({resp.status_code}): {err_text[:200]}",
                )

            return resp.json()
    except HTTPException:
        raise
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"连接中转站接口失败: {str(exc)}",
        )


@router.post("/chat")
async def chat_stream(payload: ChatStreamRequest, _user: User = Depends(get_current_user)):
    _validate_base_url(payload.base_url)
    target_url = _build_url(payload.base_url, "chat/completions")
    clean_key = payload.api_key.strip()

    headers = {
        "Authorization": f"Bearer {clean_key}",
        "x-api-key": clean_key,
        "api-key": clean_key,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    body = {
        "model": payload.model.strip(),
        "messages": payload.messages,
        "temperature": payload.temperature,
        "stream": True,
    }

    async def event_generator():
        try:
            async with httpx.AsyncClient(timeout=60.0, follow_redirects=False) as client:
                async with client.stream("POST", target_url, headers=headers, json=body) as resp:
                    if resp.status_code != 200:
                        err_bytes = await resp.aread()
                        err_msg = err_bytes.decode("utf-8", errors="ignore")
                        try:
                            parsed = json.loads(err_msg)
                            err_msg = parsed.get("message") or parsed.get("error") or err_msg
                        except Exception:
                            pass
                        yield f"data: {json.dumps({'error': str(err_msg)[:300]})}\n\n"
                        return

                    async for line in resp.aiter_lines():
                        if line:
                            yield f"{line}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
