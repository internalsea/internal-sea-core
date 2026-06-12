import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import type { NotificationTemplateListItem } from '@/features/notifications/types'
import { formatDateTime } from '@/features/notifications/utils'

interface NotificationTemplatesTableProps {
  items: NotificationTemplateListItem[]
  onDelete?: (item: NotificationTemplateListItem) => void
}

export function NotificationTemplatesTable({ items, onDelete }: NotificationTemplatesTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No notification templates found.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Name</th>
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Event type</th>
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
                  to={`/notifications/templates/${item.id}`}
                >
                  {item.name}
                </Link>
              </td>
              <td className="px-3 py-2">{item.status}</td>
              <td className="px-3 py-2">{item.event_type ?? '—'}</td>
              <td className="px-3 py-2">{formatDateTime(item.updated_at)}</td>
              <td className="px-3 py-2">
                <div className="flex gap-2">
                  <Link to={`/notifications/templates/${item.id}/edit`}>
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
