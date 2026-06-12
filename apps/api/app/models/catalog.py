from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin, WorkspaceScopedMixin
from app.domain.enums import DataProductStatus, DataProductType, QualityStatus

if TYPE_CHECKING:
    from app.models.people import Capability, Person, Team
    from app.models.work import Comment, WorkItem


class BusinessDomain(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "business_domains"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )

    owner: Mapped[Person | None] = relationship(back_populates="owned_business_domains")
    data_products: Mapped[list[DataProduct]] = relationship(back_populates="business_domain")


class DataProduct(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "data_products"
    __table_args__ = (
        Index("ix_data_products_name", "name"),
        Index("ix_data_products_status", "status"),
        Index("ix_data_products_type", "type"),
        Index("ix_data_products_quality_status", "quality_status"),
        Index("ix_data_products_business_domain_id", "business_domain_id"),
        Index("ix_data_products_capability_id", "capability_id"),
        Index("ix_data_products_team_id", "team_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[DataProductType] = mapped_column(
        Enum(DataProductType, native_enum=False, length=50),
        default=DataProductType.DATASET,
        nullable=False,
    )
    status: Mapped[DataProductStatus] = mapped_column(
        Enum(DataProductStatus, native_enum=False, length=50),
        default=DataProductStatus.DRAFT,
        nullable=False,
    )
    quality_status: Mapped[QualityStatus] = mapped_column(
        Enum(QualityStatus, native_enum=False, length=50),
        default=QualityStatus.UNKNOWN,
        nullable=False,
    )
    business_domain_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business_domains.id"),
        nullable=True,
    )
    business_owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    technical_owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    capability_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("capabilities.id"),
        nullable=True,
    )
    team_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id"),
        nullable=True,
    )
    refresh_frequency: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_systems: Mapped[str | None] = mapped_column(Text, nullable=True)
    consumers: Mapped[str | None] = mapped_column(Text, nullable=True)
    documentation_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    business_domain: Mapped[BusinessDomain | None] = relationship(
        back_populates="data_products",
    )
    business_owner: Mapped[Person | None] = relationship(
        back_populates="owned_business_data_products",
        foreign_keys=[business_owner_id],
    )
    technical_owner: Mapped[Person | None] = relationship(
        back_populates="owned_technical_data_products",
        foreign_keys=[technical_owner_id],
    )
    capability: Mapped[Capability | None] = relationship(back_populates="data_products")
    team: Mapped[Team | None] = relationship(back_populates="data_products")
    work_items: Mapped[list[WorkItem]] = relationship(back_populates="data_product")
    comments: Mapped[list[Comment]] = relationship(back_populates="data_product")
