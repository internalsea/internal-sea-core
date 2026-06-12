import type { PaginatedResponse, UUID } from '@/types/common'

export type AutomationTargetType =
  | 'data_product'
  | 'project'
  | 'internal_project'
  | 'compliance_check'
  | 'team'
  | 'capability'
  | 'work_item'

export type AutomationTriggerType =
  | 'schedule'
  | 'status_change'
  | 'due_date'
  | 'quality_status'
  | 'compliance_status'
  | 'manual'

export type AutomationActionType =
  | 'create_work_item'
  | 'create_compliance_check'
  | 'add_comment'
  | 'create_activity_event'
  | 'send_notification'
  | 'run_quality_check'
  | 'run_compliance_check'
  | 'call_webhook'
  | 'call_ai_tool'

export type AutomationStatus = 'draft' | 'active' | 'paused' | 'archived'

export type AutomationRunStatus =
  | 'pending'
  | 'running'
  | 'succeeded'
  | 'failed'
  | 'skipped'
  | 'simulated'

export type ScheduleFrequency =
  | 'once'
  | 'daily'
  | 'weekly'
  | 'monthly'
  | 'quarterly'
  | 'yearly'
  | 'custom'

export interface AutomationSchedule {
  id: UUID
  name: string
  description: string | null
  frequency: ScheduleFrequency
  timezone: string | null
  start_at: string | null
  end_at: string | null
  next_run_at: string | null
  last_run_at: string | null
  cron_expression: string | null
  is_active: boolean
  created_by_id: UUID | null
  created_at: string
  updated_at: string
}

export interface AutomationScheduleCreateInput {
  name: string
  description?: string | null
  frequency?: ScheduleFrequency
  timezone?: string | null
  start_at?: string | null
  end_at?: string | null
  next_run_at?: string | null
  cron_expression?: string | null
  is_active?: boolean
}

export interface AutomationScheduleUpdateInput {
  name?: string
  description?: string | null
  frequency?: ScheduleFrequency
  timezone?: string | null
  start_at?: string | null
  end_at?: string | null
  next_run_at?: string | null
  cron_expression?: string | null
  is_active?: boolean
}

export interface AutomationScheduleListItem {
  id: UUID
  name: string
  frequency: string
  next_run_at: string | null
  last_run_at: string | null
  is_active: boolean
  updated_at: string
}

export type AutomationScheduleListResponse = PaginatedResponse<AutomationScheduleListItem>

export interface AutomationTrigger {
  id: UUID
  name: string
  description: string | null
  status: AutomationStatus
  trigger_type: AutomationTriggerType
  action_type: AutomationActionType
  schedule_id: UUID | null
  target_type: AutomationTargetType | null
  target_id: UUID | null
  conditions: Record<string, unknown> | null
  action_config: Record<string, unknown> | null
  created_by_id: UUID | null
  last_run_at: string | null
  next_run_at: string | null
  locked_at?: string | null
  locked_by?: string | null
  lock_expires_at?: string | null
  created_at: string
  updated_at: string
}

export interface AutomationTriggerCreateInput {
  name: string
  description?: string | null
  status?: AutomationStatus
  trigger_type?: AutomationTriggerType
  action_type: AutomationActionType
  schedule_id?: UUID | null
  target_type?: AutomationTargetType | null
  target_id?: UUID | null
  conditions?: Record<string, unknown> | null
  action_config?: Record<string, unknown> | null
}

export interface AutomationTriggerUpdateInput {
  name?: string
  description?: string | null
  status?: AutomationStatus
  trigger_type?: AutomationTriggerType
  action_type?: AutomationActionType
  schedule_id?: UUID | null
  target_type?: AutomationTargetType | null
  target_id?: UUID | null
  conditions?: Record<string, unknown> | null
  action_config?: Record<string, unknown> | null
}

export interface AutomationTriggerListItem {
  id: UUID
  name: string
  status: string
  trigger_type: string
  action_type: string
  schedule_id: UUID | null
  target_type: string | null
  target_id: UUID | null
  last_run_at: string | null
  next_run_at: string | null
  updated_at: string
}

export type AutomationTriggerListResponse = PaginatedResponse<AutomationTriggerListItem>

export interface AutomationRun {
  id: UUID
  trigger_id: UUID
  status: AutomationRunStatus
  started_at: string | null
  finished_at: string | null
  target_type: string | null
  target_id: UUID | null
  action_type: string | null
  result_summary: string | null
  result_details: Record<string, unknown> | null
  error_message: string | null
  executed_by_id: UUID | null
  created_at: string
  updated_at: string
}

export type AutomationRunListResponse = PaginatedResponse<AutomationRun>

export interface AutomationRunRequest {
  simulate?: boolean
}

export interface AutomationRunResult {
  run: AutomationRun
  created_work_item_id: UUID | null
  created_comment_id: UUID | null
  created_activity_event_id: UUID | null
  message: string
}

export interface EntityAutomationsResponse {
  target_type: AutomationTargetType
  target_id: UUID
  triggers: AutomationTriggerListItem[]
  total: number
}

export interface AutomationOverview {
  schedules_total: number
  schedules_active: number
  triggers_total: number
  triggers_active: number
  triggers_paused: number
  runs_total: number
  runs_succeeded: number
  runs_failed: number
  runs_simulated: number
  next_runs_count: number
}

export interface AutomationScheduleFilters {
  search?: string
  frequency?: ScheduleFrequency
  is_active?: boolean
  page?: number
  page_size?: number
}

export interface AutomationTriggerFilters {
  search?: string
  status?: AutomationStatus
  trigger_type?: AutomationTriggerType
  action_type?: AutomationActionType
  target_type?: AutomationTargetType
  target_id?: UUID
  schedule_id?: UUID
  page?: number
  page_size?: number
}

export interface AutomationRunFilters {
  trigger_id?: UUID
  status?: AutomationRunStatus
  target_type?: AutomationTargetType
  target_id?: UUID
  action_type?: AutomationActionType
  page?: number
  page_size?: number
}

export interface AutomationScheduleFormValues {
  name: string
  description: string
  frequency: ScheduleFrequency
  timezone: string
  start_at: string
  end_at: string
  next_run_at: string
  cron_expression: string
  is_active: boolean
}

export interface AutomationTriggerFormValues {
  name: string
  description: string
  status: AutomationStatus
  trigger_type: AutomationTriggerType
  action_type: AutomationActionType
  schedule_id: string
  conditionsJson: string
  actionConfigJson: string
}
