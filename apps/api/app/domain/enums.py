"""Shared domain enums."""

from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class SeniorityLevel(StrEnum):
    INTERN = "intern"
    JUNIOR = "junior"
    MEDIOR = "medior"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"
    DIRECTOR = "director"
    PARTNER = "partner"


class DataProductType(StrEnum):
    DASHBOARD = "dashboard"
    DATASET = "dataset"
    METRIC = "metric"
    KPI = "kpi"
    API = "api"
    AI_AGENT = "ai_agent"
    REPORT = "report"
    AUTOMATION = "automation"
    DATA_CONTRACT = "data_contract"
    OTHER = "other"


class DataProductStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class QualityStatus(StrEnum):
    UNKNOWN = "unknown"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"


class WorkItemType(StrEnum):
    EPIC = "epic"
    STORY = "story"
    TASK = "task"
    BUG = "bug"
    RISK = "risk"
    DECISION = "decision"
    TECHNICAL_DEBT = "technical_debt"
    IMPROVEMENT = "improvement"
    SUPPORT_REQUEST = "support_request"


class WorkItemStatus(StrEnum):
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    CLOSED = "closed"


class WorkItemPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CommentEntityType(StrEnum):
    DATA_PRODUCT = "data_product"
    WORK_ITEM = "work_item"


class CommentTargetType(StrEnum):
    DATA_PRODUCT = "data_product"
    WORK_ITEM = "work_item"
    PROJECT = "project"
    INTERNAL_PROJECT = "internal_project"


class ActivityEntityType(StrEnum):
    DATA_PRODUCT = "data_product"
    WORK_ITEM = "work_item"
    PROJECT = "project"
    INTERNAL_PROJECT = "internal_project"
    PERSON = "person"
    TEAM = "team"
    CAPABILITY = "capability"


