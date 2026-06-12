import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createPerson,
  deactivatePerson,
  getPerson,
  getPeople,
  getPersonSummary,
  updatePerson,
} from '@/features/people/api'
import type {
  PersonCreateInput,
  PersonFilters,
  PersonUpdateInput,
} from '@/features/people/types'

export const peopleKeys = {
  all: ['people'] as const,
  lists: () => [...peopleKeys.all, 'list'] as const,
  list: (filters: PersonFilters) => [...peopleKeys.lists(), filters] as const,
  details: () => [...peopleKeys.all, 'detail'] as const,
  detail: (id: string) => [...peopleKeys.details(), id] as const,
  summary: (id: string) => [...peopleKeys.all, 'summary', id] as const,
}

export function usePeople(filters: PersonFilters) {
  return useQuery({
    queryKey: peopleKeys.list(filters),
    queryFn: () => getPeople(filters),
  })
}

export function usePerson(id: string | undefined) {
  return useQuery({
    queryKey: peopleKeys.detail(id ?? ''),
    queryFn: () => getPerson(id!),
    enabled: Boolean(id),
  })
}

export function usePersonSummary(id: string | undefined) {
  return useQuery({
    queryKey: peopleKeys.summary(id ?? ''),
    queryFn: () => getPersonSummary(id!),
    enabled: Boolean(id),
  })
}

export function useCreatePerson() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: PersonCreateInput) => createPerson(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: peopleKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: peopleKeys.all })
    },
  })
}

export function useUpdatePerson() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: PersonUpdateInput }) =>
      updatePerson(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: peopleKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: peopleKeys.all })
      void queryClient.invalidateQueries({ queryKey: peopleKeys.detail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: peopleKeys.summary(variables.id) })
    },
  })
}

export function useDeactivatePerson() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => deactivatePerson(id),
    onSuccess: (_data, id) => {
      void queryClient.invalidateQueries({ queryKey: peopleKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: peopleKeys.all })
      void queryClient.invalidateQueries({ queryKey: peopleKeys.detail(id) })
      void queryClient.invalidateQueries({ queryKey: peopleKeys.summary(id) })
    },
  })
}
