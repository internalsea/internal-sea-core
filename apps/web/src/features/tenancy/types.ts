import type { CurrentUser } from '@/features/auth/types'
import type { PaginatedResponse } from '@/types/common'

export type CompanyStatus = 'trial' | 'active' | 'suspended' | 'archived'

export type CompanySize =
  | 'solo'
  | 'size_2_10'
  | 'size_11_50'
  | 'size_51_200'
  | 'size_201_1000'
  | 'size_1000_plus'

export type WorkspaceStatus = 'active' | 'archived'

export type CompanyMemberRole = 'owner' | 'admin' | 'editor' | 'viewer'

export type CompanyMemberStatus = 'invited' | 'active' | 'inactive' | 'removed'

export type Industry =
  | 'fashion'
  | 'consulting'
  | 'technology'
  | 'retail'
  | 'energy'
  | 'finance'
  | 'manufacturing'
  | 'other'

export interface Company {
  id: string
  name: string
  slug: string
  description: string | null
  industry: string | null
  company_size: string | null
  country: string | null
  website: string | null
  status: string
  created_at: string
  updated_at: string
}

export interface Workspace {
  id: string
  company_id: string
  name: string
  slug: string
  description: string | null
  default_timezone: string | null
  default_currency: string | null
  status: string
  created_at: string
  updated_at: string
}

export interface CompanyMember {
  id: string
  company_id: string
  user_id: string
  person_id: string | null
  role: string
  status: string
  joined_at: string | null
  created_at: string
  updated_at: string
}

export interface CurrentTenantContext {
  company: Company
  workspace: Workspace
  member: CompanyMember
}

export interface FirstUserOnboardingRequest {
  full_name: string
  email: string
  password: string
  company_name: string
  company_size?: CompanySize | null
  industry?: Industry | null
  country?: string | null
  team_name?: string | null
  main_capability_name?: string | null
}

export interface FirstUserOnboardingResponse {
  user: CurrentUser
  company: Company
  workspace: Workspace
  member: CompanyMember
  access_token: string
  token_type: string
  expires_in: number
}

export interface CompanyCreateInput {
  name: string
  slug?: string | null
  description?: string | null
  industry?: Industry | null
  company_size?: CompanySize | null
  country?: string | null
  website?: string | null
  status?: CompanyStatus
}

export interface CompanyUpdateInput {
  name?: string | null
  slug?: string | null
  description?: string | null
  industry?: Industry | null
  company_size?: CompanySize | null
  country?: string | null
  website?: string | null
  status?: CompanyStatus | null
}

export interface WorkspaceCreateInput {
  company_id: string
  name: string
  slug?: string | null
  description?: string | null
  default_timezone?: string
  default_currency?: string
  status?: WorkspaceStatus
}

export interface WorkspaceUpdateInput {
  name?: string | null
  slug?: string | null
  description?: string | null
  default_timezone?: string | null
  default_currency?: string | null
  status?: WorkspaceStatus | null
}

export interface CompanyMemberCreateInput {
  company_id: string
  user_id: string
  person_id?: string | null
  role?: CompanyMemberRole
  status?: CompanyMemberStatus
}

export interface CompanyMemberUpdateInput {
  person_id?: string | null
  role?: CompanyMemberRole | null
  status?: CompanyMemberStatus | null
}

export type CompanyListResponse = PaginatedResponse<Company>
export type WorkspaceListResponse = PaginatedResponse<Workspace>
export type CompanyMemberListResponse = PaginatedResponse<CompanyMember>

export interface CompanyFormValues {
  name: string
  slug: string
  description: string
  industry: string
  company_size: string
  country: string
  website: string
  status: string
}

export interface WorkspaceFormValues {
  name: string
  slug: string
  description: string
  default_timezone: string
  default_currency: string
  status: string
}

export interface FirstUserOnboardingFormValues {
  full_name: string
  email: string
  password: string
  company_name: string
  company_size: string
  industry: string
  country: string
  team_name: string
  main_capability_name: string
}
