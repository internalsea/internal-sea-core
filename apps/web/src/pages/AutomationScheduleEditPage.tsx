import { useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { AutomationScheduleForm } from '@/features/automation/components/AutomationScheduleForm'
import { useAutomationSchedule, useUpdateAutomationSchedule } from '@/features/automation/hooks'
import { getApiErrorMessage, scheduleToFormValues } from '@/features/automation/utils'
import { ApiError } from '@/lib/apiClient'

export function AutomationScheduleEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data, isLoading, isError, error } = useAutomationSchedule(id)
  const updateMutation = useUpdateAutomationSchedule()

  if (isLoading) {
    return <LoadingState message="Loading schedule…" />
  }

  if (isError) {
    if (error instanceof ApiError && error.status === 404) {
      return <ErrorState title="Schedule not found" message="This automation schedule does not exist." />
    }
    return <ErrorState title="Failed to load schedule" message={getApiErrorMessage(error)} />
  }

  if (!data || !id) {
    return null
  }

  return (
    <div className="space-y-6">
      <PageHeader title="Edit Automation Schedule" description={data.name} />
      <Card>
        <AutomationScheduleForm
          mode="edit"
          initialValues={scheduleToFormValues(data)}
          isSubmitting={updateMutation.isPending}
          submitError={updateMutation.isError ? getApiErrorMessage(updateMutation.error) : null}
          onSubmit={async (payload) => {
            await updateMutation.mutateAsync({ id, payload })
            navigate('/automation')
          }}
          onCancel={() => navigate('/automation')}
        />
      </Card>
    </div>
  )
}
