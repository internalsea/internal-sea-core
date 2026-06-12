import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  EntityLink,
  EntityLinkCreateInput,
  EntityLinkListResponse,
  EntityLinkUpdateInput,
  EntityRelationshipView,
  EntityType,
  RelationshipFilters,
} from '@/features/relationships/types'

export function getRelationships(filters?: RelationshipFilters): Promise<EntityLinkListResponse> {
  return apiGet<EntityLinkListResponse>(
    '/relationships',
    filters as Record<string, string | number | boolean | undefined> | undefined,
  )
}

export function getRelationship(linkId: string): Promise<EntityLink> {
  return apiGet<EntityLink>(`/relationships/${linkId}`)
}

export function getEntityRelationships(
  entityType: EntityType,
  entityId: string,
): Promise<EntityRelationshipView> {
  return apiGet<EntityRelationshipView>(`/relationships/entity/${entityType}/${entityId}`)
}

export function createRelationship(payload: EntityLinkCreateInput): Promise<EntityLink> {
  return apiPost<EntityLink>('/relationships', payload)
}

export function updateRelationship(
  linkId: string,
  payload: EntityLinkUpdateInput,
): Promise<EntityLink> {
  return apiPatch<EntityLink>(`/relationships/${linkId}`, payload)
}

export function deleteRelationship(linkId: string): Promise<void> {
  return apiDelete(`/relationships/${linkId}`)
}
