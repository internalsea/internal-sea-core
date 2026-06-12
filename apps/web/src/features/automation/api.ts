import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  AutomationOverview,
  AutomationRunFilters,
  AutomationRunListResponse,
  AutomationRunRequest,
  AutomationRunResult,
  AutomationSchedule,
  AutomationScheduleCreateInput,
  AutomationScheduleFilters,
  AutomationScheduleListResponse,
  AutomationScheduleUpdateInput,
  AutomationTrigger,
  AutomationTriggerCreateInput,
  AutomationTriggerFilters,
  AutomationTriggerListResponse,
  AutomationTriggerUpdateInput,
  AutomationTargetType,
  EntityAutomationsResponse,
} from '@/features/automation/types'
import type { UUID } from '@/types/common'

function toScheduleQueryParams(
  filters?: AutomationScheduleFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) return undefined
  return {
    search: filters.search,
    frequency: filters.frequency,
    is_active: filters.is_active,
    page: filters.page,
    page_size: filters.page_size,
  }
}

function toTriggerQueryParams(
  filters?: AutomationTriggerFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) return undefined
  return {
    search: filters.search,
    status: filters.status,
    trigger_type: filters.trigger_type,
    action_type: filters.action_type,
    target_type: filters.target_type,
    target_id: filters.target_id,
    schedule_id: filters.schedule_id,
    page: filters.page,
    page_size: filters.page_size,
  }
}

function toRunQueryParams(
  filters?: AutomationRunFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) return undefined
  return {
    trigger_id: filters.trigger_id,
    status: filters.status,
    target_type: filters.target_type,
    target_id: filters.target_id,
    action_type: filters.action_type,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getAutomationOverview() {
  return apiGet<AutomationOverview>('/automation/overview')
}

export function getAutomationSchedules(filters?: AutomationScheduleFilters) {
  return apiGet<AutomationScheduleListResponse>('/automation/schedules', toScheduleQueryParams(filters))
}

export function getAutomationSchedule(id: UUID) {
  return apiGet<AutomationSchedule>(`/automation/schedules/${id}`)
}

export function createAutomationSchedule(payload: AutomationScheduleCreateInput) {
  return apiPost<AutomationSchedule>('/automation/schedules', payload)
}

export function updateAutomationSchedule(id: UUID, payload: AutomationScheduleUpdateInput) {
  return apiPatch<AutomationSchedule>(`/automation/schedules/${id}`, payload)
}

export function deleteAutomationSchedule(id: UUID) {
  return apiDelete(`/automation/schedules/${id}`)
}

export function getAutomationTriggers(filters?: AutomationTriggerFilters) {
  return apiGet<AutomationTriggerListResponse>('/automation/triggers', toTriggerQueryParams(filters))
}

export function getAutomationTrigger(id: UUID) {
  return apiGet<AutomationTrigger>(`/automation/triggers/${id}`)
}

export function createAutomationTrigger(payload: AutomationTriggerCreateInput) {
  return apiPost<AutomationTrigger>('/automation/triggers', payload)
}

export function updateAutomationTrigger(id: UUID, payload: AutomationTriggerUpdateInput) {
  return apiPatch<AutomationTrigger>(`/automation/triggers/${id}`, payload)
}

export function deleteAutomationTrigger(id: UUID) {
  return apiDelete(`/automation/triggers/${id}`)
}

export function getAutomationRuns(filters?: AutomationRunFilters) {
  return apiGet<AutomationRunListResponse>('/automation/runs', toRunQueryParams(filters))
}

export function getTriggerRuns(triggerId: UUID, page = 1, pageSize = 20) {
  return apiGet<AutomationRunListResponse>(`/automation/triggers/${triggerId}/runs`, {
    page,
    page_size: pageSize,
  })
}

export function runAutomationTrigger(triggerId: UUID, payload: AutomationRunRequest) {
  return apiPost<AutomationRunResult>(`/automation/triggers/${triggerId}/run`, payload)
}

export function getEntityAutomations(targetType: AutomationTargetType, targetId: UUID) {
  return apiGet<EntityAutomationsResponse>(`/automation/entity/${targetType}/${targetId}`)
}
