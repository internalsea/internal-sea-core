import { useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { PersonDetail } from '@/features/people/components/PersonDetail'
import { usePerson, usePersonSummary } from '@/features/people/hooks'
import { getApiErrorMessage } from '@/features/people/utils'
import { ApiError } from '@/lib/apiClient'

export function PersonDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, isError, error } = usePerson(id)
  const {
    data: summary,
    isLoading: summaryLoading,
    isError: summaryError,
  } = usePersonSummary(id)

  if (isLoading) {
    return <LoadingState message="Loading person…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Person not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <PersonDetail
      person={data}
      summary={summaryError ? undefined : summary}
      summaryLoading={summaryLoading}
    />
  )
}
