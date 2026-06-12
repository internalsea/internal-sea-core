import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class DashboardSummary(BaseModel):
    data_products_total: int = 0
    data_products_active: int = 0
    data_products_with_quality_warning: int = 0
    data_products_with_quality_critical: int = 0
    work_items_total: int = 0
    work_items_open: int = 0
    work_items_overdue: int = 0
    work_items_technical_debt: int = 0
    work_items_risks: int = 0
    projects_total: int = 0
    projects_active: int = 0
    internal_projects_total: int = 0
    internal_projects_active: int = 0
    people_total: int = 0
    people_active: int = 0
    teams_total: int = 0
    capabilities_total: int = 0
    compliance_checks_total: int = 0
    compliance_checks_open: int = 0
    compliance_checks_non_compliant: int = 0
    compliance_checks_overdue: int = 0
    automation_triggers_active: int = 0
    automation_runs_failed: int = 0
    automation_next_runs: int = 0
    performance_metrics_total: int = 0
    performance_values_total: int = 0
    notification_messages_total: int = 0
    notification_messages_failed: int = 0


class RecentDataProductItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    type: str
    status: str
    quality_status: str
    updated_at: datetime


class HighPriorityWorkItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    type: str
    status: str
    priority: str
    due_date: date | None
    data_product_id: uuid.UUID | None
    project_id: uuid.UUID | None
    updated_at: datetime


class ProjectHealthItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    project_type: str
    status: str
    health_status: str | None
    client_name: str | None
    target_end_date: date | None
    open_work_items: int = 0
    overdue_work_items: int = 0


class CapabilityWorkloadItem(BaseModel):
    capability_id: uuid.UUID
    capability_name: str
    people_count: int = 0
    active_people_count: int = 0
    open_work_items: int = 0
    active_projects: int = 0
    active_data_products: int = 0


class OwnershipGapItem(BaseModel):
    entity_type: str
    entity_id: uuid.UUID
    name: str
    gap_type: str
    severity: str
    description: str


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    recent_data_products: list[RecentDataProductItem] = Field(default_factory=list)
    high_priority_work_items: list[HighPriorityWorkItem] = Field(default_factory=list)
    project_health: list[ProjectHealthItem] = Field(default_factory=list)
    capability_workload: list[CapabilityWorkloadItem] = Field(default_factory=list)
    ownership_gaps: list[OwnershipGapItem] = Field(default_factory=list)


class ExecutiveSummary(BaseModel):
    overall_status: str
    overall_score: int | None
    active_projects: int
    active_internal_projects: int
    active_data_products: int
    open_work_items: int
    overdue_work_items: int
    compliance_open_checks: int
    compliance_overdue_checks: int
    average_performance_score: float | None
    ownership_gaps: int
    automation_due_triggers: int
    notification_failed_messages: int
    generated_at: datetime


class OperationalHealth(BaseModel):
    status: str
    work_health_score: int | None
    project_health_score: int | None
    compliance_health_score: int | None
    performance_health_score: int | None
    automation_health_score: int | None
    risk_items_count: int
    critical_work_items_count: int
    overdue_items_count: int
    blocked_or_warning_projects: int
    generated_at: datetime


