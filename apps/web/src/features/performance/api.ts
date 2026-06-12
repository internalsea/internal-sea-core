import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  MetricDefinitionFilters,
  MetricValueFilters,
  PerformanceMetricDefinition,
  PerformanceMetricDefinitionCreateInput,
  PerformanceMetricDefinitionListResponse,
  PerformanceMetricDefinitionUpdateInput,
  PerformanceMetricValue,
  PerformanceMetricValueCreateInput,
  PerformanceMetricValueListResponse,
  PerformanceMetricValueUpdateInput,
  PerformanceOverview,
  PerformanceScorecard,
  PerformanceSubjectType,
} from '@/features/performance/types'

function definitionQueryParams(
  filters?: MetricDefinitionFilters,
): Record<string, string | number | undefined> | undefined {
  if (!filters) return undefined
  return {
    search: filters.search,
    subject_type: filters.subject_type,
    value_type: filters.value_type,
    status: filters.status,
    owner_id: filters.owner_id,
    page: filters.page,
    page_size: filters.page_size,
  }
}

function valueQueryParams(
  filters?: MetricValueFilters,
): Record<string, string | number | undefined> | undefined {
  if (!filters) return undefined
  return {
    metric_definition_id: filters.metric_definition_id,
    subject_type: filters.subject_type,
    subject_id: filters.subject_id,
    status: filters.status,
    period_start_from: filters.period_start_from,
    period_end_to: filters.period_end_to,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getPerformanceOverview(): Promise<PerformanceOverview> {
  return apiGet<PerformanceOverview>('/performance/overview')
}

export function getMetricDefinitions(
  filters?: MetricDefinitionFilters,
): Promise<PerformanceMetricDefinitionListResponse> {
  return apiGet<PerformanceMetricDefinitionListResponse>(
    '/performance/metrics',
    definitionQueryParams(filters),
  )
}

export function getMetricDefinition(id: string): Promise<PerformanceMetricDefinition> {
  return apiGet<PerformanceMetricDefinition>(`/performance/metrics/${id}`)
}

export function createMetricDefinition(
  payload: PerformanceMetricDefinitionCreateInput,
): Promise<PerformanceMetricDefinition> {
  return apiPost<PerformanceMetricDefinition>('/performance/metrics', payload)
}

export function updateMetricDefinition(
  id: string,
  payload: PerformanceMetricDefinitionUpdateInput,
): Promise<PerformanceMetricDefinition> {
  return apiPatch<PerformanceMetricDefinition>(`/performance/metrics/${id}`, payload)
}

export function deleteMetricDefinition(id: string): Promise<void> {
  return apiDelete(`/performance/metrics/${id}`)
}

export function getMetricValues(
  filters?: MetricValueFilters,
): Promise<PerformanceMetricValueListResponse> {
  return apiGet<PerformanceMetricValueListResponse>('/performance/values', valueQueryParams(filters))
}

export function getMetricValue(id: string): Promise<PerformanceMetricValue> {
  return apiGet<PerformanceMetricValue>(`/performance/values/${id}`)
}

export function createMetricValue(
  payload: PerformanceMetricValueCreateInput,
): Promise<PerformanceMetricValue> {
  return apiPost<PerformanceMetricValue>('/performance/values', payload)
}

export function updateMetricValue(
  id: string,
  payload: PerformanceMetricValueUpdateInput,
): Promise<PerformanceMetricValue> {
  return apiPatch<PerformanceMetricValue>(`/performance/values/${id}`, payload)
}

export function deleteMetricValue(id: string): Promise<void> {
  return apiDelete(`/performance/values/${id}`)
}

export function getEntityPerformanceScorecard(
  subjectType: PerformanceSubjectType,
  subjectId: string,
): Promise<PerformanceScorecard> {
  return apiGet<PerformanceScorecard>(
    `/performance/entity/${subjectType}/${subjectId}/scorecard`,
  )
}

export function getEntityPerformanceValues(
  subjectType: PerformanceSubjectType,
  subjectId: string,
  filters?: Pick<MetricValueFilters, 'page' | 'page_size'>,
): Promise<PerformanceMetricValueListResponse> {
  return apiGet<PerformanceMetricValueListResponse>(
    `/performance/entity/${subjectType}/${subjectId}/values`,
    valueQueryParams(filters),
  )
}
