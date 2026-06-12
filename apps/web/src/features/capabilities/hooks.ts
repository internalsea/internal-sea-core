import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createCapability,
  deleteCapability,
  getCapability,
  getCapabilities,
  getCapabilitySummary,
  updateCapability,
} from '@/features/capabilities/api'
import type {
  CapabilityCreateInput,
  CapabilityFilters,
  CapabilityUpdateInput,
} from '@/features/capabilities/types'

export const capabilityKeys = {
  all: ['capabilities'] as const,
  lists: () => [...capabilityKeys.all, 'list'] as const,
  list: (filters: CapabilityFilters) => [...capabilityKeys.lists(), filters] as const,
  details: () => [...capabilityKeys.all, 'detail'] as const,
  detail: (id: string) => [...capabilityKeys.details(), id] as const,
  summary: (id: string) => [...capabilityKeys.all, 'summary', id] as const,
}

export function useCapabilities(filters: CapabilityFilters) {
  return useQuery({
    queryKey: capabilityKeys.list(filters),
    queryFn: () => getCapabilities(filters),
  })
}

export function useCapability(id: string | undefined) {
  return useQuery({
    queryKey: capabilityKeys.detail(id ?? ''),
    queryFn: () => getCapability(id!),
    enabled: Boolean(id),
  })
}

export function useCapabilitySummary(id: string | undefined) {
  return useQuery({
    queryKey: capabilityKeys.summary(id ?? ''),
    queryFn: () => getCapabilitySummary(id!),
    enabled: Boolean(id),
  })
}

export function useCreateCapability() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: CapabilityCreateInput) => createCapability(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.all })
    },
  })
}

export function useUpdateCapability() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: CapabilityUpdateInput }) =>
      updateCapability(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.all })
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.detail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.summary(variables.id) })
    },
  })
}

export function useDeleteCapability() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => deleteCapability(id),
    onSuccess: (_data, id) => {
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.all })
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.detail(id) })
      void queryClient.invalidateQueries({ queryKey: capabilityKeys.summary(id) })
    },
  })
}
