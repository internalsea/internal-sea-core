import type { BadgeVariant } from '@/lib/designTokens'
import type {
  AutomationActionType,
  AutomationRunStatus,
  AutomationStatus,
  AutomationTargetType,
  AutomationTriggerType,
  ScheduleFrequency,
} from '@/features/automation/types'

export interface SelectOption<T extends string = string> {
  value: T
  label: string
}

export const AUTOMATION_TARGET_TYPES: SelectOption<AutomationTargetType>[] = [
  { value: 'data_product', label: 'Data Product' },
  { value: 'project', label: 'Project' },
  { value: 'internal_project', label: 'Internal Project' },
  { value: 'compliance_check', label: 'Compliance Check' },
  { value: 'team', label: 'Team' },
  { value: 'capability', label: 'Capability' },
  { value: 'work_item', label: 'Work Item' },
]

export const AUTOMATION_TRIGGER_TYPES: SelectOption<AutomationTriggerType>[] = [
  { value: 'schedule', label: 'Schedule' },
  { value: 'status_change', label: 'Status Change' },
  { value: 'due_date', label: 'Due Date' },
  { value: 'quality_status', label: 'Quality Status' },
  { value: 'compliance_status', label: 'Compliance Status' },
  { value: 'manual', label: 'Manual' },
]

export const AUTOMATION_ACTION_TYPES: SelectOption<AutomationActionType>[] = [
  { value: 'create_work_item', label: 'Create Work Item' },
  { value: 'create_compliance_check', label: 'Create Compliance Check' },
  { value: 'add_comment', label: 'Add Comment' },
  { value: 'create_activity_event', label: 'Create Activity Event' },
  { value: 'send_notification', label: 'Send Notification' },
  { value: 'run_quality_check', label: 'Run Quality Check' },
  { value: 'run_compliance_check', label: 'Run Compliance Check' },
  { value: 'call_webhook', label: 'Call Webhook' },
  { value: 'call_ai_tool', label: 'Call AI Tool' },
]

export const AUTOMATION_STATUSES: SelectOption<AutomationStatus>[] = [
  { value: 'draft', label: 'Draft' },
  { value: 'active', label: 'Active' },
  { value: 'paused', label: 'Paused' },
  { value: 'archived', label: 'Archived' },
]

export const AUTOMATION_RUN_STATUSES: SelectOption<AutomationRunStatus>[] = [
  { value: 'pending', label: 'Pending' },
  { value: 'running', label: 'Running' },
  { value: 'succeeded', label: 'Succeeded' },
  { value: 'failed', label: 'Failed' },
  { value: 'skipped', label: 'Skipped' },
  { value: 'simulated', label: 'Simulated' },
]

export const SCHEDULE_FREQUENCIES: SelectOption<ScheduleFrequency>[] = [
  { value: 'once', label: 'Once' },
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
  { value: 'quarterly', label: 'Quarterly' },
  { value: 'yearly', label: 'Yearly' },
  { value: 'custom', label: 'Custom' },
]

export const automationStatusBadgeVariant: Record<AutomationStatus, BadgeVariant> = {
  draft: 'neutral',
  active: 'success',
  paused: 'warning',
  archived: 'neutral',
}

export const automationRunStatusBadgeVariant: Record<AutomationRunStatus, BadgeVariant> = {
  pending: 'neutral',
  running: 'info',
  succeeded: 'success',
  failed: 'danger',
  skipped: 'warning',
  simulated: 'teal',
}

export const actionTypeBadgeVariant: Record<AutomationActionType, BadgeVariant> = {
  create_work_item: 'info',
  create_compliance_check: 'warning',
  add_comment: 'neutral',
  create_activity_event: 'teal',
  send_notification: 'warning',
  run_quality_check: 'info',
  run_compliance_check: 'warning',
  call_webhook: 'neutral',
  call_ai_tool: 'teal',
}

export const DEFAULT_PAGE_SIZE = 20

export const selectClassName =
  'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue disabled:cursor-not-allowed disabled:bg-app-muted disabled:text-gray-400'

export const MVP_ACTION_TYPES: AutomationActionType[] = [
  'create_work_item',
  'add_comment',
  'create_activity_event',
]

export const ACTION_CONFIG_EXAMPLES: Partial<Record<AutomationActionType, string>> = {
  create_work_item: JSON.stringify(
    {
      title: 'Review data product documentation',
      description: 'Monthly reminder to review ownership, documentation and quality status.',
      priority: 'medium',
      type: 'task',
      due_in_days: 7,
    },
    null,
    2,
  ),
  add_comment: JSON.stringify({ body: 'Monthly review reminder.' }, null, 2),
  create_activity_event: JSON.stringify(
    {
      title: 'Automated review reminder',
      description: 'Schedule reached for this object.',
    },
    null,
    2,
  ),
}
