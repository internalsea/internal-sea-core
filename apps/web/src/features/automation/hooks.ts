import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createAutomationSchedule,
  createAutomationTrigger,
  deleteAutomationSchedule,
  deleteAutomationTrigger,
  getAutomationOverview,
  getAutomationRuns,
  getAutomationSchedule,
  getAutomationSchedules,
  getAutomationTrigger,
  getAutomationTriggers,
  getEntityAutomations,
  getTriggerRuns,
  runAutomationTrigger,
  updateAutomationSchedule,
  updateAutomationTrigger,
} from '@/features/automation/api'
import type {
  AutomationRunFilters,
  AutomationRunRequest,
  AutomationScheduleCreateInput,
  AutomationScheduleFilters,
  AutomationScheduleUpdateInput,
  AutomationTargetType,
  AutomationTriggerCreateInput,
  AutomationTriggerFilters,
  AutomationTriggerUpdateInput,
} from '@/features/automation/types'
import type { UUID } from '@/types/common'

export const automationKeys = {
  all: ['automation'] as const,
  overview: () => [...automationKeys.all, 'overview'] as const,
  schedules: () => [...automationKeys.all, 'schedules'] as const,
  scheduleList: (filters: AutomationScheduleFilters) =>
    [...automationKeys.schedules(), 'list', filters] as const,
  scheduleDetail: (id: string) => [...automationKeys.schedules(), 'detail', id] as const,
  triggers: () => [...automationKeys.all, 'triggers'] as const,
  triggerList: (filters: AutomationTriggerFilters) =>
    [...automationKeys.triggers(), 'list', filters] as const,
  triggerDetail: (id: string) => [...automationKeys.triggers(), 'detail', id] as const,
  runs: () => [...automationKeys.all, 'runs'] as const,
  runList: (filters: AutomationRunFilters) => [...automationKeys.runs(), 'list', filters] as const,
  triggerRuns: (triggerId: string) => [...automationKeys.runs(), 'trigger', triggerId] as const,
  entity: (targetType: AutomationTargetType, targetId: string) =>
    [...automationKeys.all, 'entity', targetType, targetId] as const,
}

export function useAutomationOverview() {
  return useQuery({
    queryKey: automationKeys.overview(),
    queryFn: getAutomationOverview,
  })
}

export function useAutomationSchedules(filters: AutomationScheduleFilters) {
  return useQuery({
    queryKey: automationKeys.scheduleList(filters),
    queryFn: () => getAutomationSchedules(filters),
  })
}

export function useAutomationSchedule(id: string | undefined) {
  return useQuery({
    queryKey: automationKeys.scheduleDetail(id ?? ''),
    queryFn: () => getAutomationSchedule(id!),
    enabled: Boolean(id),
  })
}

export function useCreateAutomationSchedule() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: AutomationScheduleCreateInput) => createAutomationSchedule(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: automationKeys.schedules() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggers() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.overview() })
    },
  })
}

export function useUpdateAutomationSchedule() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: UUID; payload: AutomationScheduleUpdateInput }) =>
      updateAutomationSchedule(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: automationKeys.schedules() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.scheduleDetail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggers() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.overview() })
    },
  })
}

export function useDeleteAutomationSchedule() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: UUID) => deleteAutomationSchedule(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: automationKeys.schedules() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggers() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.overview() })
    },
  })
}

export function useAutomationTriggers(filters: AutomationTriggerFilters) {
  return useQuery({
    queryKey: automationKeys.triggerList(filters),
    queryFn: () => getAutomationTriggers(filters),
  })
}

export function useAutomationTrigger(id: string | undefined) {
  return useQuery({
    queryKey: automationKeys.triggerDetail(id ?? ''),
    queryFn: () => getAutomationTrigger(id!),
    enabled: Boolean(id),
  })
}

export function useCreateAutomationTrigger() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: AutomationTriggerCreateInput) => createAutomationTrigger(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggers() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.all })
      void queryClient.invalidateQueries({ queryKey: automationKeys.overview() })
    },
  })
}

export function useUpdateAutomationTrigger() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: UUID; payload: AutomationTriggerUpdateInput }) =>
      updateAutomationTrigger(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggers() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggerDetail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: automationKeys.all })
      void queryClient.invalidateQueries({ queryKey: automationKeys.overview() })
    },
  })
}

export function useDeleteAutomationTrigger() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: UUID) => deleteAutomationTrigger(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggers() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.all })
      void queryClient.invalidateQueries({ queryKey: automationKeys.overview() })
    },
  })
}

export function useAutomationRuns(filters: AutomationRunFilters) {
  return useQuery({
    queryKey: automationKeys.runList(filters),
    queryFn: () => getAutomationRuns(filters),
  })
}

export function useTriggerRuns(triggerId: string | undefined) {
  return useQuery({
    queryKey: automationKeys.triggerRuns(triggerId ?? ''),
    queryFn: () => getTriggerRuns(triggerId!),
    enabled: Boolean(triggerId),
  })
}

export function useRunAutomationTrigger(triggerId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: AutomationRunRequest) => runAutomationTrigger(triggerId, payload),
    onSuccess: (result) => {
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggerDetail(triggerId) })
      void queryClient.invalidateQueries({ queryKey: automationKeys.triggerRuns(triggerId) })
      void queryClient.invalidateQueries({ queryKey: automationKeys.runs() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.overview() })
      void queryClient.invalidateQueries({ queryKey: automationKeys.all })
      if (result.created_work_item_id) {
        void queryClient.invalidateQueries({ queryKey: ['work-items'] })
      }
      if (result.created_comment_id) {
        void queryClient.invalidateQueries({ queryKey: ['comments'] })
      }
      if (result.created_activity_event_id) {
        void queryClient.invalidateQueries({ queryKey: ['activity'] })
      }
    },
  })
}

export function useEntityAutomations(targetType: AutomationTargetType, targetId: string) {
  return useQuery({
    queryKey: automationKeys.entity(targetType, targetId),
    queryFn: () => getEntityAutomations(targetType, targetId),
    enabled: Boolean(targetId),
  })
}
