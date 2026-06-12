import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  Company,
  CompanyCreateInput,
  CompanyListResponse,
  CompanyMember,
  CompanyMemberCreateInput,
  CompanyMemberListResponse,
  CompanyMemberUpdateInput,
  CompanyUpdateInput,
  CurrentTenantContext,
  FirstUserOnboardingRequest,
  FirstUserOnboardingResponse,
  Workspace,
  WorkspaceCreateInput,
  WorkspaceListResponse,
  WorkspaceUpdateInput,
} from '@/features/tenancy/types'

export function firstUserOnboarding(
  payload: FirstUserOnboardingRequest,
): Promise<FirstUserOnboardingResponse> {
  return apiPost<FirstUserOnboardingResponse>('/tenancy/onboarding/first-user', payload)
}

export function getCurrentTenant(): Promise<CurrentTenantContext> {
  return apiGet<CurrentTenantContext>('/tenancy/current')
}

export function listCompanies(page = 1, pageSize = 20): Promise<CompanyListResponse> {
  return apiGet<CompanyListResponse>('/tenancy/companies', { page, page_size: pageSize })
}

export function createCompany(payload: CompanyCreateInput): Promise<Company> {
  return apiPost<Company>('/tenancy/companies', payload)
}

export function getCompany(companyId: string): Promise<Company> {
  return apiGet<Company>(`/tenancy/companies/${companyId}`)
}

export function updateCompany(companyId: string, payload: CompanyUpdateInput): Promise<Company> {
  return apiPatch<Company>(`/tenancy/companies/${companyId}`, payload)
}

export function listWorkspaces(
  companyId: string,
  page = 1,
  pageSize = 20,
): Promise<WorkspaceListResponse> {
  return apiGet<WorkspaceListResponse>(`/tenancy/companies/${companyId}/workspaces`, {
    page,
    page_size: pageSize,
  })
}

export function createWorkspace(companyId: string, payload: WorkspaceCreateInput): Promise<Workspace> {
  return apiPost<Workspace>(`/tenancy/companies/${companyId}/workspaces`, payload)
}

export function getWorkspace(workspaceId: string): Promise<Workspace> {
  return apiGet<Workspace>(`/tenancy/workspaces/${workspaceId}`)
}

export function updateWorkspace(
  workspaceId: string,
  payload: WorkspaceUpdateInput,
): Promise<Workspace> {
  return apiPatch<Workspace>(`/tenancy/workspaces/${workspaceId}`, payload)
}

export function listMembers(
  companyId: string,
  page = 1,
  pageSize = 20,
): Promise<CompanyMemberListResponse> {
  return apiGet<CompanyMemberListResponse>(`/tenancy/companies/${companyId}/members`, {
    page,
    page_size: pageSize,
  })
}

export function addMember(companyId: string, payload: CompanyMemberCreateInput): Promise<CompanyMember> {
  return apiPost<CompanyMember>(`/tenancy/companies/${companyId}/members`, payload)
}

export function updateMember(memberId: string, payload: CompanyMemberUpdateInput): Promise<CompanyMember> {
  return apiPatch<CompanyMember>(`/tenancy/members/${memberId}`, payload)
}

export function removeMember(memberId: string): Promise<void> {
  return apiDelete(`/tenancy/members/${memberId}`)
}
