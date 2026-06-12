import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { useCanWrite } from '@/features/auth/hooks'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { ComplianceChecksTable } from '@/features/compliance/components/ComplianceChecksTable'
import { ComplianceOverviewCards } from '@/features/compliance/components/ComplianceOverviewCards'
import { PoliciesTable } from '@/features/compliance/components/PoliciesTable'
import { DEFAULT_PAGE_SIZE } from '@/features/compliance/constants'
import {
  useComplianceChecks,
  useDeleteComplianceCheck,
  useDeletePolicy,
  usePolicies,
} from '@/features/compliance/hooks'
import type { ComplianceCheckFilters, PolicyFilters } from '@/features/compliance/types'
import { confirmCheckDelete, confirmPolicyDelete, getApiErrorMessage } from '@/features/compliance/utils'

export function CompliancePage() {
  const navigate = useNavigate()
  const canWrite = useCanWrite()
  const [policyFilters] = useState<PolicyFilters>({ page: 1, page_size: DEFAULT_PAGE_SIZE })
  const [checkFilters] = useState<ComplianceCheckFilters>({ page: 1, page_size: DEFAULT_PAGE_SIZE })
  const policiesQuery = usePolicies(policyFilters)
  const checksQuery = useComplianceChecks(checkFilters)
  const deletePolicy = useDeletePolicy()
  const deleteCheck = useDeleteComplianceCheck()

  return (
    <div className="space-y-6">
      <PageHeader
        title="Compliance"
        description="Track policies, rules, controls, checks and evidence across products, projects and teams."
        actions={
          <PermissionGate require="editor">
            <>
              <Link to="/compliance/policies/new"><Button variant="secondary">New Policy</Button></Link>
              <Link to="/compliance/checks/new"><Button>New Check</Button></Link>
            </>
          </PermissionGate>
        }
      />

      <ComplianceOverviewCards />

      <Card title="Policies">
        {policiesQuery.isError ? (
          <ErrorState message={getApiErrorMessage(policiesQuery.error)} />
        ) : (
          <PoliciesTable
            items={policiesQuery.data?.items ?? []}
            isLoading={policiesQuery.isLoading}
            onOpen={(id) => navigate(`/compliance/policies/${id}`)}
            onEdit={(id) => navigate(`/compliance/policies/${id}/edit`)}
            onDelete={async (item) => {
              if (!confirmPolicyDelete(item.name)) return
              await deletePolicy.mutateAsync(item.id)
            }}
          />
        )}
      </Card>

      <Card title="Compliance Checks">
        {checksQuery.isError ? (
          <ErrorState message={getApiErrorMessage(checksQuery.error)} />
        ) : (
          <ComplianceChecksTable
            items={checksQuery.data?.items ?? []}
            isLoading={checksQuery.isLoading}
            showWriteActions={canWrite}
            onOpen={(id) => navigate(`/compliance/checks/${id}`)}
            onEdit={(id) => navigate(`/compliance/checks/${id}/edit`)}
            onDelete={async (item) => {
              if (!confirmCheckDelete(item.title)) return
              await deleteCheck.mutateAsync(item.id)
            }}
          />
        )}
      </Card>

      <Card title="Future governance capabilities">
        <ul className="list-disc space-y-1 pl-5 text-sm text-gray-600">
          <li>Automated rule execution</li>
          <li>Approval workflows</li>
          <li>Scheduled compliance checks</li>
          <li>External audit export</li>
        </ul>
      </Card>
    </div>
  )
}
