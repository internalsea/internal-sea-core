import type { DataProduct } from '@/features/data-products/types'
import { ApiError } from '@/lib/apiClient'

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    const detail = error.body?.detail
    if (typeof detail === 'string') {
      return detail
    }
    return `Request failed (${error.status})`
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'Something went wrong.'
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

export function dataProductToFormValues(product: DataProduct) {
  return {
    name: product.name,
    description: product.description ?? '',
    type: product.type,
    status: product.status,
    quality_status: product.quality_status,
    business_domain_id: product.business_domain_id ?? '',
    business_owner_id: product.business_owner_id ?? undefined,
    technical_owner_id: product.technical_owner_id ?? undefined,
    capability_id: product.capability_id ?? undefined,
    team_id: product.team_id ?? undefined,
    refresh_frequency: product.refresh_frequency ?? '',
    source_systems: product.source_systems ?? '',
    consumers: product.consumers ?? '',
    documentation_url: product.documentation_url ?? '',
  }
}
