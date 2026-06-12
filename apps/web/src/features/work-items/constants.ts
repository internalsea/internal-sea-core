import type { WorkItemPriority, WorkItemStatus, WorkItemType } from '@/features/work-items/types'

export interface SelectOption<T extends string = string> {
  value: T
  label: string
}

export const WORK_ITEM_TYPES: SelectOption<WorkItemType>[] = [
  { value: 'epic', label: 'Epic' },
  { value: 'story', label: 'Story' },
  { value: 'task', label: 'Task' },
  { value: 'bug', label: 'Bug' },
  { value: 'risk', label: 'Risk' },
  { value: 'decision', label: 'Decision' },
  { value: 'technical_debt', label: 'Technical Debt' },
  { value: 'improvement', label: 'Improvement' },
  { value: 'support_request', label: 'Support Request' },
]

export const WORK_ITEM_STATUSES: SelectOption<WorkItemStatus>[] = [
  { value: 'backlog', label: 'Backlog' },
  { value: 'ready', label: 'Ready' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'review', label: 'Review' },
  { value: 'done', label: 'Done' },
  { value: 'closed', label: 'Closed' },
]

export const WORK_ITEM_PRIORITIES: SelectOption<WorkItemPriority>[] = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
  { value: 'critical', label: 'Critical' },
]

export const BOARD_STATUSES: WorkItemStatus[] = [
  'backlog',
  'ready',
  'in_progress',
  'review',
  'done',
]

export const workItemTypeLabels: Record<WorkItemType, string> = Object.fromEntries(
  WORK_ITEM_TYPES.map((item) => [item.value, item.label]),
) as Record<WorkItemType, string>

export const workItemStatusLabels: Record<WorkItemStatus, string> = Object.fromEntries(
  WORK_ITEM_STATUSES.map((item) => [item.value, item.label]),
) as Record<WorkItemStatus, string>

export const workItemPriorityLabels: Record<WorkItemPriority, string> = Object.fromEntries(
  WORK_ITEM_PRIORITIES.map((item) => [item.value, item.label]),
) as Record<WorkItemPriority, string>

export const DEFAULT_PAGE_SIZE = 20

export const selectClassName =
  'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue disabled:cursor-not-allowed disabled:bg-app-muted disabled:text-gray-400'
