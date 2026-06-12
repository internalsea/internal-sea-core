import type { ApiError } from '@/lib/apiClient'
import {
  complianceStatusVariantMap,
  evidenceStatusVariantMap,
  ruleSeverityVariantMap,
  subjectTypeLabels,
} from '@/features/compliance/constants'
import type {
  ComplianceCheck,
  ComplianceCheckFormValues,
  ComplianceCheckListItem,
  ComplianceEvidenceCreateInput,
  ComplianceStatus,
  ComplianceSubjectType,
  EvidenceStatus,
  Policy,
  PolicyFormValues,
  RuleSeverity,
} from '@/features/compliance/types'
import type { BadgeVariant } from '@/lib/designTokens'

export function formatDate(value: string | null | undefined): string {
  if (!value) return '—'
  const date = new Date(value.includes('T') ? value : `${value}T00:00:00`)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatSubjectType(subjectType: ComplianceSubjectType): string {
  return subjectTypeLabels[subjectType] ?? subjectType
}

export function getSubjectHref(
  subjectType: ComplianceSubjectType,
  subjectId: string,
): string | null {
  switch (subjectType) {
    case 'data_product':
      return `/data-products/${subjectId}`
    case 'project':
      return `/projects/${subjectId}`
    case 'internal_project':
      return `/internal-projects/${subjectId}`
    case 'team':
      return `/teams/${subjectId}`
    case 'capability':
      return `/capabilities/${subjectId}`
    default:
      return null
  }
}

export function getComplianceStatusVariant(status: ComplianceStatus): BadgeVariant {
  return complianceStatusVariantMap[status] ?? 'neutral'
}

export function getRuleSeverityVariant(severity: RuleSeverity): BadgeVariant {
  return ruleSeverityVariantMap[severity] ?? 'neutral'
}

export function getEvidenceStatusVariant(status: EvidenceStatus): BadgeVariant {
  return evidenceStatusVariantMap[status] ?? 'neutral'
}

function emptyToNull(value: string): string | null {
  const trimmed = value.trim()
  return trimmed === '' ? null : trimmed
}

export function cleanPolicyPayload(values: PolicyFormValues) {
  return {
    name: values.name.trim(),
    description: emptyToNull(values.description),
    status: values.status,
    owner_id: emptyToNull(values.owner_id),
    effective_from: emptyToNull(values.effective_from),
    effective_to: emptyToNull(values.effective_to),
    version: emptyToNull(values.version),
  }
}

export function policyToFormValues(policy: Policy): PolicyFormValues {
  return {
    name: policy.name,
    description: policy.description ?? '',
    status: policy.status,
    owner_id: policy.owner_id ?? '',
    effective_from: policy.effective_from ?? '',
    effective_to: policy.effective_to ?? '',
    version: policy.version ?? '',
  }
}

export function cleanComplianceCheckPayload(values: ComplianceCheckFormValues) {
  return {
    title: values.title.trim(),
    description: emptyToNull(values.description),
    subject_type: values.subject_type,
    subject_id: values.subject_id.trim(),
    rule_id: emptyToNull(values.rule_id),
    control_id: emptyToNull(values.control_id),
    check_type: values.check_type,
    status: values.status,
    result_summary: emptyToNull(values.result_summary),
    owner_id: emptyToNull(values.owner_id),
    due_date: emptyToNull(values.due_date),
  }
}

export function checkToFormValues(check: ComplianceCheck): ComplianceCheckFormValues {
  return {
    title: check.title,
    description: check.description ?? '',
    subject_type: check.subject_type,
    subject_id: check.subject_id,
    rule_id: check.rule_id ?? '',
    control_id: check.control_id ?? '',
    check_type: check.check_type,
    status: check.status,
    result_summary: check.result_summary ?? '',
    owner_id: check.owner_id ?? '',
    due_date: check.due_date ?? '',
  }
}

export function cleanEvidencePayload(values: {
  file_id: string
  status: EvidenceStatus
  description: string
}): ComplianceEvidenceCreateInput {
  return {
    file_id: values.file_id.trim(),
    status: values.status,
    description: emptyToNull(values.description),
  }
}

export function isOverdueCheck(check: ComplianceCheckListItem | ComplianceCheck): boolean {
  if (!check.due_date) return false
  if (check.status === 'compliant' || check.status === 'non_compliant' || check.status === 'exception' || check.status === 'not_applicable') {
    return false
  }
  const due = new Date(check.due_date.includes('T') ? check.due_date : `${check.due_date}T00:00:00`)
  return due < new Date()
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof Error && 'status' in error) {
    return (error as ApiError).message || `Request failed (${(error as ApiError).status})`
  }
  if (error instanceof Error) return error.message
  return 'An unexpected error occurred'
}

export function confirmPolicyDelete(name: string): boolean {
  return window.confirm(`Delete policy "${name}"?`)
}

export function confirmCheckDelete(title: string): boolean {
  return window.confirm(`Delete compliance check "${title}"?`)
}
