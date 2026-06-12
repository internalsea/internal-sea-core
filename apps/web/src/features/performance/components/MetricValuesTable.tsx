import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { DetailEntityField } from '@/features/entity-picker/components/DetailEntityField'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { MetricValueStatusBadge } from '@/features/performance/components/MetricValueStatusBadge'
import type { PerformanceMetricDefinitionListItem, PerformanceMetricValueListItem } from '@/features/performance/types'
import { formatDate, formatDateTime, formatMetricValue, formatSubjectType } from '@/features/performance/utils'

interface MetricValuesTableProps {
  items: PerformanceMetricValueListItem[]
  definitionsById?: Record<string, PerformanceMetricDefinitionListItem>
  onDelete?: (item: PerformanceMetricValueListItem) => void
}

export function MetricValuesTable({ items, definitionsById, onDelete }: MetricValuesTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No metric values found.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Metric</th>
            <th className="px-3 py-2">Subject</th>
            <th className="px-3 py-2">Value</th>
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Period</th>
            <th className="px-3 py-2">Source</th>
            <th className="px-3 py-2">Updated</th>
            <th className="px-3 py-2">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => {
            const definition = definitionsById?.[item.metric_definition_id]
            return (
              <tr key={item.id}>
                <td className="px-3 py-2">
                  {definition ? (
                    <Link
                      className="font-medium text-core-blue hover:underline"
                      to={`/performance/metrics/${definition.id}`}
                    >
                      {definition.name}
                    </Link>
                  ) : (
                    <span className="font-mono text-xs">{item.metric_definition_id.slice(0, 8)}</span>
                  )}
                </td>
                <td className="px-3 py-2">
                  <div className="space-y-1">
                    <p className="text-xs text-gray-500">{formatSubjectType(item.subject_type)}</p>
                    <DetailEntityField
                      label=""
                      entityType={item.subject_type}
                      entityId={item.subject_id}
                    />
                  </div>
                </td>
                <td className="px-3 py-2">
                  {formatMetricValue(item.value_numeric, item.value_text, item.value_bool, definition?.unit)}
                </td>
                <td className="px-3 py-2">
                  <MetricValueStatusBadge status={item.status} />
                </td>
                <td className="px-3 py-2">
                  {formatDate(item.period_start)} – {formatDate(item.period_end)}
                </td>
                <td className="px-3 py-2">{item.source ?? '—'}</td>
                <td className="px-3 py-2">{formatDateTime(item.updated_at)}</td>
                <td className="px-3 py-2">
                  <div className="flex gap-2">
                    <Link to={`/performance/values/${item.id}/edit`}>
                      <Button variant="secondary" size="sm">Edit</Button>
                    </Link>
                    <PermissionGate require="editor">
                      {onDelete ? (
                        <Button variant="secondary" size="sm" onClick={() => onDelete(item)}>
                          Delete
                        </Button>
                      ) : null}
                    </PermissionGate>
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