class ActivityAction(StrEnum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    COMMENTED = "commented"
    STATUS_CHANGED = "status_changed"
    ASSIGNED = "assigned"
    LINKED = "linked"
    UNLINKED = "unlinked"


class ProjectType(StrEnum):
    CLIENT_PROJECT = "client_project"
    INTERNAL_PROJECT = "internal_project"
    POC = "poc"
    PILOT = "pilot"
    MVP = "mvp"
    INITIATIVE = "initiative"


class ProjectStatus(StrEnum):
    IDEA = "idea"
    PLANNED = "planned"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class PerformanceMetricType(StrEnum):
    UTILIZATION = "utilization"
    CAPACITY = "capacity"
    VELOCITY = "velocity"
    QUALITY = "quality"
    DELIVERY_HEALTH = "delivery_health"
    SLA_ADHERENCE = "sla_adherence"
    BUDGET_BURN = "budget_burn"
    RISK_SCORE = "risk_score"
    SATISFACTION = "satisfaction"
    CUSTOM = "custom"


class PerformanceSubjectType(StrEnum):
    PERSON = "person"
    TEAM = "team"
    CAPABILITY = "capability"
    PROJECT = "project"
    INTERNAL_PROJECT = "internal_project"
    DATA_PRODUCT = "data_product"


class MetricValueType(StrEnum):
    NUMBER = "number"
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    BOOLEAN = "boolean"
    SCORE = "score"
    DURATION_DAYS = "duration_days"
    COUNT = "count"


class MetricDirection(StrEnum):
    HIGHER_IS_BETTER = "higher_is_better"
    LOWER_IS_BETTER = "lower_is_better"
    TARGET_IS_BEST = "target_is_best"
    NEUTRAL = "neutral"


class MetricFrequency(StrEnum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class MetricStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class MetricValueStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class PerformanceTrend(StrEnum):
    UP = "up"
    DOWN = "down"
    STABLE = "stable"
    UNKNOWN = "unknown"


class ComplianceSubjectType(StrEnum):
    TEAM = "team"
    PROJECT = "project"
    INTERNAL_PROJECT = "internal_project"
    DATA_PRODUCT = "data_product"
    PERSON = "person"
    CAPABILITY = "capability"
    TOOL = "tool"


class ComplianceStatus(StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    EXCEPTION = "exception"
    NOT_APPLICABLE = "not_applicable"


class ControlType(StrEnum):
    MANUAL = "manual"
    AUTOMATED = "automated"
    DETECTIVE = "detective"
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"


class ControlStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class ComplianceCheckType(StrEnum):
    MANUAL = "manual"
    AUTOMATED = "automated"
    SELF_ASSESSMENT = "self_assessment"
    AUDIT = "audit"
    REVIEW = "review"


class ComplianceFrequency(StrEnum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    ON_CHANGE = "on_change"
    CUSTOM = "custom"


class EvidenceStatus(StrEnum):
    MISSING = "missing"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class PolicyStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class RuleSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ToolStatus(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    ACTIVE = "active"
    RESTRICTED = "restricted"
    DEPRECATED = "deprecated"
    BLOCKED = "blocked"


class TriggerType(StrEnum):
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EVENT_BASED = "event_based"
    WEBHOOK = "webhook"


class AutomationTargetType(StrEnum):
    DATA_PRODUCT = "data_product"
    PROJECT = "project"
    INTERNAL_PROJECT = "internal_project"
    COMPLIANCE_CHECK = "compliance_check"
    TEAM = "team"
    CAPABILITY = "capability"
    WORK_ITEM = "work_item"


class AutomationTriggerType(StrEnum):
    SCHEDULE = "schedule"
    STATUS_CHANGE = "status_change"
    DUE_DATE = "due_date"
    QUALITY_STATUS = "quality_status"
    COMPLIANCE_STATUS = "compliance_status"
    MANUAL = "manual"


class AutomationActionType(StrEnum):
    CREATE_WORK_ITEM = "create_work_item"
    CREATE_COMPLIANCE_CHECK = "create_compliance_check"
    ADD_COMMENT = "add_comment"
    CREATE_ACTIVITY_EVENT = "create_activity_event"
    SEND_NOTIFICATION = "send_notification"
    RUN_QUALITY_CHECK = "run_quality_check"
    RUN_COMPLIANCE_CHECK = "run_compliance_check"
    CALL_WEBHOOK = "call_webhook"
    CALL_AI_TOOL = "call_ai_tool"


class AutomationStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class AutomationRunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"
    SIMULATED = "simulated"


class ScheduleFrequency(StrEnum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class MeetingType(StrEnum):
    GOVERNANCE = "governance"
    DELIVERY = "delivery"
    PLANNING = "planning"
    REVIEW = "review"
    STEERING = "steering"
    ONE_TO_ONE = "one_to_one"
    SALES = "sales"
    DISCOVERY = "discovery"
    OTHER = "other"


class DealStatus(StrEnum):
    IDEA = "idea"
    DISCOVERY = "discovery"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"
    ARCHIVED = "archived"


class ExperimentStage(StrEnum):
    POTENTIAL_DEAL = "potential_deal"
    POC = "poc"
    PILOT = "pilot"
    MVP = "mvp"
    PROJECT = "project"
    STOPPED = "stopped"


class FileStorageType(StrEnum):
    LOCAL = "local"
    S3 = "s3"
    AZURE_BLOB = "azure_blob"
    GOOGLE_DRIVE = "google_drive"
    SHAREPOINT = "sharepoint"
    EXTERNAL_URL = "external_url"


class FileAssetType(StrEnum):
    DOCUMENT = "document"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    IMAGE = "image"
    PDF = "pdf"
    CONTRACT = "contract"
    EVIDENCE = "evidence"
    SPECIFICATION = "specification"
    REPORT = "report"
    OTHER = "other"


class FileSensitivity(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class FileStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class FileEntityType(StrEnum):
    DATA_PRODUCT = "data_product"
    WORK_ITEM = "work_item"
    PROJECT = "project"
    INTERNAL_PROJECT = "internal_project"
    PERSON = "person"
    TEAM = "team"
    CAPABILITY = "capability"
    COMPLIANCE_CHECK = "compliance_check"
    POLICY = "policy"
    RULE = "rule"
    MEETING = "meeting"
    DEAL = "deal"


class EntityType(StrEnum):
    DATA_PRODUCT = "data_product"
    WORK_ITEM = "work_item"
    PROJECT = "project"
    INTERNAL_PROJECT = "internal_project"
    PERSON = "person"
    TEAM = "team"
    CAPABILITY = "capability"
    POLICY = "policy"
    RULE = "rule"
    COMPLIANCE_CHECK = "compliance_check"
    FILE = "file"
    MEETING = "meeting"
    DEAL = "deal"
    TOOL = "tool"


class NotificationChannelType(StrEnum):
    EMAIL = "email"
    TEAMS = "teams"
    SLACK = "slack"
    WEBHOOK = "webhook"
    IN_APP = "in_app"
    OTHER = "other"


class NotificationChannelStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class NotificationTemplateStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class NotificationMessageStatus(StrEnum):
    DRAFT = "draft"
    QUEUED = "queued"
    SIMULATED = "simulated"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class NotificationDeliveryStatus(StrEnum):
    PENDING = "pending"
    SIMULATED = "simulated"
    SENT = "sent"
    FAILED = "failed"
    SKIPPED = "skipped"


class NotificationRecipientType(StrEnum):
    USER = "user"
    PERSON = "person"
    EMAIL = "email"
    CHANNEL = "channel"


class NotificationEventType(StrEnum):
    MANUAL = "manual"
    AUTOMATION_RUN = "automation_run"
    COMPLIANCE_DUE = "compliance_due"
    WORK_ITEM_DUE = "work_item_due"
    PROJECT_HEALTH = "project_health"
    DATA_PRODUCT_REVIEW = "data_product_review"
    SYSTEM = "system"


class CompanyStatus(StrEnum):
    TRIAL = "trial"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class CompanySize(StrEnum):
    SOLO = "solo"
    SIZE_2_10 = "size_2_10"
    SIZE_11_50 = "size_11_50"
    SIZE_51_200 = "size_51_200"
    SIZE_201_1000 = "size_201_1000"
    SIZE_1000_PLUS = "size_1000_plus"


class WorkspaceStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class CompanyMemberRole(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class CompanyMemberStatus(StrEnum):
    INVITED = "invited"
    ACTIVE = "active"
    INACTIVE = "inactive"
    REMOVED = "removed"


class TeamType(StrEnum):
    DELIVERY = "delivery"
    PRODUCT = "product"
    PLATFORM = "platform"
    GOVERNANCE = "governance"
    OPERATIONS = "operations"
    LEADERSHIP = "leadership"
    INTERNAL = "internal"


class Industry(StrEnum):
    FASHION = "fashion"
    CONSULTING = "consulting"
    TECHNOLOGY = "technology"
    RETAIL = "retail"
    ENERGY = "energy"
    FINANCE = "finance"
    MANUFACTURING = "manufacturing"
    OTHER = "other"


class EntityLinkType(StrEnum):
    RELATES_TO = "relates_to"
    DEPENDS_ON = "depends_on"
    BLOCKS = "blocks"
    DUPLICATES = "duplicates"
    REPLACES = "replaces"
    OWNS = "owns"
    SUPPORTS = "supports"
    IMPROVES = "improves"
    AFFECTS = "affects"
    CREATED_FROM = "created_from"
    EVIDENCE_FOR = "evidence_for"
    DECISION_FOR = "decision_for"
    RISK_FOR = "risk_for"
