import { useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { PageHeader } from '@/components/ui/PageHeader'
import { AutomationTriggerDetail } from '@/features/automation/components/AutomationTriggerDetail'
import { useAutomationTrigger } from '@/features/automation/hooks'
import { getApiErrorMessage } from '@/features/automation/utils'
import { ApiError } from '@/lib/apiClient'

export function AutomationTriggerDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, isError, error } = useAutomationTrigger(id)

  if (isLoading) {
    return <LoadingState message="Loading automation trigger…" />
  }

  if (isError) {
    if (error instanceof ApiError && error.status === 404) {
      return <ErrorState title="Trigger not found" message="This automation trigger does not exist." />
    }
    return <ErrorState title="Failed to load trigger" message={getApiErrorMessage(error)} />
  }

  if (!data) {
    return null
  }

  return (
    <div className="space-y-6">
      <PageHeader title="Automation Trigger" description="Trigger details, configuration and run history." />
      <AutomationTriggerDetail trigger={data} />
    </div>
  )
}
