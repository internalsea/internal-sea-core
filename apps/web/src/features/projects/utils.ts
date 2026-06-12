import type {
  Project,
  ProjectCreateInput,
  ProjectFormValues,
  ProjectListItem,
  ProjectUpdateInput,
  ProjectVariant,
} from '@/features/projects/types'

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

export function formatCurrency(
  amount: string | number | null | undefined,
  currency: string | null | undefined,
): string {
  if (amount === null || amount === undefined || amount === '') {
    return '—'
  }
  const numeric = typeof amount === 'string' ? Number.parseFloat(amount) : amount
  if (Number.isNaN(numeric)) {
    return String(amount)
  }
  const code = currency?.trim() || 'EUR'
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency: code,
    }).format(numeric)
  } catch {
    return `${numeric} ${code}`
  }
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

function emptyStringToNull(value: string | null | undefined): string | null {
  if (value === undefined || value === null) {
    return null
  }
  const trimmed = value.trim()
  return trimmed ? trimmed : null
}

function emptyUuidToNull(value: string | null | undefined): string | null {
  const trimmed = emptyStringToNull(value)
  if (!trimmed) {
    return null
  }
  if (!UUID_PATTERN.test(trimmed)) {
    return null
  }
  return trimmed
}

export function cleanProjectPayload(
  payload: ProjectCreateInput | ProjectUpdateInput,
  variant?: ProjectVariant,
): ProjectCreateInput | ProjectUpdateInput {
  const cleaned = { ...payload }

  const stringFields = [
    'description',
    'client_name',
    'account_name',
    'priority',
    'health_status',
    'delivery_notes',
    'budget_currency',
    'start_date',
    'target_end_date',
    'actual_end_date',
  ] as const

  for (const field of stringFields) {
    if (field in cleaned && cleaned[field] === '') {
      cleaned[field] = null
    }
  }

  const uuidFields = ['owner_id', 'team_id', 'capability_id'] as const
  for (const field of uuidFields) {
    if (field in cleaned) {
      cleaned[field] = emptyUuidToNull(cleaned[field] ?? undefined)
    }
  }

  if ('budget_amount' in cleaned) {
    if (cleaned.budget_amount === '' || cleaned.budget_amount === null || cleaned.budget_amount === undefined) {
      cleaned.budget_amount = null
    }
  }

  if (variant === 'internal-projects') {
    cleaned.project_type = 'internal_project'
  }

  return cleaned
}

export function isProjectOverdue(
  project: Pick<ProjectListItem | Project, 'target_end_date' | 'status'>,
): boolean {
  if (!project.target_end_date) {
    return false
  }
  if (project.status === 'completed' || project.status === 'cancelled' || project.status === 'archived') {
    return false
  }
  const due = new Date(`${project.target_end_date}T23:59:59`)
  return due.getTime() < Date.now()
}

export function getProjectTimelineLabel(
  project: Pick<ProjectListItem | Project, 'start_date' | 'target_end_date'>,
): string {
  if (!project.start_date && !project.target_end_date) {
    return 'Not planned'
  }
  if (project.start_date && project.target_end_date) {
    return `${formatDate(project.start_date)} → ${formatDate(project.target_end_date)}`
  }
  if (project.start_date) {
    return `${formatDate(project.start_date)} → —`
  }
  return `— → ${formatDate(project.target_end_date)}`
}

export function projectToFormValues(project: Project): ProjectFormValues {
  return {
    name: project.name,
    description: project.description ?? '',
    project_type: project.project_type,
    status: project.status,
    health_status: project.health_status ?? '',
    priority: project.priority ?? '',
    client_name: project.client_name ?? '',
    account_name: project.account_name ?? '',
    start_date: project.start_date ?? '',
    target_end_date: project.target_end_date ?? '',
    actual_end_date: project.actual_end_date ?? '',
    budget_amount:
      project.budget_amount === null || project.budget_amount === undefined
        ? ''
        : String(project.budget_amount),
    budget_currency: project.budget_currency ?? '',
    owner_id: project.owner_id ?? '',
    team_id: project.team_id ?? '',
    capability_id: project.capability_id ?? '',
    delivery_notes: project.delivery_notes ?? '',
  }
}

export function formValuesToPayload(
  values: ProjectFormValues,
  variant?: ProjectVariant,
): ProjectCreateInput {
  const budget =
    values.budget_amount.trim() === '' ? null : Number.parseFloat(values.budget_amount)

  return cleanProjectPayload(
    {
      name: values.name.trim(),
      description: values.description.trim() || null,
      project_type: values.project_type,
      status: values.status,
      health_status: values.health_status.trim() || null,
      priority: values.priority.trim() || null,
      client_name: values.client_name.trim() || null,
      account_name: values.account_name.trim() || null,
      start_date: values.start_date.trim() || null,
      target_end_date: values.target_end_date.trim() || null,
      actual_end_date: values.actual_end_date.trim() || null,
      budget_amount: budget === null || Number.isNaN(budget) ? null : budget,
      budget_currency: values.budget_currency.trim() || null,
      owner_id: values.owner_id,
      team_id: values.team_id,
      capability_id: values.capability_id,
      delivery_notes: values.delivery_notes.trim() || null,
    },
    variant,
  ) as ProjectCreateInput
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }
  return 'Request failed'
}
