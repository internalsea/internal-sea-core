import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { NotificationPriorityBadge } from '@/features/notifications/components/NotificationPriorityBadge'
import { NotificationStatusBadge } from '@/features/notifications/components/NotificationStatusBadge'
import type { NotificationMessageListItem } from '@/features/notifications/types'
import { formatDateTime } from '@/features/notifications/utils'

interface NotificationMessagesTableProps {
  items: NotificationMessageListItem[]
  onDelete?: (item: NotificationMessageListItem) => void
  onQueue?: (item: NotificationMessageListItem) => void
}

export function NotificationMessagesTable({ items, onDelete, onQueue }: NotificationMessagesTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No notification messages found.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Subject</th>
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Priority</th>
            <th className="px-3 py-2">Recipient</th>
            <th className="px-3 py-2">Event</th>
            <th className="px-3 py-2">Scheduled</th>
            <th className="px-3 py-2">Delivered</th>
            <th className="px-3 py-2">Updated</th>
            <th className="px-3 py-2">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => (
            <tr key={item.id}>
              <td className="px-3 py-2">
                <Link
                  className="font-medium text-core-blue hover:underline"
                  to={`/notifications/messages/${item.id}`}
                >
                  {item.subject ?? 'Untitled message'}
                </Link>
              </td>
              <td className="px-3 py-2">
                <NotificationStatusBadge status={item.status} />
              </td>
              <td className="px-3 py-2">
                <NotificationPriorityBadge priority={item.priority} />
              </td>
              <td className="px-3 py-2">{item.recipient_value ?? '—'}</td>
              <td className="px-3 py-2">{item.event_type}</td>
              <td className="px-3 py-2">{formatDateTime(item.scheduled_at)}</td>
              <td className="px-3 py-2">
                {formatDateTime(item.sent_at ?? item.simulated_at)}
              </td>
              <td className="px-3 py-2">{formatDateTime(item.updated_at)}</td>
              <td className="px-3 py-2">
                <div className="flex gap-2">
                  <Link to={`/notifications/messages/${item.id}/edit`}>
                    <Button variant="secondary" size="sm">Edit</Button>
                  </Link>
                  <PermissionGate require="editor">
                    {onQueue && item.status === 'draft' ? (
                      <Button variant="secondary" size="sm" onClick={() => onQueue(item)}>
                        Queue
                      </Button>
                    ) : null}
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
