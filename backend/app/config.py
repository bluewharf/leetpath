from typing import Literal
from urllib.parse import urlsplit

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: Literal["development", "test", "production"] = "development"
    # 部署版本号，由根目录 VERSION 文件经 compose 环境变量注入
    APP_VERSION: str = "dev"
    SECRET_KEY: str = "dev-secret-change-me"
    DATABASE_URL: str = "sqlite:///data/leetpath.db"
    TOKEN_TTL_DAYS: int = 7
    COOKIE_NAME: str = "leetpath_token"
    COOKIE_SECURE: bool = False
    PUBLIC_ORIGIN: str = "http://localhost:5173"
    # AI 助教代理允许转发的目标域名（逗号分隔），防止 SSRF
    AI_ALLOWED_HOSTS: str = "api.antithor.asia,api.deepseek.com"
    # 内测阶段服务端内置 AI 密钥（保存在 .env 中，绝不泄露给前端或 Git）
    SYSTEM_AI_API_KEY: str = ""
    SYSTEM_AI_BASE_URL: str = "https://api.antithor.asia/v1"
    SYSTEM_AI_MODEL: str = "grok-4.6-xhigh"

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.APP_ENV != "production":
            return self
        if self.SECRET_KEY == "dev-secret-change-me" or len(self.SECRET_KEY.encode("utf-8")) < 32:
            raise ValueError("生产环境 SECRET_KEY 必须是至少 32 字节的随机值")
        if not self.COOKIE_SECURE:
            raise ValueError("生产环境必须启用 COOKIE_SECURE")
        try:
            origin = urlsplit(self.PUBLIC_ORIGIN)
            _ = origin.port
        except ValueError as exc:
            raise ValueError("生产环境 PUBLIC_ORIGIN 必须是有效的 HTTPS origin") from exc
        if (
            origin.scheme != "https"
            or not origin.hostname
            or origin.username is not None
            or origin.password is not None
            or origin.path
            or origin.query
            or origin.fragment
        ):
            raise ValueError("生产环境 PUBLIC_ORIGIN 必须是有效的 HTTPS origin")
        return self


def get_settings() -> Settings:
    return Settings()