class DataProductHealthItem(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    quality_status: str | None
    business_owner_id: uuid.UUID | None
    technical_owner_id: uuid.UUID | None
    team_id: uuid.UUID | None
    capability_id: uuid.UUID | None
    open_work_items: int
    compliance_open_checks: int
    latest_performance_score: float | None
    health_status: str
    health_reasons: list[str]


class DataProductHealthResponse(BaseModel):
    total: int
    active: int
    good_quality: int
    warning_quality: int
    critical_quality: int
    missing_owner_count: int
    items: list[DataProductHealthItem]


class WorkDeliverySummary(BaseModel):
    total_work_items: int
    open_work_items: int
    done_work_items: int
    overdue_work_items: int
    critical_items: int
    risks: int
    technical_debt: int
    by_status: dict[str, int]
    by_priority: dict[str, int]
    by_type: dict[str, int]


class ProjectInsightItem(BaseModel):
    id: uuid.UUID
    name: str
    project_type: str
    status: str
    health_status: str | None
    target_end_date: date | None
    open_work_items: int
    overdue_work_items: int
    risks: int
    compliance_open_checks: int
    performance_score: float | None
    insight_status: str
    insight_reasons: list[str]


class ProjectInsightsResponse(BaseModel):
    total: int
    active: int
    warning_or_critical: int
    overdue_or_at_risk: int
    items: list[ProjectInsightItem]


class ComplianceCheckInsightItem(BaseModel):
    id: uuid.UUID
    title: str
    subject_type: str
    subject_id: uuid.UUID
    status: str
    due_date: date | None
    owner_id: uuid.UUID | None


class ComplianceInsights(BaseModel):
    policies_active: int
    active_rules: int
    active_controls: int
    checks_total: int
    checks_open: int
    checks_compliant: int
    checks_non_compliant: int
    checks_overdue: int
    evidence_missing: int
    by_status: dict[str, int]
    top_overdue_checks: list[ComplianceCheckInsightItem]


class MetricGapItem(BaseModel):
    subject_type: str
    subject_id: uuid.UUID
    metric_definition_id: uuid.UUID
    metric_name: str
    current_value: float | None
    target_value: float | None
    score: float | None
    trend: str | None


class PerformanceInsights(BaseModel):
    metric_definitions_active: int
    metric_values_total: int
    average_score: float | None
    scorecards_with_values: int
    weak_scorecards_count: int
    top_metric_gaps: list[MetricGapItem]


class AutomationRunInsightItem(BaseModel):
    id: uuid.UUID
    trigger_id: uuid.UUID
    status: str
    action_type: str | None
    target_type: str | None
    target_id: uuid.UUID | None
    error_message: str | None
    created_at: datetime


class AutomationHealth(BaseModel):
    schedules_active: int
    triggers_active: int
    due_triggers: int
    locked_triggers: int
    runs_total: int
    runs_failed: int
    runs_succeeded: int
    runs_simulated: int
    recent_failed_runs: list[AutomationRunInsightItem]


class NotificationMessageInsightItem(BaseModel):
    id: uuid.UUID
    status: str
    priority: str
    event_type: str
    subject: str | None
    recipient_value: str | None
    error_message: str | None
    updated_at: datetime


class NotificationHealth(BaseModel):
    channels_active: int
    templates_active: int
    messages_total: int
    messages_queued: int
    messages_failed: int
    delivery_attempts_failed: int
    recent_failed_messages: list[NotificationMessageInsightItem]


class RecentActivityItem(BaseModel):
    id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    action: str
    title: str
    description: str | None
    actor_id: uuid.UUID | None
    created_at: datetime


class RecentActivityResponse(BaseModel):
    items: list[RecentActivityItem]
    total: int


class ActionableInsight(BaseModel):
    id: str
    category: str
    severity: str
    title: str
    description: str
    entity_type: str | None
    entity_id: uuid.UUID | None
    recommended_action: str | None
    url: str | None


class ActionableInsightsResponse(BaseModel):
    items: list[ActionableInsight]
    total: int
    critical_count: int
    warning_count: int
    info_count: int


class AdvancedDashboardResponse(BaseModel):
    executive_summary: ExecutiveSummary
    operational_health: OperationalHealth
    data_product_health: DataProductHealthResponse
    work_delivery: WorkDeliverySummary
    project_insights: ProjectInsightsResponse
    compliance_insights: ComplianceInsights
    performance_insights: PerformanceInsights
    automation_health: AutomationHealth
    notification_health: NotificationHealth
    recent_activity: RecentActivityResponse
    actionable_insights: ActionableInsightsResponse
