import pytest
from pydantic import ValidationError

from app.config import Settings, get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_local_settings_allow_default_jwt_secret() -> None:
    settings = Settings(app_env="local", jwt_secret_key="change_me_later", debug=True)
    assert settings.is_production_like is False


def test_production_rejects_default_jwt_secret() -> None:
    with pytest.raises(ValidationError, match="JWT_SECRET_KEY"):
        Settings(app_env="production", jwt_secret_key="change_me_later", debug=False)


def test_production_rejects_debug_true() -> None:
    with pytest.raises(ValidationError, match="DEBUG"):
        Settings(
            app_env="production",
            jwt_secret_key="a-secure-production-secret-value",
            debug=True,
        )


def test_production_rejects_wildcard_cors() -> None:
    with pytest.raises(ValidationError, match="CORS"):
        Settings(
            app_env="production",
            jwt_secret_key="a-secure-production-secret-value",
            debug=False,
            cors_origins=["*"],
        )
