import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { NotificationTemplateForm } from '@/features/notifications/components/NotificationTemplateForm'
import { useNotificationTemplate, useUpdateNotificationTemplate } from '@/features/notifications/hooks'
import { getApiErrorMessage } from '@/features/notifications/utils'

export function NotificationTemplateEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data, isLoading, isError } = useNotificationTemplate(id)
  const updateMutation = useUpdateNotificationTemplate()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) return <LoadingState message="Loading template…" />
  if (isError || !data || !id) return <ErrorState message="Template not found." />

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Edit ${data.name}`}
        description="Update notification template content."
        actions={
          <Link to={`/notifications/templates/${id}`}>
            <Button variant="secondary">Back to template</Button>
          </Link>
        }
      />
      <Card>
        <NotificationTemplateForm
          initial={data}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/notifications/templates/${id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id, payload })
              navigate(`/notifications/templates/${id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
