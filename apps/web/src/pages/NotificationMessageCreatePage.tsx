import { useMemo, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import { NotificationMessageForm } from '@/features/notifications/components/NotificationMessageForm'
import { useCreateNotificationMessage } from '@/features/notifications/hooks'
import { getApiErrorMessage } from '@/features/notifications/utils'

export function NotificationMessageCreatePage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const createMutation = useCreateNotificationMessage()
  const [submitError, setSubmitError] = useState<string | null>(null)

  const defaultEntity = useMemo<EntityPickerValue | null>(() => {
    const entityType = searchParams.get('entity_type')
    const entityId = searchParams.get('entity_id')
    if (!entityType || !entityId) return null
    return { entity_type: entityType as EntityPickerValue['entity_type'], entity_id: entityId }
  }, [searchParams])

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Notification Message"
        description="Compose a notification message for simulation or in-app delivery."
        actions={
          <Link to="/notifications">
            <Button variant="secondary">Back to Notifications</Button>
          </Link>
        }
      />
      <Card>
        <NotificationMessageForm
          defaultEntity={defaultEntity}
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/notifications')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/notifications/messages/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
