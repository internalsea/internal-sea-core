import { ApiError } from '@/lib/apiClient'
import type {
  MetricDefinitionFormValues,
  MetricValueFormValues,
  PerformanceMetricDefinitionCreateInput,
  PerformanceMetricValueCreateInput,
  PerformanceSubjectType,
} from '@/features/performance/types'
import type { BadgeVariant } from '@/lib/designTokens'

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    const body = error.body as { detail?: string } | undefined
    if (body?.detail) return body.detail
    return error.message
  }
  if (error instanceof Error) return error.message
  return 'An unexpected error occurred'
}

export function formatMetricValue(
  valueNumeric: string | null | undefined,
  valueText: string | null | undefined,
  valueBool: boolean | null | undefined,
  unit?: string | null,
): string {
  if (valueNumeric != null && valueNumeric !== '') {
    return unit ? `${valueNumeric} ${unit}` : valueNumeric
  }
  if (valueText) return valueText
  if (valueBool != null) return valueBool ? 'Yes' : 'No'
  return '—'
}

export function formatScore(score: string | null | undefined): string {
  if (!score) return '—'
  return score
}

export function formatDate(value: string | null | undefined): string {
  if (!value) return '—'
  return new Date(value).toLocaleDateString()
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) return '—'
  return new Date(value).toLocaleString()
}

export function formatSubjectType(subjectType: PerformanceSubjectType): string {
  return subjectType.replace(/_/g, ' ')
}

export function getSubjectHref(
  subjectType: PerformanceSubjectType,
  subjectId: string,
): string {
  const routes: Record<PerformanceSubjectType, string> = {
    person: `/people/${subjectId}`,
    team: `/teams/${subjectId}`,
    capability: `/capabilities/${subjectId}`,
    project: `/projects/${subjectId}`,
    internal_project: `/internal-projects/${subjectId}`,
    data_product: `/data-products/${subjectId}`,
  }
  return routes[subjectType]
}

export function parseDecimalInput(value: string): string | null {
  const trimmed = value.trim()
  if (!trimmed) return null
  return trimmed
}

function nullIfEmpty(value: string): string | null {
  const trimmed = value.trim()
  return trimmed ? trimmed : null
}

export function cleanMetricDefinitionPayload(
  values: MetricDefinitionFormValues,
): PerformanceMetricDefinitionCreateInput {
  return {
    name: values.name.trim(),
    code: nullIfEmpty(values.code),
    description: nullIfEmpty(values.description),
    subject_type: values.subject_type,
    value_type: values.value_type,
    direction: values.direction,
    frequency: values.frequency || null,
    status: values.status,
    unit: nullIfEmpty(values.unit),
    target_value: parseDecimalInput(values.target_value),
    warning_threshold: parseDecimalInput(values.warning_threshold),
    critical_threshold: parseDecimalInput(values.critical_threshold),
    owner_id: values.owner_id,
  }
}

export function cleanMetricValuePayload(
  values: MetricValueFormValues,
): PerformanceMetricValueCreateInput {
  const valueBool =
    values.value_bool === 'true' ? true : values.value_bool === 'false' ? false : undefined

  return {
    metric_definition_id: values.metric_definition_id,
    subject_type: values.subject_type,
    subject_id: values.subject_id,
    period_start: nullIfEmpty(values.period_start),
    period_end: nullIfEmpty(values.period_end),
    value_numeric: parseDecimalInput(values.value_numeric),
    value_text: nullIfEmpty(values.value_text),
    value_bool: valueBool,
    status: values.status,
    source: nullIfEmpty(values.source),
    comment: nullIfEmpty(values.comment),
  }
}

export function getHealthVariantFromScore(
  averageScore: string | null | undefined,
): BadgeVariant {
  if (!averageScore) return 'neutral'
  const score = Number(averageScore)
  if (Number.isNaN(score)) return 'neutral'
  if (score >= 90) return 'success'
  if (score >= 70) return 'warning'
  return 'danger'
}

export function definitionToFormValues(
  definition: import('@/features/performance/types').PerformanceMetricDefinition,
): MetricDefinitionFormValues {
  return {
    name: definition.name,
    code: definition.code ?? '',
    description: definition.description ?? '',
    subject_type: definition.subject_type,
    value_type: definition.value_type,
    direction: definition.direction,
    frequency: definition.frequency ?? '',
    status: definition.status,
    unit: definition.unit ?? '',
    target_value: definition.target_value ?? '',
    warning_threshold: definition.warning_threshold ?? '',
    critical_threshold: definition.critical_threshold ?? '',
    owner_id: definition.owner_id,
  }
}

export function valueToFormValues(
  value: import('@/features/performance/types').PerformanceMetricValue,
): MetricValueFormValues {
  return {
    metric_definition_id: value.metric_definition_id,
    subject_type: value.subject_type,
    subject_id: value.subject_id,
    period_start: value.period_start ?? '',
    period_end: value.period_end ?? '',
    value_numeric: value.value_numeric ?? '',
    value_text: value.value_text ?? '',
    value_bool: value.value_bool == null ? '' : value.value_bool ? 'true' : 'false',
    status: value.status,
    source: value.source ?? '',
    comment: value.comment ?? '',
  }
}
