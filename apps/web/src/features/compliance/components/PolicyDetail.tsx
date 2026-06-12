import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import { Card } from '@/components/ui/Card'
import { PolicyStatusBadge } from '@/features/compliance/components/PolicyStatusBadge'
import { RulesTable } from '@/features/compliance/components/RulesTable'
import { usePolicyRules } from '@/features/compliance/hooks'
import type { Policy } from '@/features/compliance/types'
import { formatDate, formatDateTime } from '@/features/compliance/utils'

interface PolicyDetailProps {
  policy: Policy
  onEdit: () => void
  onDelete: () => void
}

export function PolicyDetail({ policy, onEdit, onDelete }: PolicyDetailProps) {
  const canWrite = useCanWrite()
  const { data: rulesData, isLoading } = usePolicyRules(policy.id)

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="text-2xl font-semibold text-gray-900">{policy.name}</h1>
            <PolicyStatusBadge status={policy.status} />
          </div>
          {policy.description ? <p className="text-gray-600">{policy.description}</p> : null}
        </div>
        {canWrite ? (
          <div className="flex gap-2">
            <Button variant="secondary" onClick={onEdit}>Edit</Button>
            <Button variant="ghost" onClick={onDelete}>Delete</Button>
          </div>
        ) : null}
      </div>

      <Card title="Overview">
        <dl className="grid gap-4 sm:grid-cols-2">
          <div><dt className="text-xs font-medium uppercase text-gray-500">Version</dt><dd className="mt-1 text-sm">{policy.version ?? '—'}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">Owner ID</dt><dd className="mt-1 text-sm">{policy.owner_id ?? '—'}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">Effective from</dt><dd className="mt-1 text-sm">{formatDate(policy.effective_from)}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">Effective to</dt><dd className="mt-1 text-sm">{formatDate(policy.effective_to)}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">Updated</dt><dd className="mt-1 text-sm">{formatDateTime(policy.updated_at)}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">ID</dt><dd className="mt-1 text-sm break-all">{policy.id}</dd></div>
        </dl>
      </Card>

      <Card title="Rules">
        {isLoading ? <p className="text-sm text-gray-500">Loading rules…</p> : <RulesTable items={rulesData?.items ?? []} />}
      </Card>
    </div>
  )
}
