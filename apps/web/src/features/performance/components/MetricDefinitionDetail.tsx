import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { DetailEntityField } from '@/features/entity-picker/components/DetailEntityField'
import { MetricStatusBadge } from '@/features/performance/components/MetricStatusBadge'
import { MetricValuesTable } from '@/features/performance/components/MetricValuesTable'
import type { PerformanceMetricDefinition, PerformanceMetricValueListItem } from '@/features/performance/types'
import { formatDateTime, formatSubjectType } from '@/features/performance/utils'

interface MetricDefinitionDetailProps {
  definition: PerformanceMetricDefinition
  recentValues: PerformanceMetricValueListItem[]
}

function DetailField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-700">{value}</dd>
    </div>
  )
}

export function MetricDefinitionDetail({ definition, recentValues }: MetricDefinitionDetailProps) {
  return (
    <div className="space-y-6">
      <Card title="Overview">
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <DetailField label="Code" value={definition.code ?? '—'} />
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Status</dt>
            <dd className="mt-1">
              <MetricStatusBadge status={definition.status} />
            </dd>
          </div>
          <DetailField label="Subject type" value={formatSubjectType(definition.subject_type)} />
          <DetailField label="Value type" value={definition.value_type} />
          <DetailField label="Direction" value={definition.direction.replace(/_/g, ' ')} />
          <DetailField label="Frequency" value={definition.frequency ?? '—'} />
          <DetailField label="Unit" value={definition.unit ?? '—'} />
          <DetailField label="Description" value={definition.description ?? '—'} />
        </dl>
      </Card>

      <Card title="Thresholds">
        <dl className="grid gap-4 sm:grid-cols-3">
          <DetailField label="Target" value={definition.target_value ?? '—'} />
          <DetailField label="Warning" value={definition.warning_threshold ?? '—'} />
          <DetailField label="Critical" value={definition.critical_threshold ?? '—'} />
        </dl>
      </Card>

      <Card title="Owner">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailEntityField label="Owner" entityType="person" entityId={definition.owner_id} />
        </dl>
      </Card>

      <Card title="Recent values">
        <MetricValuesTable items={recentValues} />
      </Card>

      <Card title="Related scorecards">
        <p className="text-sm text-gray-500">
          Open entity detail pages to view scorecards using this metric definition.
        </p>
      </Card>

      <Card title="System info">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField label="Created" value={formatDateTime(definition.created_at)} />
          <DetailField label="Updated" value={formatDateTime(definition.updated_at)} />
          <DetailField label="ID" value={definition.id} />
        </dl>
        <div className="mt-4">
          <Link to={`/performance/metrics/${definition.id}/edit`}>
            <Button variant="secondary">Edit metric</Button>
          </Link>
        </div>
      </Card>
    </div>
  )
}
