import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createWorkItem,
  deleteWorkItem,
  getWorkItem,
  getWorkItemBoard,
  getWorkItems,
  updateWorkItem,
  updateWorkItemStatus,
} from '@/features/work-items/api'
import type {
  WorkItemCreateInput,
  WorkItemFilters,
  WorkItemStatus,
  WorkItemUpdateInput,
} from '@/features/work-items/types'

export const workItemKeys = {
  all: ['work-items'] as const,
  lists: () => [...workItemKeys.all, 'list'] as const,
  list: (filters: WorkItemFilters) => [...workItemKeys.lists(), filters] as const,
  board: (filters: WorkItemFilters) => [...workItemKeys.all, 'board', filters] as const,
  details: () => [...workItemKeys.all, 'detail'] as const,
  detail: (id: string) => [...workItemKeys.details(), id] as const,
}

export function useWorkItems(filters: WorkItemFilters) {
  return useQuery({
    queryKey: workItemKeys.list(filters),
    queryFn: () => getWorkItems(filters),
  })
}

export function useWorkItem(id: string | undefined) {
  return useQuery({
    queryKey: workItemKeys.detail(id ?? ''),
    queryFn: () => getWorkItem(id!),
    enabled: Boolean(id),
  })
}

export function useWorkItemBoard(filters: WorkItemFilters) {
  return useQuery({
    queryKey: workItemKeys.board(filters),
    queryFn: () => getWorkItemBoard(filters),
  })
}

export function useCreateWorkItem() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: WorkItemCreateInput) => createWorkItem(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: workItemKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: workItemKeys.all })
    },
  })
}

export function useUpdateWorkItem() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: WorkItemUpdateInput }) =>
      updateWorkItem(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: workItemKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: workItemKeys.all })
      void queryClient.invalidateQueries({ queryKey: workItemKeys.detail(variables.id) })
    },
  })
}

export function useDeleteWorkItem() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => deleteWorkItem(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: workItemKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: workItemKeys.all })
    },
  })
}

export function useUpdateWorkItemStatus() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: WorkItemStatus }) =>
      updateWorkItemStatus(id, status),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: workItemKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: workItemKeys.all })
      void queryClient.invalidateQueries({ queryKey: workItemKeys.detail(variables.id) })
    },
  })
}
