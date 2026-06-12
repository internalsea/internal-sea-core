import type { PaginatedResponse } from '@/types/common'

export type PerformanceSubjectType =
  | 'person'
  | 'team'
  | 'capability'
  | 'project'
  | 'internal_project'
  | 'data_product'

export type MetricValueType =
  | 'number'
  | 'percentage'
  | 'currency'
  | 'boolean'
  | 'score'
  | 'duration_days'
  | 'count'

export type MetricDirection =
  | 'higher_is_better'
  | 'lower_is_better'
  | 'target_is_best'
  | 'neutral'

export type MetricFrequency =
  | 'once'
  | 'daily'
  | 'weekly'
  | 'monthly'
  | 'quarterly'
  | 'yearly'
  | 'custom'

export type MetricStatus = 'draft' | 'active' | 'deprecated' | 'archived'

export type MetricValueStatus = 'draft' | 'submitted' | 'approved' | 'rejected'

export type PerformanceTrend = 'up' | 'down' | 'stable' | 'unknown'

export interface PerformanceMetricDefinition {
  id: string
  name: string
  code: string | null
  description: string | null
  subject_type: PerformanceSubjectType
  value_type: MetricValueType
  direction: MetricDirection
  frequency: MetricFrequency | null
  status: MetricStatus
  unit: string | null
  target_value: string | null
  warning_threshold: string | null
  critical_threshold: string | null
  owner_id: string | null
  created_at: string
  updated_at: string
}

export interface PerformanceMetricDefinitionCreateInput {
  name: string
  code?: string | null
  description?: string | null
  subject_type: PerformanceSubjectType
  value_type?: MetricValueType
  direction?: MetricDirection
  frequency?: MetricFrequency | null
  status?: MetricStatus
  unit?: string | null
  target_value?: string | null
  warning_threshold?: string | null
  critical_threshold?: string | null
  owner_id?: string | null
}

export type PerformanceMetricDefinitionUpdateInput = Partial<PerformanceMetricDefinitionCreateInput>

export interface PerformanceMetricDefinitionListItem {
  id: string
  name: string
  code: string | null
  subject_type: PerformanceSubjectType
  value_type: MetricValueType
  direction: MetricDirection
  frequency: MetricFrequency | null
  status: MetricStatus
  unit: string | null
  target_value: string | null
  owner_id: string | null
  updated_at: string
}

export type PerformanceMetricDefinitionListResponse =
  PaginatedResponse<PerformanceMetricDefinitionListItem>

export interface PerformanceMetricValue {
  id: string
  metric_definition_id: string
  subject_type: PerformanceSubjectType
  subject_id: string
  period_start: string | null
  period_end: string | null
  value_numeric: string | null
  value_text: string | null
  value_bool: boolean | null
  status: MetricValueStatus
  source: string | null
  comment: string | null
  submitted_by_id: string | null
  approved_by_id: string | null
  approved_at: string | null
  created_at: string
  updated_at: string
}

export interface PerformanceMetricValueCreateInput {
  metric_definition_id: string
  subject_type: PerformanceSubjectType
  subject_id: string
  period_start?: string | null
  period_end?: string | null
  value_numeric?: string | null
  value_text?: string | null
  value_bool?: boolean | null
  status?: MetricValueStatus
  source?: string | null
  comment?: string | null
}

export type PerformanceMetricValueUpdateInput = Partial<PerformanceMetricValueCreateInput>

export interface PerformanceMetricValueListItem {
  id: string
  metric_definition_id: string
  subject_type: PerformanceSubjectType
  subject_id: string
  period_start: string | null
  period_end: string | null
  value_numeric: string | null
  value_text: string | null
  value_bool: boolean | null
  status: MetricValueStatus
  source: string | null
  updated_at: string
}

export type PerformanceMetricValueListResponse = PaginatedResponse<PerformanceMetricValueListItem>

export interface PerformanceScorecardMetric {
  metric_definition_id: string
  name: string
  code: string | null
  value_type: MetricValueType
  direction: MetricDirection
  unit: string | null
  target_value: string | null
  current_value_numeric: string | null
  current_value_text: string | null
  current_value_bool: boolean | null
  previous_value_numeric: string | null
  trend: PerformanceTrend
  status: string | null
  period_start: string | null
  period_end: string | null
  score: string | null
  interpretation: string | null
}

export interface PerformanceScorecard {
  subject_type: PerformanceSubjectType
  subject_id: string
  metrics: PerformanceScorecardMetric[]
  metrics_total: number
  metrics_with_values: number
  average_score: string | null
  health_status: string | null
  updated_at: string | null
}

export interface PerformanceOverview {
  metric_definitions_total: number
  metric_definitions_active: number
  metric_values_total: number
  scorecards_available: number
  people_metrics_count: number
  team_metrics_count: number
  capability_metrics_count: number
  project_metrics_count: number
  data_product_metrics_count: number
}

export interface MetricDefinitionFilters {
  search?: string
  subject_type?: PerformanceSubjectType
  value_type?: MetricValueType
  status?: MetricStatus
  owner_id?: string
  page?: number
  page_size?: number
}

export interface MetricValueFilters {
  metric_definition_id?: string
  subject_type?: PerformanceSubjectType
  subject_id?: string
  status?: MetricValueStatus
  period_start_from?: string
  period_end_to?: string
  page?: number
  page_size?: number
}

export interface MetricDefinitionFormValues {
  name: string
  code: string
  description: string
  subject_type: PerformanceSubjectType
  value_type: MetricValueType
  direction: MetricDirection
  frequency: MetricFrequency | ''
  status: MetricStatus
  unit: string
  target_value: string
  warning_threshold: string
  critical_threshold: string
  owner_id: string | null
}

export interface MetricValueFormValues {
  metric_definition_id: string
  subject_type: PerformanceSubjectType
  subject_id: string
  period_start: string
  period_end: string
  value_numeric: string
  value_text: string
  value_bool: string
  status: MetricValueStatus
  source: string
  comment: string
}
