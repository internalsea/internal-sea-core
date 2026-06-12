from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class SystemInfo(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Infrastructure table used to validate migrations."""

    __tablename__ = "system_info"

    key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    value: Mapped[str | None] = mapped_column(String(1024), nullable=True)
