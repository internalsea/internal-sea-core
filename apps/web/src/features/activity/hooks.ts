import { useQuery } from '@tanstack/react-query'

import { getActivity, getEntityActivity } from '@/features/activity/api'
import type { ActivityFilters } from '@/features/activity/types'

export const activityKeys = {
  all: ['activity'] as const,
  lists: () => [...activityKeys.all, 'list'] as const,
  list: (filters: ActivityFilters) => [...activityKeys.lists(), filters] as const,
  entities: () => [...activityKeys.all, 'entity'] as const,
  entity: (entityType: string, entityId: string) =>
    [...activityKeys.entities(), entityType, entityId] as const,
}

export function useEntityActivity(entityType: string, entityId: string | undefined) {
  return useQuery({
    queryKey: activityKeys.entity(entityType, entityId ?? ''),
    queryFn: () => getEntityActivity(entityType, entityId!),
    enabled: Boolean(entityId),
  })
}

export function useActivity(filters: ActivityFilters = {}) {
  return useQuery({
    queryKey: activityKeys.list(filters),
    queryFn: () => getActivity(filters),
  })
}
