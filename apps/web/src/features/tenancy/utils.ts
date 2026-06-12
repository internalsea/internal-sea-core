import type {
  Company,
  CompanyFormValues,
  CompanyUpdateInput,
  FirstUserOnboardingFormValues,
  FirstUserOnboardingRequest,
  Workspace,
  WorkspaceFormValues,
  WorkspaceUpdateInput,
} from '@/features/tenancy/types'

export const COMPANY_ID_STORAGE_KEY = 'internal_sea_core_company_id'
export const WORKSPACE_ID_STORAGE_KEY = 'internal_sea_core_workspace_id'

export function getStoredCompanyId(): string | null {
  return localStorage.getItem(COMPANY_ID_STORAGE_KEY)
}

export function getStoredWorkspaceId(): string | null {
  return localStorage.getItem(WORKSPACE_ID_STORAGE_KEY)
}

export function setStoredCompanyId(companyId: string): void {
  localStorage.setItem(COMPANY_ID_STORAGE_KEY, companyId)
}

export function setStoredWorkspaceId(workspaceId: string): void {
  localStorage.setItem(WORKSPACE_ID_STORAGE_KEY, workspaceId)
}

export function setStoredTenantIds(companyId: string, workspaceId: string): void {
  setStoredCompanyId(companyId)
  setStoredWorkspaceId(workspaceId)
}

export function clearStoredTenantIds(): void {
  localStorage.removeItem(COMPANY_ID_STORAGE_KEY)
  localStorage.removeItem(WORKSPACE_ID_STORAGE_KEY)
}

export function companyToFormValues(company: Company): CompanyFormValues {
  return {
    name: company.name,
    slug: company.slug,
    description: company.description ?? '',
    industry: company.industry ?? '',
    company_size: company.company_size ?? '',
    country: company.country ?? '',
    website: company.website ?? '',
    status: company.status,
  }
}

export function workspaceToFormValues(workspace: Workspace): WorkspaceFormValues {
  return {
    name: workspace.name,
    slug: workspace.slug,
    description: workspace.description ?? '',
    default_timezone: workspace.default_timezone ?? 'UTC',
    default_currency: workspace.default_currency ?? 'EUR',
    status: workspace.status,
  }
}

export function formValuesToCompanyUpdate(values: CompanyFormValues): CompanyUpdateInput {
  return {
    name: values.name.trim(),
    slug: values.slug.trim() || null,
    description: values.description.trim() || null,
    industry: values.industry ? (values.industry as CompanyUpdateInput['industry']) : null,
    company_size: values.company_size
      ? (values.company_size as CompanyUpdateInput['company_size'])
      : null,
    country: values.country.trim() || null,
    website: values.website.trim() || null,
    status: values.status ? (values.status as CompanyUpdateInput['status']) : null,
  }
}

export function formValuesToWorkspaceUpdate(values: WorkspaceFormValues): WorkspaceUpdateInput {
  return {
    name: values.name.trim(),
    slug: values.slug.trim() || null,
    description: values.description.trim() || null,
    default_timezone: values.default_timezone.trim() || null,
    default_currency: values.default_currency.trim() || null,
    status: values.status ? (values.status as WorkspaceUpdateInput['status']) : null,
  }
}

export function formValuesToOnboardingRequest(
  values: FirstUserOnboardingFormValues,
): FirstUserOnboardingRequest {
  return {
    full_name: values.full_name.trim(),
    email: values.email.trim(),
    password: values.password,
    company_name: values.company_name.trim(),
    company_size: values.company_size
      ? (values.company_size as FirstUserOnboardingRequest['company_size'])
      : null,
    industry: values.industry ? (values.industry as FirstUserOnboardingRequest['industry']) : null,
    country: values.country.trim() || null,
    team_name: values.team_name.trim() || null,
    main_capability_name: values.main_capability_name.trim() || null,
  }
}

export function formatMemberRole(role: string): string {
  switch (role) {
    case 'owner':
      return 'Owner'
    case 'admin':
      return 'Admin'
    case 'editor':
      return 'Editor'
    case 'viewer':
      return 'Viewer'
    default:
      return role
  }
}
