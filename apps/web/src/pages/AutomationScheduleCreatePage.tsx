import { useNavigate } from 'react-router-dom'

import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { AutomationScheduleForm } from '@/features/automation/components/AutomationScheduleForm'
import { useCreateAutomationSchedule } from '@/features/automation/hooks'
import type { AutomationScheduleCreateInput } from '@/features/automation/types'
import { getApiErrorMessage } from '@/features/automation/utils'

export function AutomationScheduleCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateAutomationSchedule()

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Automation Schedule"
        description="Define recurrence settings for scheduled triggers."
      />
      <Card>
        <AutomationScheduleForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={createMutation.isError ? getApiErrorMessage(createMutation.error) : null}
          onSubmit={async (payload) => {
            await createMutation.mutateAsync(payload as AutomationScheduleCreateInput)
            navigate('/automation')
          }}
          onCancel={() => navigate('/automation')}
        />
      </Card>
    </div>
  )
}
