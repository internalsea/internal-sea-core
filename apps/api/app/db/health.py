import logging

from sqlalchemy import text

from app.db.session import get_engine

logger = logging.getLogger(__name__)


async def check_database_connection() -> bool:
    """Return True when the database accepts a simple query."""
    try:
        engine = get_engine()
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.exception("Database connection check failed")
        return False
