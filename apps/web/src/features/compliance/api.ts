import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  ComplianceCheck,
  ComplianceCheckCreateInput,
  ComplianceCheckFilters,
  ComplianceCheckListResponse,
  ComplianceCheckUpdateInput,
  ComplianceEvidence,
  ComplianceEvidenceCreateInput,
  ComplianceOverview,
  ComplianceRule,
  EntityComplianceResponse,
  Policy,
  PolicyCreateInput,
  PolicyFilters,
  PolicyListResponse,
  PolicyUpdateInput,
} from '@/features/compliance/types'

function policyQueryParams(
  filters?: PolicyFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) return undefined
  return {
    search: filters.search,
    status: filters.status,
    owner_id: filters.owner_id,
    page: filters.page,
    page_size: filters.page_size,
  }
}

function checkQueryParams(
  filters?: ComplianceCheckFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) return undefined
  return {
    search: filters.search,
    subject_type: filters.subject_type,
    subject_id: filters.subject_id,
    status: filters.status,
    check_type: filters.check_type,
    overdue: filters.overdue,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getComplianceOverview(): Promise<ComplianceOverview> {
  return apiGet<ComplianceOverview>('/compliance/overview')
}

export function getPolicies(filters?: PolicyFilters): Promise<PolicyListResponse> {
  return apiGet<PolicyListResponse>('/compliance/policies', policyQueryParams(filters))
}

export function getPolicy(id: string): Promise<Policy> {
  return apiGet<Policy>(`/compliance/policies/${id}`)
}

export function createPolicy(payload: PolicyCreateInput): Promise<Policy> {
  return apiPost<Policy>('/compliance/policies', payload)
}

export function updatePolicy(id: string, payload: PolicyUpdateInput): Promise<Policy> {
  return apiPatch<Policy>(`/compliance/policies/${id}`, payload)
}

export function deletePolicy(id: string): Promise<void> {
  return apiDelete(`/compliance/policies/${id}`)
}

export function getPolicyRules(policyId: string): Promise<{ items: ComplianceRule[]; total: number }> {
  return apiGet<{ items: ComplianceRule[]; total: number }>(`/compliance/policies/${policyId}/rules`)
}

export function getComplianceChecks(
  filters?: ComplianceCheckFilters,
): Promise<ComplianceCheckListResponse> {
  return apiGet<ComplianceCheckListResponse>('/compliance/checks', checkQueryParams(filters))
}

export function getComplianceCheck(id: string): Promise<ComplianceCheck> {
  return apiGet<ComplianceCheck>(`/compliance/checks/${id}`)
}

export function createComplianceCheck(payload: ComplianceCheckCreateInput): Promise<ComplianceCheck> {
  return apiPost<ComplianceCheck>('/compliance/checks', payload)
}

export function updateComplianceCheck(
  id: string,
  payload: ComplianceCheckUpdateInput,
): Promise<ComplianceCheck> {
  return apiPatch<ComplianceCheck>(`/compliance/checks/${id}`, payload)
}

export function deleteComplianceCheck(id: string): Promise<void> {
  return apiDelete(`/compliance/checks/${id}`)
}

export function getEntityCompliance(
  subjectType: string,
  subjectId: string,
): Promise<EntityComplianceResponse> {
  return apiGet<EntityComplianceResponse>(`/compliance/entity/${subjectType}/${subjectId}`)
}

export function getComplianceCheckEvidence(checkId: string): Promise<ComplianceEvidence[]> {
  return apiGet<ComplianceEvidence[]>(`/compliance/checks/${checkId}/evidence`)
}

export function addComplianceEvidence(
  checkId: string,
  payload: ComplianceEvidenceCreateInput,
): Promise<ComplianceEvidence> {
  return apiPost<ComplianceEvidence>(`/compliance/checks/${checkId}/evidence`, payload)
}

export function deleteComplianceEvidence(evidenceId: string): Promise<void> {
  return apiDelete(`/compliance/evidence/${evidenceId}`)
}
