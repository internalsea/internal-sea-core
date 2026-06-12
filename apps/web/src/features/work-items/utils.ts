import type {
  WorkItemCreateInput,
  WorkItemFormValues,
  WorkItemListItem,
  WorkItemStatus,
  WorkItemUpdateInput,
} from '@/features/work-items/types'

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

export function formatDate(value: string | null | undefined): string {
  if (!value) {
    return '—'
  }
  const date = new Date(value.includes('T') ? value : `${value}T00:00:00`)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return '—'
  }
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function truncateText(value: string | null | undefined, maxLength: number): string {
  if (!value) {
    return ''
  }
  if (value.length <= maxLength) {
    return value
  }
  return `${value.slice(0, maxLength).trim()}…`
}

function emptyToNull(value: string | null | undefined): string | null {
  if (value === undefined || value === null) {
    return null
  }
  const trimmed = value.trim()
  if (!trimmed) {
    return null
  }
  if (!UUID_PATTERN.test(trimmed)) {
    return null
  }
  return trimmed
}

export function cleanWorkItemPayload(
  payload: WorkItemCreateInput | WorkItemUpdateInput,
): WorkItemCreateInput | WorkItemUpdateInput {
  const cleaned = { ...payload }

  if ('description' in cleaned && cleaned.description === '') {
    cleaned.description = null
  }
  if ('assignee_id' in cleaned) {
    cleaned.assignee_id = emptyToNull(cleaned.assignee_id ?? undefined)
  }
  if ('reporter_id' in cleaned) {
    cleaned.reporter_id = emptyToNull(cleaned.reporter_id ?? undefined)
  }
  if ('data_product_id' in cleaned) {
    cleaned.data_product_id = emptyToNull(cleaned.data_product_id ?? undefined)
  }
  if ('project_id' in cleaned) {
    cleaned.project_id = emptyToNull(cleaned.project_id ?? undefined)
  }
  if ('capability_id' in cleaned) {
    cleaned.capability_id = emptyToNull(cleaned.capability_id ?? undefined)
  }
  if ('team_id' in cleaned) {
    cleaned.team_id = emptyToNull(cleaned.team_id ?? undefined)
  }
  if ('due_date' in cleaned && cleaned.due_date === '') {
    cleaned.due_date = null
  }
  if ('estimate_points' in cleaned) {
    if (cleaned.estimate_points === null || cleaned.estimate_points === undefined) {
      cleaned.estimate_points = null
    }
  }

  return cleaned
}

export function getNextWorkItemStatus(status: WorkItemStatus): WorkItemStatus | null {
  switch (status) {
    case 'backlog':
      return 'ready'
    case 'ready':
      return 'in_progress'
    case 'in_progress':
      return 'review'
    case 'review':
      return 'done'
    case 'done':
      return 'closed'
    default:
      return null
  }
}

export function isWorkItemOverdue(workItem: Pick<WorkItemListItem, 'due_date' | 'status'>): boolean {
  if (!workItem.due_date || workItem.status === 'done' || workItem.status === 'closed') {
    return false
  }
  const due = new Date(`${workItem.due_date}T23:59:59`)
  return due.getTime() < Date.now()
}

export function workItemToFormValues(workItem: WorkItemListItem): WorkItemFormValues {
  return {
    title: workItem.title,
    description: workItem.description ?? '',
    type: workItem.type,
    status: workItem.status,
    priority: workItem.priority,
    due_date: workItem.due_date ?? '',
    estimate_points:
      workItem.estimate_points === null || workItem.estimate_points === undefined
        ? ''
        : String(workItem.estimate_points),
    assignee_id: workItem.assignee_id ?? '',
    reporter_id: workItem.reporter_id ?? '',
    data_product_id: workItem.data_product_id ?? '',
    project_id: workItem.project_id ?? '',
    capability_id: workItem.capability_id ?? '',
    team_id: workItem.team_id ?? '',
  }
}

export function formValuesToPayload(values: WorkItemFormValues): WorkItemCreateInput {
  const estimate =
    values.estimate_points.trim() === '' ? null : Number.parseInt(values.estimate_points, 10)

  return cleanWorkItemPayload({
    title: values.title.trim(),
    description: values.description.trim() || null,
    type: values.type,
    status: values.status,
    priority: values.priority,
    due_date: values.due_date.trim() || null,
    estimate_points: Number.isNaN(estimate) ? null : estimate,
    assignee_id: values.assignee_id,
    reporter_id: values.reporter_id,
    data_product_id: values.data_product_id,
    project_id: values.project_id,
    capability_id: values.capability_id,
    team_id: values.team_id,
  }) as WorkItemCreateInput
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }
  return 'Request failed'
}
