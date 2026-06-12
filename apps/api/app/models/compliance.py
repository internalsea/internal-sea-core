"""Compliance and governance models."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin, WorkspaceScopedMixin
from app.domain.enums import (
    ComplianceCheckType,
    ComplianceFrequency,
    ComplianceStatus,
    ComplianceSubjectType,
    ControlStatus,
    ControlType,
    EvidenceStatus,
    PolicyStatus,
    RuleSeverity,
)

if TYPE_CHECKING:
    from app.models.files import FileAsset
    from app.models.identity import User
    from app.models.people import Person


class Policy(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "policies"
    __table_args__ = (
        Index("ix_policies_name", "name"),
        Index("ix_policies_status", "status"),
        Index("ix_policies_owner_id", "owner_id"),
        Index("ix_policies_effective_from", "effective_from"),
        Index("ix_policies_effective_to", "effective_to"),
        UniqueConstraint("name", name="uq_policies_name"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=PolicyStatus.DRAFT.value,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    effective_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    owner: Mapped[Person | None] = relationship("Person")
    rules: Mapped[list[ComplianceRule]] = relationship(
        "ComplianceRule",
        back_populates="policy",
        cascade="all, delete-orphan",
    )


class ComplianceRule(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "compliance_rules"
    __table_args__ = (
        Index("ix_compliance_rules_policy_id", "policy_id"),
        Index("ix_compliance_rules_code", "code"),
        Index("ix_compliance_rules_name", "name"),
        Index("ix_compliance_rules_severity", "severity"),
        Index("ix_compliance_rules_subject_type", "subject_type"),
        Index("ix_compliance_rules_is_active", "is_active"),
    )

    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policies.id"),
        nullable=False,
    )
    code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=RuleSeverity.MEDIUM.value,
    )
    subject_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    policy: Mapped[Policy] = relationship("Policy", back_populates="rules")
    controls: Mapped[list[Control]] = relationship(
        "Control",
        back_populates="rule",
        cascade="all, delete-orphan",
    )
    checks: Mapped[list[ComplianceCheck]] = relationship(
        "ComplianceCheck",
        back_populates="rule",
    )


class Control(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "controls"
    __table_args__ = (
        Index("ix_controls_rule_id", "rule_id"),
        Index("ix_controls_control_type", "control_type"),
        Index("ix_controls_status", "status"),
        Index("ix_controls_owner_id", "owner_id"),
        Index("ix_controls_frequency", "frequency"),
    )

    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("compliance_rules.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    control_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=ControlType.MANUAL.value,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=ControlStatus.ACTIVE.value,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    frequency: Mapped[str | None] = mapped_column(String(50), nullable=True)

    rule: Mapped[ComplianceRule] = relationship("ComplianceRule", back_populates="controls")
    owner: Mapped[Person | None] = relationship("Person")
    checks: Mapped[list[ComplianceCheck]] = relationship(
        "ComplianceCheck",
        back_populates="control",
    )


class ComplianceCheck(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "compliance_checks"
    __table_args__ = (
        Index("ix_compliance_checks_rule_id", "rule_id"),
        Index("ix_compliance_checks_control_id", "control_id"),
        Index("ix_compliance_checks_subject", "subject_type", "subject_id"),
        Index("ix_compliance_checks_status", "status"),
        Index("ix_compliance_checks_check_type", "check_type"),
        Index("ix_compliance_checks_owner_id", "owner_id"),
        Index("ix_compliance_checks_due_date", "due_date"),
        Index("ix_compliance_checks_completed_at", "completed_at"),
        Index("ix_compliance_checks_next_check_at", "next_check_at"),
    )

    rule_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("compliance_rules.id"),
        nullable=True,
    )
    control_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("controls.id"),
        nullable=True,
    )
    subject_type: Mapped[str] = mapped_column(String(50), nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    check_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=ComplianceCheckType.MANUAL.value,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=ComplianceStatus.NOT_STARTED.value,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_check_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    rule: Mapped[ComplianceRule | None] = relationship("ComplianceRule", back_populates="checks")
    control: Mapped[Control | None] = relationship("Control", back_populates="checks")
    owner: Mapped[Person | None] = relationship("Person")
    evidence_items: Mapped[list[ComplianceCheckEvidence]] = relationship(
        "ComplianceCheckEvidence",
        back_populates="compliance_check",
        cascade="all, delete-orphan",
    )


class ComplianceCheckEvidence(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "compliance_check_evidence"
    __table_args__ = (
        Index("ix_compliance_check_evidence_check_id", "compliance_check_id"),
        Index("ix_compliance_check_evidence_file_id", "file_id"),
        Index("ix_compliance_check_evidence_status", "status"),
        Index("ix_compliance_check_evidence_submitted_by_id", "submitted_by_id"),
        Index("ix_compliance_check_evidence_reviewed_by_id", "reviewed_by_id"),
        Index("ix_compliance_check_evidence_reviewed_at", "reviewed_at"),
        UniqueConstraint(
            "compliance_check_id",
            "file_id",
            name="uq_compliance_check_evidence_check_file",
        ),
    )

    compliance_check_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("compliance_checks.id"),
        nullable=False,
    )
    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_assets.id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=EvidenceStatus.SUBMITTED.value,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    reviewed_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    compliance_check: Mapped[ComplianceCheck] = relationship(
        "ComplianceCheck",
        back_populates="evidence_items",
    )
    file: Mapped[FileAsset] = relationship("FileAsset")
    submitted_by: Mapped[User | None] = relationship("User", foreign_keys=[submitted_by_id])
    reviewed_by: Mapped[User | None] = relationship("User", foreign_keys=[reviewed_by_id])
