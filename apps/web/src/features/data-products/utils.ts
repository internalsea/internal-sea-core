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
  return date.toLocaleString()
}
