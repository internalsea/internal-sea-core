import type { PaginatedResponse } from '@/types/common'

export type PolicyStatus = 'draft' | 'active' | 'deprecated' | 'archived'
export type RuleSeverity = 'low' | 'medium' | 'high' | 'critical'
export type ControlType = 'manual' | 'automated' | 'detective' | 'preventive' | 'corrective'
export type ControlStatus = 'draft' | 'active' | 'deprecated' | 'archived'
export type ComplianceSubjectType =
  | 'data_product'
  | 'project'
  | 'internal_project'
  | 'team'
  | 'capability'
  | 'person'
  | 'tool'
export type ComplianceStatus =
  | 'not_started'
  | 'in_progress'
  | 'compliant'
  | 'non_compliant'
  | 'exception'
  | 'not_applicable'
export type ComplianceCheckType =
  | 'manual'
  | 'automated'
  | 'self_assessment'
  | 'audit'
  | 'review'
export type ComplianceFrequency =
  | 'once'
  | 'daily'
  | 'weekly'
  | 'monthly'
  | 'quarterly'
  | 'yearly'
  | 'on_change'
  | 'custom'
export type EvidenceStatus = 'missing' | 'submitted' | 'accepted' | 'rejected' | 'expired'

export interface Policy {
  id: string
  name: string
  description: string | null
  status: PolicyStatus
  owner_id: string | null
  effective_from: string | null
  effective_to: string | null
  version: string | null
  created_at: string
  updated_at: string
}

export interface PolicyListItem {
  id: string
  name: string
  status: PolicyStatus
  owner_id: string | null
  effective_from: string | null
  effective_to: string | null
  version: string | null
  updated_at: string
}

export type PolicyListResponse = PaginatedResponse<PolicyListItem>

export interface ComplianceRule {
  id: string
  policy_id: string
  code: string | null
  name: string
  description: string | null
  severity: RuleSeverity
  subject_type: ComplianceSubjectType | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Control {
  id: string
  rule_id: string
  name: string
  description: string | null
  control_type: ControlType
  status: ControlStatus
  owner_id: string | null
  frequency: ComplianceFrequency | null
  created_at: string
  updated_at: string
}

export interface ComplianceCheck {
  id: string
  rule_id: string | null
  control_id: string | null
  subject_type: ComplianceSubjectType
  subject_id: string
  check_type: ComplianceCheckType
  status: ComplianceStatus
  title: string
  description: string | null
  result_summary: string | null
  owner_id: string | null
  due_date: string | null
  completed_at: string | null
  next_check_at: string | null
  created_at: string
  updated_at: string
}

export interface ComplianceCheckListItem {
  id: string
  subject_type: ComplianceSubjectType
  subject_id: string
  title: string
  status: ComplianceStatus
  check_type: ComplianceCheckType
  owner_id: string | null
  due_date: string | null
  completed_at: string | null
  next_check_at: string | null
  rule_id: string | null
  control_id: string | null
  updated_at: string
}

export type ComplianceCheckListResponse = PaginatedResponse<ComplianceCheckListItem>

export interface ComplianceEvidence {
  id: string
  compliance_check_id: string
  file_id: string
  status: EvidenceStatus
  description: string | null
  submitted_by_id: string | null
  reviewed_by_id: string | null
  reviewed_at: string | null
  created_at: string
  updated_at: string
}

export interface EntityComplianceResponse {
  subject_type: ComplianceSubjectType
  subject_id: string
  checks: ComplianceCheckListItem[]
  total: number
  compliant_count: number
  non_compliant_count: number
  open_count: number
  overdue_count: number
}

export interface ComplianceOverview {
  policies_total: number
  policies_active: number
  rules_total: number
  active_rules: number
  controls_total: number
  active_controls: number
  checks_total: number
  checks_open: number
  checks_compliant: number
  checks_non_compliant: number
  checks_overdue: number
  evidence_missing: number
}

export interface PolicyFilters {
  search?: string
  status?: PolicyStatus
  owner_id?: string
  page?: number
  page_size?: number
}

export interface ComplianceCheckFilters {
  search?: string
  subject_type?: ComplianceSubjectType
  subject_id?: string
  status?: ComplianceStatus
  check_type?: ComplianceCheckType
  overdue?: boolean
  page?: number
  page_size?: number
}

export interface PolicyCreateInput {
  name: string
  description?: string | null
  status?: PolicyStatus
  owner_id?: string | null
  effective_from?: string | null
  effective_to?: string | null
  version?: string | null
}

export type PolicyUpdateInput = Partial<PolicyCreateInput>

export interface ComplianceCheckCreateInput {
  rule_id?: string | null
  control_id?: string | null
  subject_type: ComplianceSubjectType
  subject_id: string
  check_type?: ComplianceCheckType
  status?: ComplianceStatus
  title: string
  description?: string | null
  result_summary?: string | null
  owner_id?: string | null
  due_date?: string | null
  completed_at?: string | null
  next_check_at?: string | null
}

export type ComplianceCheckUpdateInput = Partial<ComplianceCheckCreateInput>

export interface ComplianceEvidenceCreateInput {
  file_id: string
  status?: EvidenceStatus
  description?: string | null
  submitted_by_id?: string | null
}

export interface PolicyFormValues {
  name: string
  description: string
  status: PolicyStatus
  owner_id: string
  effective_from: string
  effective_to: string
  version: string
}

export interface ComplianceCheckFormValues {
  title: string
  description: string
  subject_type: ComplianceSubjectType
  subject_id: string
  rule_id: string
  control_id: string
  check_type: ComplianceCheckType
  status: ComplianceStatus
  result_summary: string
  owner_id: string
  due_date: string
}
