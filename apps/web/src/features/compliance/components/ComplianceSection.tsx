import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { ComplianceChecksTable } from '@/features/compliance/components/ComplianceChecksTable'
import { useEntityCompliance } from '@/features/compliance/hooks'
import type { ComplianceSubjectType } from '@/features/compliance/types'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { useCanWrite } from '@/features/auth/hooks'
import { getApiErrorMessage } from '@/features/compliance/utils'

interface ComplianceSectionProps {
  subjectType: ComplianceSubjectType
  subjectId: string
  title?: string
}

export function ComplianceSection({
  subjectType,
  subjectId,
  title = 'Compliance',
}: ComplianceSectionProps) {
  const navigate = useNavigate()
  const canWrite = useCanWrite()
  const { data, isLoading, isError, error } = useEntityCompliance(subjectType, subjectId)

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title={title}
          description="Policies, rules and checks for this record."
        />
        <PermissionGate require="editor">
          <Link to={`/compliance/checks/new?subject_type=${subjectType}&subject_id=${subjectId}`}>
            <Button variant="secondary" size="sm">New Check</Button>
          </Link>
        </PermissionGate>
      </div>

      {isLoading ? (
        <p className="mt-4 text-sm text-gray-500">Loading compliance checks…</p>
      ) : isError ? (
        <p className="mt-4 text-sm text-status-danger">{getApiErrorMessage(error)}</p>
      ) : (
        <div className="mt-4 space-y-4">
          <div className="grid gap-3 sm:grid-cols-4">
            <SummaryStat label="Total" value={data?.total ?? 0} />
            <SummaryStat label="Compliant" value={data?.compliant_count ?? 0} />
            <SummaryStat label="Non-compliant" value={data?.non_compliant_count ?? 0} />
            <SummaryStat label="Open" value={data?.open_count ?? 0} />
          </div>
          {(data?.checks.length ?? 0) === 0 ? (
            <p className="text-sm text-gray-500">No compliance checks for this record yet.</p>
          ) : (
            <ComplianceChecksTable
              items={data?.checks ?? []}
              onOpen={(id) => navigate(`/compliance/checks/${id}`)}
              onEdit={canWrite ? (id) => navigate(`/compliance/checks/${id}/edit`) : () => undefined}
              onDelete={() => undefined}
              showWriteActions={canWrite}
            />
          )}
        </div>
      )}
    </Card>
  )
}

function SummaryStat({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-md border border-app-border bg-app-muted/30 px-3 py-2">
      <p className="text-xs font-medium text-gray-500">{label}</p>
      <p className="text-lg font-semibold text-gray-900">{value}</p>
    </div>
  )
}
