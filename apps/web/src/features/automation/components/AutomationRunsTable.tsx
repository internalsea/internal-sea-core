import { Link } from 'react-router-dom'

import { EntityReference } from '@/features/entity-picker/components/EntityReference'
import type { EntityPickerType } from '@/features/entity-picker/types'
import { AutomationActionTypeBadge } from '@/features/automation/components/AutomationActionTypeBadge'
import { AutomationRunStatusBadge } from '@/features/automation/components/AutomationRunStatusBadge'
import type { AutomationRun } from '@/features/automation/types'
import { formatDateTime } from '@/features/automation/utils'

interface AutomationRunsTableProps {
  items: AutomationRun[]
  showTriggerLink?: boolean
}

export function AutomationRunsTable({ items, showTriggerLink = true }: AutomationRunsTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No runs yet.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Action</th>
            <th className="px-3 py-2">Target</th>
            <th className="px-3 py-2">Started</th>
            <th className="px-3 py-2">Finished</th>
            <th className="px-3 py-2">Result</th>
            {showTriggerLink ? <th className="px-3 py-2">Trigger</th> : null}
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => (
            <tr key={item.id} className="text-gray-900">
              <td className="px-3 py-2">
                <AutomationRunStatusBadge status={item.status} />
              </td>
              <td className="px-3 py-2">
                {item.action_type ? (
                  <AutomationActionTypeBadge actionType={item.action_type} />
                ) : (
                  '—'
                )}
              </td>
              <td className="px-3 py-2">
                {item.target_type && item.target_id ? (
                  <EntityReference
                    entityType={item.target_type as EntityPickerType}
                    entityId={item.target_id}
                    showType
                    link
                  />
                ) : (
                  '—'
                )}
              </td>
              <td className="px-3 py-2">{formatDateTime(item.started_at)}</td>
              <td className="px-3 py-2">{formatDateTime(item.finished_at)}</td>
              <td className="px-3 py-2 max-w-xs truncate">{item.result_summary ?? item.error_message ?? '—'}</td>
              {showTriggerLink ? (
                <td className="px-3 py-2">
                  <Link
                    to={`/automation/triggers/${item.trigger_id}`}
                    className="text-core-blue hover:underline"
                  >
                    View
                  </Link>
                </td>
              ) : null}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
