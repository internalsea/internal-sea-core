from functools import lru_cache
from pathlib import Path
from typing import Annotated, Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


def _settings_env_files() -> tuple[str, ...]:
    """Resolve .env paths for monorepo (apps/api) and Docker (/app) layouts."""
    here = Path(__file__).resolve()
    candidates: list[str] = []
    if len(here.parents) > 3:
        candidates.append(str(here.parents[3] / ".env"))
    candidates.append(str(here.parents[1] / ".env"))
    candidates.append(".env")
    return tuple(dict.fromkeys(candidates))


_ENV_FILES = _settings_env_files()

_PRODUCTION_LIKE_ENVS = frozenset({"production", "staging", "prod"})
_INSECURE_JWT_SECRETS = frozenset({"change_me_later", "changeme", "secret"})


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILES,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Internal Sea API"
    app_env: str = "local"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    # Comma-separated in .env / docker-compose; NoDecode skips pydantic-settings JSON parsing.
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:5173"]
    )

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "internal_sea_core"
    postgres_user: str = "internal_sea"
    postgres_password: str = "internal_sea"
    database_url: str = (
        "postgresql+asyncpg://internal_sea:internal_sea@localhost:5432/internal_sea_core"
    )
    database_pool_size: int | None = None
    database_max_overflow: int | None = None

    # Redis (optional — reserved for future workers/cache)
    redis_url: str | None = "redis://localhost:6379/0"

    # Auth
    jwt_secret_key: str = "change_me_later"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    auth_enabled: bool = True

    # Security
    secure_cookies: bool = False
    password_min_length: int = 8
    rate_limit_enabled: bool = False

    # Worker (optional background process)
    worker_enabled: bool = False
    worker_poll_interval_seconds: int = 30
    worker_batch_size: int = 10
    worker_instance_id: str | None = None
    worker_lock_timeout_seconds: int = 300

    # Automation worker execution
    automation_real_run_enabled: bool = True
    automation_default_simulate: bool = False

    # Notification worker delivery
    notification_external_delivery_enabled: bool = False
    notification_worker_simulate_external: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def is_production_like(self) -> bool:
        return self.app_env.lower() in _PRODUCTION_LIKE_ENVS

    @model_validator(mode="after")
    def validate_production_settings(self) -> Self:
        if not self.is_production_like:
            return self

        if self.jwt_secret_key.strip().lower() in _INSECURE_JWT_SECRETS:
            raise ValueError(
                "JWT_SECRET_KEY must be changed from the default value "
                "in production-like environments"
            )
        if self.debug:
            raise ValueError("DEBUG must be false in production-like environments")
        if "*" in self.cors_origins:
            raise ValueError(
                "CORS_ORIGINS must not include wildcard in production-like environments"
            )
        if not self.auth_enabled:
            raise ValueError("AUTH_ENABLED must be true in production-like environments")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
