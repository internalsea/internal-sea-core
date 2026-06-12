import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  addMember,
  createCompany,
  createWorkspace,
  firstUserOnboarding,
  getCompany,
  getCurrentTenant,
  getWorkspace,
  listCompanies,
  listMembers,
  listWorkspaces,
  removeMember,
  updateCompany,
  updateMember,
  updateWorkspace,
} from '@/features/tenancy/api'
import type {
  CompanyCreateInput,
  CompanyMemberCreateInput,
  CompanyMemberUpdateInput,
  CompanyUpdateInput,
  FirstUserOnboardingRequest,
  WorkspaceCreateInput,
  WorkspaceUpdateInput,
} from '@/features/tenancy/types'

export const tenancyKeys = {
  all: ['tenancy'] as const,
  current: () => [...tenancyKeys.all, 'current'] as const,
  companies: () => [...tenancyKeys.all, 'companies'] as const,
  company: (id: string) => [...tenancyKeys.companies(), id] as const,
  workspaces: (companyId: string) => [...tenancyKeys.all, 'workspaces', companyId] as const,
  workspace: (id: string) => [...tenancyKeys.all, 'workspace', id] as const,
  members: (companyId: string) => [...tenancyKeys.all, 'members', companyId] as const,
}

export function useCurrentTenantQuery(enabled = true) {
  return useQuery({
    queryKey: tenancyKeys.current(),
    queryFn: getCurrentTenant,
    enabled,
    retry: false,
  })
}

export function useCompanies(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: [...tenancyKeys.companies(), page, pageSize],
    queryFn: () => listCompanies(page, pageSize),
  })
}

export function useCompany(companyId: string | undefined) {
  return useQuery({
    queryKey: tenancyKeys.company(companyId ?? ''),
    queryFn: () => getCompany(companyId!),
    enabled: Boolean(companyId),
  })
}

export function useWorkspaces(companyId: string | undefined, page = 1, pageSize = 20) {
  return useQuery({
    queryKey: [...tenancyKeys.workspaces(companyId ?? ''), page, pageSize],
    queryFn: () => listWorkspaces(companyId!, page, pageSize),
    enabled: Boolean(companyId),
  })
}

export function useWorkspace(workspaceId: string | undefined) {
  return useQuery({
    queryKey: tenancyKeys.workspace(workspaceId ?? ''),
    queryFn: () => getWorkspace(workspaceId!),
    enabled: Boolean(workspaceId),
  })
}

export function useCompanyMembers(companyId: string | undefined, page = 1, pageSize = 50) {
  return useQuery({
    queryKey: [...tenancyKeys.members(companyId ?? ''), page, pageSize],
    queryFn: () => listMembers(companyId!, page, pageSize),
    enabled: Boolean(companyId),
  })
}

export function useFirstUserOnboarding() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: FirstUserOnboardingRequest) => firstUserOnboarding(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.all })
    },
  })
}

export function useCreateCompany() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: CompanyCreateInput) => createCompany(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.companies() })
    },
  })
}

export function useUpdateCompany() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: CompanyUpdateInput }) =>
      updateCompany(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.companies() })
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.company(variables.id) })
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.current() })
    },
  })
}

export function useCreateWorkspace() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ companyId, payload }: { companyId: string; payload: WorkspaceCreateInput }) =>
      createWorkspace(companyId, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.workspaces(variables.companyId) })
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.current() })
    },
  })
}

export function useUpdateWorkspace() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: WorkspaceUpdateInput }) =>
      updateWorkspace(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.workspace(variables.id) })
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.current() })
    },
  })
}

export function useAddMember() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ companyId, payload }: { companyId: string; payload: CompanyMemberCreateInput }) =>
      addMember(companyId, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.members(variables.companyId) })
    },
  })
}

export function useUpdateMember() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ memberId, payload }: { memberId: string; payload: CompanyMemberUpdateInput }) =>
      updateMember(memberId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.all })
    },
  })
}

export function useRemoveMember() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ memberId }: { memberId: string; companyId: string }) => removeMember(memberId),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: tenancyKeys.members(variables.companyId) })
    },
  })
}
