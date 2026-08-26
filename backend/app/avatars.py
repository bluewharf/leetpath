from __future__ import annotations

import io
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from app.config import get_settings
from app.db import BACKEND_ROOT
from app.models import User

MAX_UPLOAD_BYTES = 1_500_000
AVATAR_SIZE = 256
ALLOWED_PREFIXES = (
    b"\xff\xd8\xff",  # jpeg
    b"\x89PNG\r\n\x1a\n",  # png
    b"GIF87a",
    b"GIF89a",
    b"RIFF",  # webp 还需检查 WEBP
)

Image.MAX_IMAGE_PIXELS = 8_000_000


def data_dir() -> Path:
    url = get_settings().DATABASE_URL
    if url.startswith("sqlite:///") and not url.startswith("sqlite:///:memory:"):
        rest = url[len("sqlite:///"):]
        path = Path(rest)
        if not path.is_absolute():
            path = BACKEND_ROOT / path
        return path.parent
    return BACKEND_ROOT / "data"


def avatars_dir() -> Path:
    path = data_dir() / "avatars"
    path.mkdir(parents=True, exist_ok=True)
    return path


def avatar_url(user: User) -> str | None:
    if not user.avatar_path:
        return None
    stamp = 0
    if user.avatar_updated_at is not None:
        stamp = int(user.avatar_updated_at.timestamp())
    return f"/api/auth/avatar/{user.id}?v={stamp}"


def _looks_like_image(data: bytes) -> bool:
    if data.startswith(b"RIFF") and b"WEBP" in data[:16]:
        return True
    return any(data.startswith(prefix) for prefix in ALLOWED_PREFIXES if prefix != b"RIFF")


def process_avatar(data: bytes) -> bytes:
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValueError("图片不能超过 1.5MB")
    if not _looks_like_image(data):
        raise ValueError("只支持 JPG / PNG / WebP / GIF 图片")
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            image = image.convert("RGBA")
            width, height = image.size
            side = min(width, height)
            left = (width - side) // 2
            top = (height - side) // 2
            image = image.crop((left, top, left + side, top + side))
            image = image.resize((AVATAR_SIZE, AVATAR_SIZE), Image.Resampling.LANCZOS)
            background = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), (31, 31, 35))
            background.paste(image, mask=image.split()[-1])
            output = io.BytesIO()
            background.save(output, format="WEBP", quality=82, method=4)
            return output.getvalue()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError("无法读取该图片，请换一张再试") from exc


def save_avatar(user_id: int, data: bytes) -> str:
    processed = process_avatar(data)
    relative = f"avatars/{user_id}.webp"
    path = avatars_dir() / f"{user_id}.webp"
    path.write_bytes(processed)
    return relative


def delete_avatar_file(relative: str | None) -> None:
    if not relative:
        return
    path = data_dir() / relative
    if path.is_file() and path.resolve().is_relative_to(avatars_dir().resolve()):
        path.unlink(missing_ok=True)


def absolute_avatar_path(relative: str) -> Path:
    return data_dir() / relative
