import { ApiError } from '@/lib/apiClient'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import { getEntityHref } from '@/features/entity-picker/utils'
import {
  AUTOMATION_ACTION_TYPES,
  AUTOMATION_RUN_STATUSES,
  AUTOMATION_TRIGGER_TYPES,
  MVP_ACTION_TYPES,
  SCHEDULE_FREQUENCIES,
} from '@/features/automation/constants'
import type {
  AutomationActionType,
  AutomationSchedule,
  AutomationScheduleCreateInput,
  AutomationScheduleFormValues,
  AutomationScheduleUpdateInput,
  AutomationTargetType,
  AutomationTriggerCreateInput,
  AutomationTriggerFormValues,
  AutomationTriggerType,
  AutomationTriggerUpdateInput,
  ScheduleFrequency,
} from '@/features/automation/types'

export function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return '—'
  }
  return new Date(value).toLocaleString()
}

export function formatFrequency(value: string): string {
  return SCHEDULE_FREQUENCIES.find((item) => item.value === value)?.label ?? value
}

export function formatTriggerType(value: string): string {
  return AUTOMATION_TRIGGER_TYPES.find((item) => item.value === value)?.label ?? value
}

export function formatActionType(value: string): string {
  return AUTOMATION_ACTION_TYPES.find((item) => item.value === value)?.label ?? value
}

export function formatRunStatus(value: string): string {
  return AUTOMATION_RUN_STATUSES.find((item) => item.value === value)?.label ?? value
}

function emptyToNull(value: string): string | null {
  const trimmed = value.trim()
  return trimmed === '' ? null : trimmed
}

function datetimeToIso(value: string): string | null {
  const trimmed = value.trim()
  if (!trimmed) {
    return null
  }
  return new Date(trimmed).toISOString()
}

export function cleanScheduleCreatePayload(
  values: AutomationScheduleFormValues,
): AutomationScheduleCreateInput {
  return {
    name: values.name.trim(),
    description: emptyToNull(values.description),
    frequency: values.frequency,
    timezone: emptyToNull(values.timezone) ?? 'UTC',
    start_at: datetimeToIso(values.start_at),
    end_at: datetimeToIso(values.end_at),
    next_run_at: datetimeToIso(values.next_run_at),
    cron_expression: values.frequency === 'custom' ? emptyToNull(values.cron_expression) : null,
    is_active: values.is_active,
  }
}

export function cleanScheduleUpdatePayload(
  values: AutomationScheduleFormValues,
): AutomationScheduleUpdateInput {
  return cleanScheduleCreatePayload(values)
}

export function cleanTriggerCreatePayload(
  values: AutomationTriggerFormValues,
  target: EntityPickerValue | null,
): AutomationTriggerCreateInput {
  return cleanTriggerPayload(values, target) as AutomationTriggerCreateInput
}

export function cleanTriggerUpdatePayload(
  values: AutomationTriggerFormValues,
  target: EntityPickerValue | null,
): AutomationTriggerUpdateInput {
  return cleanTriggerPayload(values, target)
}

export function parseJsonField(value: string): Record<string, unknown> | null {
  const trimmed = value.trim()
  if (!trimmed) {
    return null
  }
  return JSON.parse(trimmed) as Record<string, unknown>
}

export function stringifyJsonField(value: Record<string, unknown> | null | undefined): string {
  if (!value || Object.keys(value).length === 0) {
    return ''
  }
  return JSON.stringify(value, null, 2)
}

export function cleanTriggerPayload(
  values: AutomationTriggerFormValues,
  target: EntityPickerValue | null,
): AutomationTriggerCreateInput | AutomationTriggerUpdateInput {
  return {
    name: values.name.trim(),
    description: emptyToNull(values.description),
    status: values.status,
    trigger_type: values.trigger_type,
    action_type: values.action_type,
    schedule_id: emptyToNull(values.schedule_id),
    target_type: (target?.entity_type as AutomationTargetType | undefined) ?? null,
    target_id: target?.entity_id ?? null,
    conditions: parseJsonField(values.conditionsJson),
    action_config: parseJsonField(values.actionConfigJson),
  }
}

export function getAutomationTargetHref(
  targetType: string | null,
  targetId: string | null,
): string | null {
  if (!targetType || !targetId) {
    return null
  }
  return getEntityHref(targetType as Parameters<typeof getEntityHref>[0], targetId)
}

export function isActionImplementedInMvp(actionType: AutomationActionType): boolean {
  return MVP_ACTION_TYPES.includes(actionType)
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'Something went wrong'
}

function toDatetimeLocalInput(value: string | null | undefined): string {
  if (!value) {
    return ''
  }
  const date = new Date(value)
  const pad = (part: number) => String(part).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

export function scheduleToFormValues(schedule: AutomationSchedule): AutomationScheduleFormValues {
  return {
    name: schedule.name ?? '',
    description: schedule.description ?? '',
    frequency: (schedule.frequency as ScheduleFrequency) ?? 'monthly',
    timezone: schedule.timezone ?? 'UTC',
    start_at: toDatetimeLocalInput(schedule.start_at),
    end_at: toDatetimeLocalInput(schedule.end_at),
    next_run_at: toDatetimeLocalInput(schedule.next_run_at),
    cron_expression: schedule.cron_expression ?? '',
    is_active: schedule.is_active ?? true,
  }
}

export function triggerToFormValues(trigger: {
  name?: string
  description?: string | null
  status?: AutomationTriggerFormValues['status']
  trigger_type?: AutomationTriggerType
  action_type?: AutomationActionType
  schedule_id?: string | null
  conditions?: Record<string, unknown> | null
  action_config?: Record<string, unknown> | null
}): AutomationTriggerFormValues {
  return {
    name: trigger.name ?? '',
    description: trigger.description ?? '',
    status: trigger.status ?? 'draft',
    trigger_type: trigger.trigger_type ?? 'schedule',
    action_type: trigger.action_type ?? 'create_work_item',
    schedule_id: trigger.schedule_id ?? '',
    conditionsJson: stringifyJsonField(trigger.conditions),
    actionConfigJson: stringifyJsonField(trigger.action_config),
  }
}
