import type {
  ComplianceCheckType,
  ComplianceFrequency,
  ComplianceStatus,
  ComplianceSubjectType,
  ControlStatus,
  ControlType,
  EvidenceStatus,
  PolicyStatus,
  RuleSeverity,
} from '@/features/compliance/types'
import type { BadgeVariant } from '@/lib/designTokens'

export interface SelectOption<T extends string = string> {
  value: T
  label: string
}

export const POLICY_STATUSES: SelectOption<PolicyStatus>[] = [
  { value: 'draft', label: 'Draft' },
  { value: 'active', label: 'Active' },
  { value: 'deprecated', label: 'Deprecated' },
  { value: 'archived', label: 'Archived' },
]

export const RULE_SEVERITIES: SelectOption<RuleSeverity>[] = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
  { value: 'critical', label: 'Critical' },
]

export const CONTROL_TYPES: SelectOption<ControlType>[] = [
  { value: 'manual', label: 'Manual' },
  { value: 'automated', label: 'Automated' },
  { value: 'detective', label: 'Detective' },
  { value: 'preventive', label: 'Preventive' },
  { value: 'corrective', label: 'Corrective' },
]

export const CONTROL_STATUSES: SelectOption<ControlStatus>[] = [
  { value: 'draft', label: 'Draft' },
  { value: 'active', label: 'Active' },
  { value: 'deprecated', label: 'Deprecated' },
  { value: 'archived', label: 'Archived' },
]

export const COMPLIANCE_SUBJECT_TYPES: SelectOption<ComplianceSubjectType>[] = [
  { value: 'data_product', label: 'Data Product' },
  { value: 'project', label: 'Project' },
  { value: 'internal_project', label: 'Internal Project' },
  { value: 'team', label: 'Team' },
  { value: 'capability', label: 'Capability' },
  { value: 'person', label: 'Person' },
  { value: 'tool', label: 'Tool' },
]

export const COMPLIANCE_STATUSES: SelectOption<ComplianceStatus>[] = [
  { value: 'not_started', label: 'Not Started' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'compliant', label: 'Compliant' },
  { value: 'non_compliant', label: 'Non-Compliant' },
  { value: 'exception', label: 'Exception' },
  { value: 'not_applicable', label: 'Not Applicable' },
]

export const COMPLIANCE_CHECK_TYPES: SelectOption<ComplianceCheckType>[] = [
  { value: 'manual', label: 'Manual' },
  { value: 'automated', label: 'Automated' },
  { value: 'self_assessment', label: 'Self Assessment' },
  { value: 'audit', label: 'Audit' },
  { value: 'review', label: 'Review' },
]

export const COMPLIANCE_FREQUENCIES: SelectOption<ComplianceFrequency>[] = [
  { value: 'once', label: 'Once' },
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
  { value: 'quarterly', label: 'Quarterly' },
  { value: 'yearly', label: 'Yearly' },
  { value: 'on_change', label: 'On Change' },
  { value: 'custom', label: 'Custom' },
]

export const EVIDENCE_STATUSES: SelectOption<EvidenceStatus>[] = [
  { value: 'missing', label: 'Missing' },
  { value: 'submitted', label: 'Submitted' },
  { value: 'accepted', label: 'Accepted' },
  { value: 'rejected', label: 'Rejected' },
  { value: 'expired', label: 'Expired' },
]

export const complianceStatusLabels: Record<ComplianceStatus, string> = Object.fromEntries(
  COMPLIANCE_STATUSES.map((item) => [item.value, item.label]),
) as Record<ComplianceStatus, string>

export const complianceStatusVariantMap: Record<ComplianceStatus, BadgeVariant> = {
  not_started: 'neutral',
  in_progress: 'teal',
  compliant: 'success',
  non_compliant: 'danger',
  exception: 'warning',
  not_applicable: 'neutral',
}

export const ruleSeverityVariantMap: Record<RuleSeverity, BadgeVariant> = {
  low: 'neutral',
  medium: 'info',
  high: 'warning',
  critical: 'danger',
}

export const evidenceStatusVariantMap: Record<EvidenceStatus, BadgeVariant> = {
  missing: 'danger',
  submitted: 'info',
  accepted: 'success',
  rejected: 'danger',
  expired: 'warning',
}

export const subjectTypeLabels: Record<ComplianceSubjectType, string> = Object.fromEntries(
  COMPLIANCE_SUBJECT_TYPES.map((item) => [item.value, item.label]),
) as Record<ComplianceSubjectType, string>

export const DEFAULT_PAGE_SIZE = 20

export const selectClassName =
  'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue'
