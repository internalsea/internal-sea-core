import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { activityKeys } from '@/features/activity/hooks'
import { fileKeys } from '@/features/files/hooks'
import type { FileEntityType } from '@/features/files/types'
import {
  addComplianceEvidence,
  createComplianceCheck,
  createPolicy,
  deleteComplianceCheck,
  deleteComplianceEvidence,
  deletePolicy,
  getComplianceCheck,
  getComplianceCheckEvidence,
  getComplianceChecks,
  getComplianceOverview,
  getEntityCompliance,
  getPolicies,
  getPolicy,
  getPolicyRules,
  updateComplianceCheck,
  updatePolicy,
} from '@/features/compliance/api'
import type {
  ComplianceCheckCreateInput,
  ComplianceCheckFilters,
  ComplianceCheckUpdateInput,
  ComplianceEvidenceCreateInput,
  ComplianceSubjectType,
  PolicyCreateInput,
  PolicyFilters,
  PolicyUpdateInput,
} from '@/features/compliance/types'

export const complianceKeys = {
  all: ['compliance'] as const,
  overview: () => [...complianceKeys.all, 'overview'] as const,
  policies: () => [...complianceKeys.all, 'policies'] as const,
  policyList: (filters: PolicyFilters) => [...complianceKeys.policies(), filters] as const,
  policy: (id: string) => [...complianceKeys.policies(), id] as const,
  policyRules: (policyId: string) => [...complianceKeys.policy(policyId), 'rules'] as const,
  checks: () => [...complianceKeys.all, 'checks'] as const,
  checkList: (filters: ComplianceCheckFilters) => [...complianceKeys.checks(), filters] as const,
  check: (id: string) => [...complianceKeys.checks(), id] as const,
  checkEvidence: (checkId: string) => [...complianceKeys.check(checkId), 'evidence'] as const,
  entity: (subjectType: ComplianceSubjectType, subjectId: string) =>
    [...complianceKeys.all, 'entity', subjectType, subjectId] as const,
}

export function useComplianceOverview() {
  return useQuery({ queryKey: complianceKeys.overview(), queryFn: getComplianceOverview })
}

export function usePolicies(filters: PolicyFilters) {
  return useQuery({
    queryKey: complianceKeys.policyList(filters),
    queryFn: () => getPolicies(filters),
  })
}

export function usePolicy(id: string | undefined) {
  return useQuery({
    queryKey: complianceKeys.policy(id ?? ''),
    queryFn: () => getPolicy(id!),
    enabled: Boolean(id),
  })
}

export function usePolicyRules(policyId: string | undefined) {
  return useQuery({
    queryKey: complianceKeys.policyRules(policyId ?? ''),
    queryFn: () => getPolicyRules(policyId!),
    enabled: Boolean(policyId),
  })
}

export function useCreatePolicy() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: PolicyCreateInput) => createPolicy(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: complianceKeys.policies() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.overview() })
    },
  })
}

export function useUpdatePolicy() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: PolicyUpdateInput }) =>
      updatePolicy(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: complianceKeys.policies() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.policy(variables.id) })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.overview() })
    },
  })
}

export function useDeletePolicy() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => deletePolicy(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: complianceKeys.policies() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.overview() })
    },
  })
}

export function useComplianceChecks(filters: ComplianceCheckFilters) {
  return useQuery({
    queryKey: complianceKeys.checkList(filters),
    queryFn: () => getComplianceChecks(filters),
  })
}

export function useComplianceCheck(id: string | undefined) {
  return useQuery({
    queryKey: complianceKeys.check(id ?? ''),
    queryFn: () => getComplianceCheck(id!),
    enabled: Boolean(id),
  })
}

export function useCreateComplianceCheck() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ComplianceCheckCreateInput) => createComplianceCheck(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: complianceKeys.checks() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.overview() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.all })
    },
  })
}

export function useUpdateComplianceCheck() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: ComplianceCheckUpdateInput }) =>
      updateComplianceCheck(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: complianceKeys.checks() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.check(variables.id) })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.overview() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.all })
    },
  })
}

export function useDeleteComplianceCheck() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => deleteComplianceCheck(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: complianceKeys.checks() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.overview() })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.all })
    },
  })
}

export function useEntityCompliance(
  subjectType: ComplianceSubjectType,
  subjectId: string | undefined,
) {
  return useQuery({
    queryKey: complianceKeys.entity(subjectType, subjectId ?? ''),
    queryFn: () => getEntityCompliance(subjectType, subjectId!),
    enabled: Boolean(subjectId),
  })
}

export function useComplianceCheckEvidence(checkId: string | undefined) {
  return useQuery({
    queryKey: complianceKeys.checkEvidence(checkId ?? ''),
    queryFn: () => getComplianceCheckEvidence(checkId!),
    enabled: Boolean(checkId),
  })
}

const FILE_ENTITY_SUBJECT_TYPES = new Set<ComplianceSubjectType>([
  'data_product',
  'project',
  'internal_project',
])

function toFileEntityType(subjectType: ComplianceSubjectType): FileEntityType | null {
  if (!FILE_ENTITY_SUBJECT_TYPES.has(subjectType)) return null
  return subjectType as FileEntityType
}

export function useAddComplianceEvidence(checkId: string, subjectType: ComplianceSubjectType, subjectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ComplianceEvidenceCreateInput) => addComplianceEvidence(checkId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: complianceKeys.checkEvidence(checkId) })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.entity(subjectType, subjectId) })
      const fileEntityType = toFileEntityType(subjectType)
      if (fileEntityType) {
        void queryClient.invalidateQueries({ queryKey: fileKeys.entity(fileEntityType, subjectId) })
      }
      void queryClient.invalidateQueries({ queryKey: activityKeys.entity(subjectType, subjectId) })
    },
  })
}

export function useDeleteComplianceEvidence(
  checkId: string,
  subjectType: ComplianceSubjectType,
  subjectId: string,
) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (evidenceId: string) => deleteComplianceEvidence(evidenceId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: complianceKeys.checkEvidence(checkId) })
      void queryClient.invalidateQueries({ queryKey: complianceKeys.entity(subjectType, subjectId) })
    },
  })
}
