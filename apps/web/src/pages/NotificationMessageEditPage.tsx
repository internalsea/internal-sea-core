import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { NotificationMessageForm } from '@/features/notifications/components/NotificationMessageForm'
import { useNotificationMessage, useUpdateNotificationMessage } from '@/features/notifications/hooks'
import { getApiErrorMessage } from '@/features/notifications/utils'

export function NotificationMessageEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data, isLoading, isError } = useNotificationMessage(id)
  const updateMutation = useUpdateNotificationMessage()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) return <LoadingState message="Loading message…" />
  if (isError || !data || !id) return <ErrorState message="Message not found." />

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit notification message"
        description={data.subject ?? 'Update message content and recipients.'}
        actions={
          <Link to={`/notifications/messages/${id}`}>
            <Button variant="secondary">Back to message</Button>
          </Link>
        }
      />
      <Card>
        <NotificationMessageForm
          initial={data}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/notifications/messages/${id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id, payload })
              navigate(`/notifications/messages/${id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
