import { Link, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { PageHeader } from '@/components/ui/PageHeader'
import { NotificationTemplateDetail } from '@/features/notifications/components/NotificationTemplateDetail'
import { useNotificationTemplate } from '@/features/notifications/hooks'

export function NotificationTemplateDetailPage() {
  const { id } = useParams()
  const { data, isLoading, isError } = useNotificationTemplate(id)

  if (isLoading) return <LoadingState message="Loading template…" />
  if (isError || !data) return <ErrorState message="Template not found." />

  return (
    <div className="space-y-6">
      <PageHeader
        title={data.name}
        description="Notification template details and render preview."
        actions={
          <div className="flex gap-2">
            <Link to="/notifications">
              <Button variant="secondary">Back</Button>
            </Link>
            <Link to={`/notifications/templates/${data.id}/edit`}>
              <Button variant="secondary">Edit</Button>
            </Link>
          </div>
        }
      />
      <NotificationTemplateDetail template={data} />
    </div>
  )
}
