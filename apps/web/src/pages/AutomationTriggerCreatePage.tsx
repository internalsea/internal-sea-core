import { useMemo } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import { AutomationTriggerForm } from '@/features/automation/components/AutomationTriggerForm'
import { useCreateAutomationTrigger } from '@/features/automation/hooks'
import type { AutomationTriggerCreateInput } from '@/features/automation/types'
import { getApiErrorMessage } from '@/features/automation/utils'

export function AutomationTriggerCreatePage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const createMutation = useCreateAutomationTrigger()

  const lockTarget = useMemo<EntityPickerValue | undefined>(() => {
    const targetType = searchParams.get('target_type')
    const targetId = searchParams.get('target_id')
    if (!targetType || !targetId) {
      return undefined
    }
    return { entity_type: targetType as EntityPickerValue['entity_type'], entity_id: targetId }
  }, [searchParams])

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Automation Trigger"
        description="Define when and what the automation should do for a target object."
      />
      <Card>
        <AutomationTriggerForm
          mode="create"
          lockTarget={lockTarget}
          isSubmitting={createMutation.isPending}
          submitError={createMutation.isError ? getApiErrorMessage(createMutation.error) : null}
          onSubmit={async (payload) => {
            const trigger = await createMutation.mutateAsync(payload as AutomationTriggerCreateInput)
            navigate(`/automation/triggers/${trigger.id}`)
          }}
          onCancel={() => navigate('/automation')}
        />
      </Card>
    </div>
  )
}
