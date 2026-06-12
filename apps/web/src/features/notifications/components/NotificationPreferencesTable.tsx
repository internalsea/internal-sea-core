import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import type { NotificationPreference } from '@/features/notifications/types'
import { formatChannelType } from '@/features/notifications/utils'

interface NotificationPreferencesTableProps {
  items: NotificationPreference[]
  onToggle?: (item: NotificationPreference) => void
  onDelete?: (item: NotificationPreference) => void
}

export function NotificationPreferencesTable({
  items,
  onToggle,
  onDelete,
}: NotificationPreferencesTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No notification preferences configured.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">User</th>
            <th className="px-3 py-2">Person</th>
            <th className="px-3 py-2">Channel</th>
            <th className="px-3 py-2">Event</th>
            <th className="px-3 py-2">Enabled</th>
            <th className="px-3 py-2">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {items.map((item) => (
            <tr key={item.id}>
              <td className="px-3 py-2 font-mono text-xs">{item.user_id ?? '—'}</td>
              <td className="px-3 py-2 font-mono text-xs">{item.person_id ?? '—'}</td>
              <td className="px-3 py-2">{formatChannelType(item.channel_type)}</td>
              <td className="px-3 py-2">{item.event_type}</td>
              <td className="px-3 py-2">{item.is_enabled ? 'Yes' : 'No'}</td>
              <td className="px-3 py-2">
                <PermissionGate require="editor">
                  <div className="flex gap-2">
                    {onToggle ? (
                      <Button variant="secondary" size="sm" onClick={() => onToggle(item)}>
                        Toggle
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
