import { useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { WorkItemDetail } from '@/features/work-items/components/WorkItemDetail'
import { useWorkItem } from '@/features/work-items/hooks'
import { getApiErrorMessage } from '@/features/work-items/utils'
import { ApiError } from '@/lib/apiClient'

export function WorkItemDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, isError, error } = useWorkItem(id)

  if (isLoading) {
    return <LoadingState message="Loading work item…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Work item not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return <WorkItemDetail workItem={data} />
}
