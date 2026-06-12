import logging
import sys

from app.config import Settings


class RequestIdFilter(logging.Filter):
    """Placeholder filter for future contextvar-based request ID injection."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True


def configure_logging(settings: Settings) -> None:
    """Configure application-wide logging."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | request_id=%(request_id)s | %(message)s",
        stream=sys.stdout,
        force=True,
    )
    request_filter = RequestIdFilter()
    for handler in logging.root.handlers:
        handler.addFilter(request_filter)

    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
