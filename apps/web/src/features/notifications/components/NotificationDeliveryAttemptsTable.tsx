import { Badge } from '@/components/ui/Badge'
import { deliveryStatusBadgeVariants } from '@/features/notifications/constants'
import type { NotificationDeliveryAttempt, NotificationDeliveryStatus } from '@/features/notifications/types'
import { formatDateTime } from '@/features/notifications/utils'

interface NotificationDeliveryAttemptsTableProps {
  items: NotificationDeliveryAttempt[]
}

export function NotificationDeliveryAttemptsTable({ items }: NotificationDeliveryAttemptsTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No delivery attempts recorded.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">#</th>
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Provider</th>
            <th className="px-3 py-2">Started</th>
            <th className="px-3 py-2">Finished</th>
            <th className="px-3 py-2">Error</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => (
            <tr key={item.id}>
              <td className="px-3 py-2">{item.attempt_number}</td>
              <td className="px-3 py-2">
                <Badge variant={deliveryStatusBadgeVariants[item.status as NotificationDeliveryStatus] ?? 'neutral'}>
                  {item.status}
                </Badge>
              </td>
              <td className="px-3 py-2">{item.provider ?? '—'}</td>
              <td className="px-3 py-2">{formatDateTime(item.started_at)}</td>
              <td className="px-3 py-2">{formatDateTime(item.finished_at)}</td>
              <td className="px-3 py-2 text-status-danger">{item.error_message ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
