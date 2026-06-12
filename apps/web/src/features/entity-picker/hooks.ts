import { useQuery } from '@tanstack/react-query'

import { getEntityReference, searchEntities } from '@/features/entity-picker/api'
import type { EntityPickerType } from '@/features/entity-picker/types'

const STALE_TIME_MS = 30_000

export function entitySearchKey(query: string, allowedTypes: EntityPickerType[]) {
  return ['entity-search', query, [...allowedTypes].sort().join(',')] as const
}

export function entityReferenceKey(entityType: EntityPickerType, entityId: string) {
  return ['entity-reference', entityType, entityId] as const
}

export function useEntitySearch(query: string, allowedTypes: EntityPickerType[], enabled: boolean) {
  const trimmed = query.trim()
  const shouldSearch = enabled && trimmed.length >= 2 && allowedTypes.length > 0

  return useQuery({
    queryKey: entitySearchKey(trimmed, allowedTypes),
    queryFn: () => searchEntities(trimmed, allowedTypes),
    enabled: shouldSearch,
    staleTime: STALE_TIME_MS,
  })
}

export function useEntityReference(
  entityType: EntityPickerType,
  entityId: string,
  enabled = true,
) {
  return useQuery({
    queryKey: entityReferenceKey(entityType, entityId),
    queryFn: () => getEntityReference(entityType, entityId),
    enabled: enabled && Boolean(entityId),
    staleTime: STALE_TIME_MS,
    retry: false,
  })
}
