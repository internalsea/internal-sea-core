import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { MetricStatusBadge } from '@/features/performance/components/MetricStatusBadge'
import type { PerformanceMetricDefinitionListItem } from '@/features/performance/types'
import { formatDateTime, formatSubjectType } from '@/features/performance/utils'

interface MetricDefinitionsTableProps {
  items: PerformanceMetricDefinitionListItem[]
  onDelete?: (item: PerformanceMetricDefinitionListItem) => void
}

export function MetricDefinitionsTable({ items, onDelete }: MetricDefinitionsTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No metric definitions found.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Name</th>
            <th className="px-3 py-2">Code</th>
            <th className="px-3 py-2">Subject</th>
            <th className="px-3 py-2">Value type</th>
            <th className="px-3 py-2">Direction</th>
            <th className="px-3 py-2">Target</th>
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Updated</th>
            <th className="px-3 py-2">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => (
            <tr key={item.id}>
              <td className="px-3 py-2">
                <Link className="font-medium text-core-blue hover:underline" to={`/performance/metrics/${item.id}`}>
                  {item.name}
                </Link>
              </td>
              <td className="px-3 py-2 font-mono text-xs">{item.code ?? '—'}</td>
              <td className="px-3 py-2">{formatSubjectType(item.subject_type)}</td>
              <td className="px-3 py-2">{item.value_type}</td>
              <td className="px-3 py-2">{item.direction.replace(/_/g, ' ')}</td>
              <td className="px-3 py-2">{item.target_value ?? '—'}</td>
              <td className="px-3 py-2">
                <MetricStatusBadge status={item.status} />
              </td>
              <td className="px-3 py-2">{formatDateTime(item.updated_at)}</td>
              <td className="px-3 py-2">
                <div className="flex gap-2">
                  <Link to={`/performance/metrics/${item.id}/edit`}>
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
          ))}
        </tbody>
      </table>
    </div>
  )
}
