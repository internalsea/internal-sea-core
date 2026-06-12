import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { NotificationChannelTypeBadge } from '@/features/notifications/components/NotificationChannelTypeBadge'
import type { NotificationChannelListItem } from '@/features/notifications/types'
import { formatDateTime } from '@/features/notifications/utils'

interface NotificationChannelsTableProps {
  items: NotificationChannelListItem[]
  onEdit?: (item: NotificationChannelListItem) => void
  onDelete?: (item: NotificationChannelListItem) => void
}

export function NotificationChannelsTable({
  items,
  onEdit,
  onDelete,
}: NotificationChannelsTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No notification channels configured.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Name</th>
            <th className="px-3 py-2">Type</th>
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Default recipient</th>
            <th className="px-3 py-2">Updated</th>
            <th className="px-3 py-2">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => (
            <tr key={item.id}>
              <td className="px-3 py-2 font-medium">{item.name}</td>
              <td className="px-3 py-2">
                <NotificationChannelTypeBadge channelType={item.channel_type} />
              </td>
              <td className="px-3 py-2">{item.status}</td>
              <td className="px-3 py-2">{item.default_recipient ?? '—'}</td>
              <td className="px-3 py-2">{formatDateTime(item.updated_at)}</td>
              <td className="px-3 py-2">
                <PermissionGate require="editor">
                  <div className="flex gap-2">
                    {onEdit ? (
                      <Button variant="secondary" size="sm" onClick={() => onEdit(item)}>
                        Edit
                      </Button>
                    ) : null}
                    {onDelete ? (
                      <Button variant="secondary" size="sm" onClick={() => onDelete(item)}>
                        Delete
                      </Button>
                    ) : null}
                  </div>
                </PermissionGate>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
