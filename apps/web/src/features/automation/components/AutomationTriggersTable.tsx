import { Link } from 'react-router-dom'

import { AutomationActionTypeBadge } from '@/features/automation/components/AutomationActionTypeBadge'
import { AutomationStatusBadge } from '@/features/automation/components/AutomationStatusBadge'
import type { AutomationTriggerListItem } from '@/features/automation/types'
import { formatDateTime, formatTriggerType } from '@/features/automation/utils'

interface AutomationTriggersTableProps {
  items: AutomationTriggerListItem[]
}

export function AutomationTriggersTable({ items }: AutomationTriggersTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No triggers yet.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Name</th>
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Type</th>
            <th className="px-3 py-2">Action</th>
            <th className="px-3 py-2">Last Run</th>
            <th className="px-3 py-2">Next Run</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => (
            <tr key={item.id} className="text-gray-900">
              <td className="px-3 py-2">
                <Link
                  to={`/automation/triggers/${item.id}`}
                  className="font-medium text-core-blue hover:underline"
                >
                  {item.name}
                </Link>
              </td>
              <td className="px-3 py-2">
                <AutomationStatusBadge status={item.status} />
              </td>
              <td className="px-3 py-2">{formatTriggerType(item.trigger_type)}</td>
              <td className="px-3 py-2">
                <AutomationActionTypeBadge actionType={item.action_type} />
              </td>
              <td className="px-3 py-2">{formatDateTime(item.last_run_at)}</td>
              <td className="px-3 py-2">{formatDateTime(item.next_run_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
