import { useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import { AutomationTriggerForm } from '@/features/automation/components/AutomationTriggerForm'
import { useAutomationTrigger, useUpdateAutomationTrigger } from '@/features/automation/hooks'
import { getApiErrorMessage, triggerToFormValues } from '@/features/automation/utils'
import { ApiError } from '@/lib/apiClient'

export function AutomationTriggerEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data, isLoading, isError, error } = useAutomationTrigger(id)
  const updateMutation = useUpdateAutomationTrigger()

  if (isLoading) {
    return <LoadingState message="Loading trigger…" />
  }

  if (isError) {
    if (error instanceof ApiError && error.status === 404) {
      return <ErrorState title="Trigger not found" message="This automation trigger does not exist." />
    }
    return <ErrorState title="Failed to load trigger" message={getApiErrorMessage(error)} />
  }

  if (!data || !id) {
    return null
  }

  const initialTarget: EntityPickerValue | null =
    data.target_type && data.target_id
      ? { entity_type: data.target_type as EntityPickerValue['entity_type'], entity_id: data.target_id }
      : null

  return (
    <div className="space-y-6">
      <PageHeader title="Edit Automation Trigger" description={data.name} />
      <Card>
        <AutomationTriggerForm
          mode="edit"
          initialValues={triggerToFormValues(data)}
          initialTarget={initialTarget}
          isSubmitting={updateMutation.isPending}
          submitError={updateMutation.isError ? getApiErrorMessage(updateMutation.error) : null}
          onSubmit={async (payload) => {
            await updateMutation.mutateAsync({ id, payload })
            navigate(`/automation/triggers/${id}`)
          }}
          onCancel={() => navigate(`/automation/triggers/${id}`)}
        />
      </Card>
    </div>
  )
}
