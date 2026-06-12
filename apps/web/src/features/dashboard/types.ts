export type DashboardSectionStatus = 'loading' | 'error' | 'ready'

export type HealthStatus = 'good' | 'warning' | 'critical' | 'unknown'
export type InsightSeverity = 'critical' | 'warning' | 'info'

export interface DashboardSummary {
  data_products_total: number
  data_products_active: number
  data_products_with_quality_warning: number
  data_products_with_quality_critical: number
  work_items_total: number
  work_items_open: number
  work_items_overdue: number
  work_items_technical_debt: number
  work_items_risks: number
  projects_total: number
  projects_active: number
  internal_projects_total: number
  internal_projects_active: number
  people_total: number
  people_active: number
  teams_total: number
  capabilities_total: number
  compliance_checks_total: number
  compliance_checks_open: number
  compliance_checks_non_compliant: number
  compliance_checks_overdue: number
  automation_triggers_active: number
  automation_runs_failed: number
  automation_next_runs: number
  performance_metrics_total: number
  performance_values_total: number
  notification_messages_total: number
  notification_messages_failed: number
}

export interface ExecutiveSummary {
  overall_status: HealthStatus
  overall_score: number | null
  active_projects: number
  active_internal_projects: number
  active_data_products: number
  open_work_items: number
  overdue_work_items: number
  compliance_open_checks: number
  compliance_overdue_checks: number
  average_performance_score: number | null
  ownership_gaps: number
  automation_due_triggers: number
  notification_failed_messages: number
  generated_at: string
}

export interface OperationalHealth {
  status: HealthStatus
  work_health_score: number | null
  project_health_score: number | null
  compliance_health_score: number | null
  performance_health_score: number | null
  automation_health_score: number | null
  risk_items_count: number
  critical_work_items_count: number
  overdue_items_count: number
  blocked_or_warning_projects: number
  generated_at: string
}

export interface DataProductHealthItem {
  id: string
  name: string
  status: string
  quality_status: string | null
  business_owner_id: string | null
  technical_owner_id: string | null
  team_id: string | null
  capability_id: string | null
  open_work_items: number
  compliance_open_checks: number
  latest_performance_score: number | null
  health_status: HealthStatus
  health_reasons: string[]
}

export interface DataProductHealthResponse {
  total: number
  active: number
  good_quality: number
  warning_quality: number
  critical_quality: number
  missing_owner_count: number
  items: DataProductHealthItem[]
}

export interface WorkDeliverySummary {
  total_work_items: number
  open_work_items: number
  done_work_items: number
  overdue_work_items: number
  critical_items: number
  risks: number
  technical_debt: number
  by_status: Record<string, number>
  by_priority: Record<string, number>
  by_type: Record<string, number>
}

export interface ProjectInsightItem {
  id: string
  name: string
  project_type: string
  status: string
  health_status: string | null
  target_end_date: string | null
  open_work_items: number
  overdue_work_items: number
  risks: number
  compliance_open_checks: number
  performance_score: number | null
  insight_status: HealthStatus
  insight_reasons: string[]
}

export interface ProjectInsightsResponse {
  total: number
  active: number
  warning_or_critical: number
  overdue_or_at_risk: number
  items: ProjectInsightItem[]
}

export interface ComplianceCheckInsightItem {
  id: string
  title: string
  subject_type: string
  subject_id: string
  status: string
  due_date: string | null
  owner_id: string | null
}

export interface ComplianceInsights {
  policies_active: number
  active_rules: number
  active_controls: number
  checks_total: number
  checks_open: number
  checks_compliant: number
  checks_non_compliant: number
  checks_overdue: number
  evidence_missing: number
  by_status: Record<string, number>
  top_overdue_checks: ComplianceCheckInsightItem[]
}

export interface MetricGapItem {
  subject_type: string
  subject_id: string
  metric_definition_id: string
  metric_name: string
  current_value: number | null
  target_value: number | null
  score: number | null
  trend: string | null
}

export interface PerformanceInsights {
  metric_definitions_active: number
  metric_values_total: number
  average_score: number | null
  scorecards_with_values: number
  weak_scorecards_count: number
  top_metric_gaps: MetricGapItem[]
}

export interface AutomationRunInsightItem {
  id: string
  trigger_id: string
  status: string
  action_type: string | null
  target_type: string | null
  target_id: string | null
  error_message: string | null
  created_at: string
}

export interface AutomationHealth {
  schedules_active: number
  triggers_active: number
  due_triggers: number
  locked_triggers: number
  runs_total: number
  runs_failed: number
  runs_succeeded: number
  runs_simulated: number
  recent_failed_runs: AutomationRunInsightItem[]
}

export interface NotificationMessageInsightItem {
  id: string
  status: string
  priority: string
  event_type: string
  subject: string | null
  recipient_value: string | null
  error_message: string | null
  updated_at: string
}

export interface NotificationHealth {
  channels_active: number
  templates_active: number
  messages_total: number
  messages_queued: number
  messages_failed: number
  delivery_attempts_failed: number
  recent_failed_messages: NotificationMessageInsightItem[]
}

export interface RecentActivityItem {
  id: string
  entity_type: string
  entity_id: string
  action: string
  title: string
  description: string | null
  actor_id: string | null
  created_at: string
}

export interface RecentActivityResponse {
  items: RecentActivityItem[]
  total: number
}

export interface ActionableInsight {
  id: string
  category: string
  severity: InsightSeverity
  title: string
  description: string
  entity_type: string | null
  entity_id: string | null
  recommended_action: string | null
  url: string | null
}

export interface ActionableInsightsResponse {
  items: ActionableInsight[]
  total: number
  critical_count: number
  warning_count: number
  info_count: number
}

export interface AdvancedDashboardResponse {
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
}

export interface RecentDataProductItem {
  id: string
  name: string
  type: string
  status: string
  quality_status: string
  updated_at: string
}

export interface HighPriorityWorkItem {
  id: string
  title: string
  type: string
  status: string
  priority: string
  due_date: string | null
  data_product_id: string | null
  project_id: string | null
  updated_at: string
}

export interface ProjectHealthItem {
  id: string
  name: string
  project_type: string
  status: string
  health_status: string | null
  client_name: string | null
  target_end_date: string | null
  open_work_items: number
  overdue_work_items: number
}

export interface CapabilityWorkloadItem {
  capability_id: string
  capability_name: string
  people_count: number
  active_people_count: number
  open_work_items: number
  active_projects: number
  active_data_products: number
}

export interface OwnershipGapItem {
  entity_type: string
  entity_id: string
  name: string
  gap_type: string
  severity: string
  description: string
}
