import type { CompanyMemberRole, CompanySize, CompanyStatus, Industry, WorkspaceStatus } from '@/features/tenancy/types'

export interface SelectOption<T extends string = string> {
  value: T
  label: string
}

export const COMPANY_STATUSES: SelectOption<CompanyStatus>[] = [
  { value: 'trial', label: 'Trial' },
  { value: 'active', label: 'Active' },
  { value: 'suspended', label: 'Suspended' },
  { value: 'archived', label: 'Archived' },
]

export const COMPANY_SIZES: SelectOption<CompanySize>[] = [
  { value: 'solo', label: 'Solo' },
  { value: 'size_2_10', label: '2–10' },
  { value: 'size_11_50', label: '11–50' },
  { value: 'size_51_200', label: '51–200' },
  { value: 'size_201_1000', label: '201–1,000' },
  { value: 'size_1000_plus', label: '1,000+' },
]

export const INDUSTRIES: SelectOption<Industry>[] = [
  { value: 'fashion', label: 'Fashion' },
  { value: 'consulting', label: 'Consulting' },
  { value: 'technology', label: 'Technology' },
  { value: 'retail', label: 'Retail' },
  { value: 'energy', label: 'Energy' },
  { value: 'finance', label: 'Finance' },
  { value: 'manufacturing', label: 'Manufacturing' },
  { value: 'other', label: 'Other' },
]

export const WORKSPACE_STATUSES: SelectOption<WorkspaceStatus>[] = [
  { value: 'active', label: 'Active' },
  { value: 'archived', label: 'Archived' },
]

export const COMPANY_MEMBER_ROLES: SelectOption<CompanyMemberRole>[] = [
  { value: 'owner', label: 'Owner' },
  { value: 'admin', label: 'Admin' },
  { value: 'editor', label: 'Editor' },
  { value: 'viewer', label: 'Viewer' },
]

export const selectClassName =
  'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue disabled:cursor-not-allowed disabled:bg-app-muted disabled:text-gray-400'
