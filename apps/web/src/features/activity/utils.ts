import type { BadgeVariant } from '@/lib/designTokens'
import { ApiError } from '@/lib/apiClient'
import { formatLabel } from '@/lib/utils'

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

export function formatDateTime(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleString()
}

export function formatActorLabel(actorId: string | null): string {
  if (!actorId) {
    return 'System'
  }
  return `User ${actorId.slice(0, 8)}`
}

export function actionBadgeVariant(action: string): BadgeVariant {
  switch (action) {
    case 'created':
      return 'success'
    case 'updated':
      return 'info'
    case 'deleted':
      return 'danger'
    case 'commented':
      return 'neutral'
    case 'status_changed':
      return 'warning'
    case 'assigned':
      return 'teal'
    case 'linked':
      return 'info'
    case 'unlinked':
      return 'neutral'
    default:
      return 'neutral'
  }
}

export function formatActionLabel(action: string): string {
  return formatLabel(action)
}
