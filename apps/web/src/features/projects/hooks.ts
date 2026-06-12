import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createInternalProject,
  createProject,
  deleteInternalProject,
  deleteProject,
  getInternalProject,
  getInternalProjects,
  getProject,
  getProjects,
  getProjectSummary,
  updateInternalProject,
  updateProject,
} from '@/features/projects/api'
import type {
  ProjectCreateInput,
  ProjectFilters,
  ProjectUpdateInput,
} from '@/features/projects/types'

export const projectKeys = {
  all: ['projects'] as const,
  lists: () => [...projectKeys.all, 'list'] as const,
  list: (filters: ProjectFilters) => [...projectKeys.lists(), filters] as const,
  details: () => [...projectKeys.all, 'detail'] as const,
  detail: (id: string) => [...projectKeys.details(), id] as const,
  summary: (id: string) => [...projectKeys.all, 'summary', id] as const,
}

export const internalProjectKeys = {
  all: ['internal-projects'] as const,
  lists: () => [...internalProjectKeys.all, 'list'] as const,
  list: (filters: ProjectFilters) => [...internalProjectKeys.lists(), filters] as const,
  details: () => [...internalProjectKeys.all, 'detail'] as const,
  detail: (id: string) => [...internalProjectKeys.details(), id] as const,
}

export function useProjects(filters: ProjectFilters) {
  return useQuery({
    queryKey: projectKeys.list(filters),
    queryFn: () => getProjects(filters),
  })
}

export function useProject(id: string | undefined) {
  return useQuery({
    queryKey: projectKeys.detail(id ?? ''),
    queryFn: () => getProject(id!),
    enabled: Boolean(id),
  })
}

export function useProjectSummary(id: string | undefined) {
  return useQuery({
    queryKey: projectKeys.summary(id ?? ''),
    queryFn: () => getProjectSummary(id!),
    enabled: Boolean(id),
  })
}

export function useCreateProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: ProjectCreateInput) => createProject(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: projectKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: projectKeys.all })
    },
  })
}

export function useUpdateProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: ProjectUpdateInput }) =>
      updateProject(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: projectKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: projectKeys.all })
      void queryClient.invalidateQueries({ queryKey: projectKeys.detail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: projectKeys.summary(variables.id) })
    },
  })
}

export function useDeleteProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => deleteProject(id),
    onSuccess: (_data, id) => {
      void queryClient.invalidateQueries({ queryKey: projectKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: projectKeys.all })
      void queryClient.invalidateQueries({ queryKey: projectKeys.detail(id) })
      void queryClient.invalidateQueries({ queryKey: projectKeys.summary(id) })
    },
  })
}

export function useInternalProjects(filters: ProjectFilters) {
  return useQuery({
    queryKey: internalProjectKeys.list(filters),
    queryFn: () => getInternalProjects(filters),
  })
}

export function useInternalProject(id: string | undefined) {
  return useQuery({
    queryKey: internalProjectKeys.detail(id ?? ''),
    queryFn: () => getInternalProject(id!),
    enabled: Boolean(id),
  })
}

export function useCreateInternalProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: ProjectCreateInput) => createInternalProject(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: internalProjectKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: internalProjectKeys.all })
    },
  })
}

export function useUpdateInternalProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: ProjectUpdateInput }) =>
      updateInternalProject(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: internalProjectKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: internalProjectKeys.all })
      void queryClient.invalidateQueries({ queryKey: internalProjectKeys.detail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: projectKeys.summary(variables.id) })
    },
  })
}

export function useDeleteInternalProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => deleteInternalProject(id),
    onSuccess: (_data, id) => {
      void queryClient.invalidateQueries({ queryKey: internalProjectKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: internalProjectKeys.all })
      void queryClient.invalidateQueries({ queryKey: internalProjectKeys.detail(id) })
      void queryClient.invalidateQueries({ queryKey: projectKeys.summary(id) })
    },
  })
}
