import { useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { TeamDetail } from '@/features/teams/components/TeamDetail'
import { useTeam, useTeamSummary } from '@/features/teams/hooks'
import { getApiErrorMessage } from '@/features/teams/utils'
import { ApiError } from '@/lib/apiClient'

export function TeamDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, isError, error } = useTeam(id)
  const {
    data: summary,
    isLoading: summaryLoading,
    isError: summaryError,
  } = useTeamSummary(id)

  if (isLoading) {
    return <LoadingState message="Loading team…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Team not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <TeamDetail
      team={data}
      summary={summaryError ? undefined : summary}
      summaryLoading={summaryLoading}
    />
  )
}
