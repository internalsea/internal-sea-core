from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.db.health import check_database_connection

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@router.get("/live")
def liveness_check() -> dict[str, str]:
    return {"status": "live"}


@router.get("/ready", response_model=None)
async def readiness_check() -> JSONResponse | dict[str, str]:
    if await check_database_connection():
        return {"status": "ready", "database": "connected"}
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "not_ready", "database": "unavailable"},
    )


@router.get("/db", response_model=None)
async def database_health_check() -> JSONResponse | dict[str, str]:
    if await check_database_connection():
        return {"status": "ok", "database": "connected"}
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "error", "database": "unavailable"},
    )
