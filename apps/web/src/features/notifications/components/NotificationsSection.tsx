import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { NotificationMessagesTable } from '@/features/notifications/components/NotificationMessagesTable'
import { useEntityNotifications } from '@/features/notifications/hooks'
import { getApiErrorMessage } from '@/features/notifications/utils'

interface NotificationsSectionProps {
  entityType: string
  entityId: string
  title?: string
}

export function NotificationsSection({
  entityType,
  entityId,
  title = 'Notifications',
}: NotificationsSectionProps) {
  const { data, isLoading, isError, error } = useEntityNotifications(entityType, entityId)
  const newMessageUrl = `/notifications/messages/new?entity_type=${entityType}&entity_id=${entityId}`

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title={title}
          description="Notification messages linked to this record."
        />
        <div className="flex flex-wrap gap-2">
          <Link to="/notifications">
            <Button variant="secondary" size="sm">View notifications</Button>
          </Link>
          <PermissionGate require="editor">
            <Link to={newMessageUrl}>
              <Button variant="secondary" size="sm">New notification</Button>
            </Link>
          </PermissionGate>
        </div>
      </div>
      {isLoading ? (
        <p className="mt-4 text-sm text-gray-500">Loading notifications…</p>
      ) : isError ? (
        <p className="mt-4 text-sm text-status-danger">{getApiErrorMessage(error)}</p>
      ) : (
        <div className="mt-4">
          <NotificationMessagesTable items={data?.messages ?? []} />
        </div>
      )}
    </Card>
  )
}
