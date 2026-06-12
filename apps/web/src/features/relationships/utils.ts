import { ApiError } from '@/lib/apiClient'
import type { EntityLinkCreateInput, EntityType } from '@/features/relationships/types'

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

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

export function getEntityHref(entityType: EntityType, entityId: string): string | null {
  switch (entityType) {
    case 'data_product':
      return `/data-products/${entityId}`
    case 'work_item':
      return `/work-items/${entityId}`
    case 'project':
      return `/projects/${entityId}`
    case 'internal_project':
      return `/internal-projects/${entityId}`
    case 'person':
      return `/people/${entityId}`
    case 'team':
      return `/teams/${entityId}`
    case 'capability':
      return `/capabilities/${entityId}`
    default:
      return null
  }
}

export function formatEntityType(entityType: string): string {
  return entityType.replace(/_/g, ' ')
}

export function formatLinkType(linkType: string): string {
  return linkType.replace(/_/g, ' ')
}

export function shortId(id: string): string {
  return id.length > 8 ? `${id.slice(0, 8)}…` : id
}

export function isValidUuid(value: string): boolean {
  return UUID_PATTERN.test(value.trim())
}

export function isSameEntity(
  sourceType: EntityType,
  sourceId: string,
  targetType: EntityType,
  targetId: string,
): boolean {
  return sourceType === targetType && sourceId === targetId
}

export function cleanRelationshipPayload(
  payload: EntityLinkCreateInput,
): EntityLinkCreateInput {
  return {
    ...payload,
    title: payload.title?.trim() || null,
    description: payload.description?.trim() || null,
  }
}

export function formatDateTime(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleString()
}
