"""Application configuration loaded from environment variables with safe local defaults."""

from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_prefix="SMARTKRISHI_",
        extra="ignore",
    )

    env: str = Field(default="development")
    database_url: str = Field(
        default=f"sqlite:///{(PROJECT_ROOT / 'backend' / 'data' / 'smartkrishi.db').as_posix()}"
    )
    cors_origins: str = Field(default="http://localhost:5173,http://127.0.0.1:5173")
    admin_username: str = Field(default="admin")
    admin_password: str = Field(default="smartkrishi-local-admin-2026")
    token_secret: str = Field(default="smartkrishi-local-dev-hmac-secret-change-in-prod")
    token_ttl_seconds: int = Field(default=60 * 60 * 8)
    model_dir: str = Field(default=str(PROJECT_ROOT / "ml" / "artifacts"))
    enable_live_weather: bool = Field(default=False)
    weather_timeout_seconds: float = Field(default=2.5)

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
