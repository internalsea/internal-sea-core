import type {
  Capability,
  CapabilityCreateInput,
  CapabilityFormValues,
  CapabilityListItem,
  CapabilityUpdateInput,
} from '@/features/capabilities/types'

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

export function cleanCapabilityPayload(
  payload: CapabilityCreateInput | CapabilityUpdateInput,
): CapabilityCreateInput | CapabilityUpdateInput {
  const cleaned = { ...payload }
  if ('description' in cleaned && cleaned.description === '') {
    cleaned.description = null
  }
  return cleaned
}

export function capabilityToFormValues(capability: Capability | CapabilityListItem): CapabilityFormValues {
  return {
    name: capability.name,
    description: capability.description ?? '',
  }
}

export function formValuesToPayload(values: CapabilityFormValues): CapabilityCreateInput {
  return cleanCapabilityPayload({
    name: values.name.trim(),
    description: values.description.trim() || null,
  }) as CapabilityCreateInput
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }
  return 'Request failed'
}
