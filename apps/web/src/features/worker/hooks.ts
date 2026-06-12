import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { automationKeys } from '@/features/automation/hooks'
import { notificationKeys } from '@/features/notifications/hooks'
import { getDueWorkSummary, getWorkerStatus, runWorkerOnce } from '@/features/worker/api'

export const workerKeys = {
  all: ['worker'] as const,
  status: () => [...workerKeys.all, 'status'] as const,
  dueWork: () => [...workerKeys.all, 'due-work'] as const,
}

export function useWorkerStatus() {
  return useQuery({
    queryKey: workerKeys.status(),
    queryFn: getWorkerStatus,
    refetchInterval: 30_000,
  })
}

export function useDueWorkSummary() {
  return useQuery({
    queryKey: workerKeys.dueWork(),
    queryFn: getDueWorkSummary,
    refetchInterval: 30_000,
  })
}

export function useRunWorkerOnce() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: runWorkerOnce,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: workerKeys.all })
      void queryClient.invalidateQueries({ queryKey: automationKeys.all })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.all })
    },
  })
}
