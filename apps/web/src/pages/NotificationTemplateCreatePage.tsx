import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { NotificationTemplateForm } from '@/features/notifications/components/NotificationTemplateForm'
import { useCreateNotificationTemplate } from '@/features/notifications/hooks'
import { getApiErrorMessage } from '@/features/notifications/utils'

export function NotificationTemplateCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateNotificationTemplate()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Notification Template"
        description="Create a reusable template with simple placeholders."
        actions={
          <Link to="/notifications">
            <Button variant="secondary">Back to Notifications</Button>
          </Link>
        }
      />
      <Card>
        <NotificationTemplateForm
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/notifications')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/notifications/templates/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
