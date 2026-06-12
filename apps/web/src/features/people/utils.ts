import type {
  Person,
  PersonCreateInput,
  PersonFormValues,
  PersonListItem,
  PersonUpdateInput,
  SeniorityLevel,
} from '@/features/people/types'

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

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

export function formatAvailability(value: number | null | undefined): string {
  if (value === null || value === undefined) {
    return 'Not set'
  }
  return `${value}%`
}

export function getPersonStatus(isActive: boolean): 'active' | 'inactive' {
  return isActive ? 'active' : 'inactive'
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

export function cleanPersonPayload(
  payload: PersonCreateInput | PersonUpdateInput,
): PersonCreateInput | PersonUpdateInput {
  const cleaned = { ...payload }

  const stringFields = ['email', 'role_title', 'location', 'seniority_level'] as const
  for (const field of stringFields) {
    if (field in cleaned && cleaned[field] === '') {
      cleaned[field] = null
    }
  }

  const uuidFields = ['user_id', 'team_id', 'capability_id'] as const
  for (const field of uuidFields) {
    if (field in cleaned) {
      cleaned[field] = emptyUuidToNull(cleaned[field] ?? undefined)
    }
  }

  if ('availability_percent' in cleaned) {
    if (cleaned.availability_percent === null || cleaned.availability_percent === undefined) {
      cleaned.availability_percent = null
    }
  }

  return cleaned
}

export function validateEmail(value: string): string | null {
  const trimmed = value.trim()
  if (!trimmed) {
    return null
  }
  if (!EMAIL_PATTERN.test(trimmed)) {
    return 'Enter a valid email address'
  }
  return null
}

export function personToFormValues(person: Person | PersonListItem): PersonFormValues {
  return {
    full_name: person.full_name,
    email: person.email ?? '',
    role_title: person.role_title ?? '',
    seniority_level: person.seniority_level ?? '',
    user_id: 'user_id' in person ? (person.user_id ?? '') : '',
    team_id: person.team_id ?? '',
    capability_id: person.capability_id ?? '',
    availability_percent:
      person.availability_percent === null || person.availability_percent === undefined
        ? ''
        : String(person.availability_percent),
    location: person.location ?? '',
    is_active: person.is_active,
  }
}

export function formValuesToPayload(values: PersonFormValues): PersonCreateInput {
  const availability =
    values.availability_percent.trim() === ''
      ? null
      : Number.parseInt(values.availability_percent, 10)

  return cleanPersonPayload({
    full_name: values.full_name.trim(),
    email: values.email.trim() || null,
    role_title: values.role_title.trim() || null,
    seniority_level: values.seniority_level
      ? (values.seniority_level as SeniorityLevel)
      : null,
    user_id: values.user_id,
    team_id: values.team_id,
    capability_id: values.capability_id,
    availability_percent: availability === null || Number.isNaN(availability) ? null : availability,
    location: values.location.trim() || null,
    is_active: values.is_active,
  }) as PersonCreateInput
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }
  return 'Request failed'
}
