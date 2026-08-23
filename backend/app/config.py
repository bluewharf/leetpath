from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SECRET_KEY: str = "dev-secret-change-me"
    DATABASE_URL: str = "sqlite:///data/leetpath.db"
    TOKEN_TTL_DAYS: int = 7
    COOKIE_NAME: str = "leetpath_token"
    COOKIE_SECURE: bool = False


def get_settings() -> Settings:
    return Settings()
