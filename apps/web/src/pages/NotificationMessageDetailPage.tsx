import { Link, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { PageHeader } from '@/components/ui/PageHeader'
import { NotificationMessageDetail } from '@/features/notifications/components/NotificationMessageDetail'
import { useNotificationMessage } from '@/features/notifications/hooks'

export function NotificationMessageDetailPage() {
  const { id } = useParams()
  const { data, isLoading, isError } = useNotificationMessage(id)

  if (isLoading) return <LoadingState message="Loading message…" />
  if (isError || !data) return <ErrorState message="Message not found." />

  return (
    <div className="space-y-6">
      <PageHeader
        title={data.subject ?? 'Notification message'}
        description="Message details, delivery attempts and simulation controls."
        actions={
          <Link to="/notifications">
            <Button variant="secondary">Back to Notifications</Button>
          </Link>
        }
      />
      <NotificationMessageDetail message={data} />
    </div>
  )
}
