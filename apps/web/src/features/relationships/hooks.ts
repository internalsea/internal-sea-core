import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { activityKeys } from '@/features/activity/hooks'
import {
  createRelationship,
  deleteRelationship,
  getEntityRelationships,
  updateRelationship,
} from '@/features/relationships/api'
import type {
  EntityLinkCreateInput,
  EntityLinkUpdateInput,
  EntityType,
} from '@/features/relationships/types'

export const relationshipKeys = {
  all: ['relationships'] as const,
  views: () => [...relationshipKeys.all, 'view'] as const,
  view: (entityType: EntityType, entityId: string) =>
    [...relationshipKeys.views(), entityType, entityId] as const,
}

export function useEntityRelationships(entityType: EntityType, entityId: string | undefined) {
  return useQuery({
    queryKey: relationshipKeys.view(entityType, entityId ?? ''),
    queryFn: () => getEntityRelationships(entityType, entityId!),
    enabled: Boolean(entityId),
  })
}

export function useCreateRelationship(entityType: EntityType, entityId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: EntityLinkCreateInput) => createRelationship(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: relationshipKeys.view(entityType, entityId),
      })
      void queryClient.invalidateQueries({ queryKey: relationshipKeys.views() })
      void queryClient.invalidateQueries({
        queryKey: activityKeys.entity(entityType, entityId),
      })
    },
  })
}

export function useUpdateRelationship(entityType: EntityType, entityId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ linkId, payload }: { linkId: string; payload: EntityLinkUpdateInput }) =>
      updateRelationship(linkId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: relationshipKeys.view(entityType, entityId),
      })
      void queryClient.invalidateQueries({ queryKey: relationshipKeys.views() })
    },
  })
}

export function useDeleteRelationship(entityType: EntityType, entityId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (linkId: string) => deleteRelationship(linkId),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: relationshipKeys.view(entityType, entityId),
      })
      void queryClient.invalidateQueries({ queryKey: relationshipKeys.views() })
      void queryClient.invalidateQueries({
        queryKey: activityKeys.entity(entityType, entityId),
      })
    },
  })
}
