import type { EntityPickerType } from '@/features/entity-picker/types'
import type {
  MetricDirection,
  MetricFrequency,
  MetricStatus,
  MetricValueStatus,
  MetricValueType,
  PerformanceSubjectType,
  PerformanceTrend,
} from '@/features/performance/types'
import type { BadgeVariant } from '@/lib/designTokens'

export const PERFORMANCE_SUBJECT_TYPES: { value: PerformanceSubjectType; label: string }[] = [
  { value: 'person', label: 'Person' },
  { value: 'team', label: 'Team' },
  { value: 'capability', label: 'Capability' },
  { value: 'project', label: 'Project' },
  { value: 'internal_project', label: 'Internal project' },
  { value: 'data_product', label: 'Data product' },
]

export const METRIC_VALUE_TYPES: { value: MetricValueType; label: string }[] = [
  { value: 'number', label: 'Number' },
  { value: 'percentage', label: 'Percentage' },
  { value: 'currency', label: 'Currency' },
  { value: 'boolean', label: 'Boolean' },
  { value: 'score', label: 'Score' },
  { value: 'duration_days', label: 'Duration (days)' },
  { value: 'count', label: 'Count' },
]

export const METRIC_DIRECTIONS: { value: MetricDirection; label: string }[] = [
  { value: 'higher_is_better', label: 'Higher is better' },
  { value: 'lower_is_better', label: 'Lower is better' },
  { value: 'target_is_best', label: 'Target is best' },
  { value: 'neutral', label: 'Neutral' },
]

export const METRIC_FREQUENCIES: { value: MetricFrequency; label: string }[] = [
  { value: 'once', label: 'Once' },
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
  { value: 'quarterly', label: 'Quarterly' },
  { value: 'yearly', label: 'Yearly' },
  { value: 'custom', label: 'Custom' },
]

export const METRIC_STATUSES: { value: MetricStatus; label: string }[] = [
  { value: 'draft', label: 'Draft' },
  { value: 'active', label: 'Active' },
  { value: 'deprecated', label: 'Deprecated' },
  { value: 'archived', label: 'Archived' },
]

export const METRIC_VALUE_STATUSES: { value: MetricValueStatus; label: string }[] = [
  { value: 'draft', label: 'Draft' },
  { value: 'submitted', label: 'Submitted' },
  { value: 'approved', label: 'Approved' },
  { value: 'rejected', label: 'Rejected' },
]

export const PERFORMANCE_TRENDS: { value: PerformanceTrend; label: string }[] = [
  { value: 'up', label: 'Up' },
  { value: 'down', label: 'Down' },
  { value: 'stable', label: 'Stable' },
  { value: 'unknown', label: 'Unknown' },
]

export const METRIC_STATUS_BADGE: Record<MetricStatus, BadgeVariant> = {
  draft: 'neutral',
  active: 'success',
  deprecated: 'warning',
  archived: 'neutral',
}

export const METRIC_VALUE_STATUS_BADGE: Record<MetricValueStatus, BadgeVariant> = {
  draft: 'neutral',
  submitted: 'info',
  approved: 'success',
  rejected: 'danger',
}

export const TREND_BADGE: Record<PerformanceTrend, BadgeVariant> = {
  up: 'success',
  down: 'warning',
  stable: 'neutral',
  unknown: 'neutral',
}

export const PERFORMANCE_SUBJECT_PICKER_TYPES: EntityPickerType[] = [
  'person',
  'team',
  'capability',
  'project',
  'internal_project',
  'data_product',
]

export const DEFAULT_PAGE_SIZE = 20
