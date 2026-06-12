import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createTeam,
  deleteTeam,
  getTeam,
  getTeams,
  getTeamSummary,
  updateTeam,
} from '@/features/teams/api'
import type { TeamCreateInput, TeamFilters, TeamUpdateInput } from '@/features/teams/types'

export const teamKeys = {
  all: ['teams'] as const,
  lists: () => [...teamKeys.all, 'list'] as const,
  list: (filters: TeamFilters) => [...teamKeys.lists(), filters] as const,
  details: () => [...teamKeys.all, 'detail'] as const,
  detail: (id: string) => [...teamKeys.details(), id] as const,
  summary: (id: string) => [...teamKeys.all, 'summary', id] as const,
}

export function useTeams(filters: TeamFilters) {
  return useQuery({
    queryKey: teamKeys.list(filters),
    queryFn: () => getTeams(filters),
  })
}

export function useTeam(id: string | undefined) {
  return useQuery({
    queryKey: teamKeys.detail(id ?? ''),
    queryFn: () => getTeam(id!),
    enabled: Boolean(id),
  })
}

export function useTeamSummary(id: string | undefined) {
  return useQuery({
    queryKey: teamKeys.summary(id ?? ''),
    queryFn: () => getTeamSummary(id!),
    enabled: Boolean(id),
  })
}

export function useCreateTeam() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: TeamCreateInput) => createTeam(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: teamKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: teamKeys.all })
    },
  })
}

export function useUpdateTeam() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: TeamUpdateInput }) =>
      updateTeam(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: teamKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: teamKeys.all })
      void queryClient.invalidateQueries({ queryKey: teamKeys.detail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: teamKeys.summary(variables.id) })
    },
  })
}

export function useDeleteTeam() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => deleteTeam(id),
    onSuccess: (_data, id) => {
      void queryClient.invalidateQueries({ queryKey: teamKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: teamKeys.all })
      void queryClient.invalidateQueries({ queryKey: teamKeys.detail(id) })
      void queryClient.invalidateQueries({ queryKey: teamKeys.summary(id) })
    },
  })
}
