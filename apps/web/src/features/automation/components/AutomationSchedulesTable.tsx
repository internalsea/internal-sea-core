import { Link } from 'react-router-dom'

import type { AutomationScheduleListItem } from '@/features/automation/types'
import { formatDateTime, formatFrequency } from '@/features/automation/utils'

interface AutomationSchedulesTableProps {
  items: AutomationScheduleListItem[]
}

export function AutomationSchedulesTable({ items }: AutomationSchedulesTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No schedules yet.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Name</th>
            <th className="px-3 py-2">Frequency</th>
            <th className="px-3 py-2">Next Run</th>
            <th className="px-3 py-2">Last Run</th>
            <th className="px-3 py-2">Active</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => (
            <tr key={item.id} className="text-gray-900">
              <td className="px-3 py-2">
                <Link
                  to={`/automation/schedules/${item.id}/edit`}
                  className="font-medium text-core-blue hover:underline"
                >
                  {item.name}
                </Link>
              </td>
              <td className="px-3 py-2">{formatFrequency(item.frequency)}</td>
              <td className="px-3 py-2">{formatDateTime(item.next_run_at)}</td>
              <td className="px-3 py-2">{formatDateTime(item.last_run_at)}</td>
              <td className="px-3 py-2">{item.is_active ? 'Yes' : 'No'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
