import { useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { ProjectDetail } from '@/features/projects/components/ProjectDetail'
import { useInternalProject, useProjectSummary } from '@/features/projects/hooks'
import { getApiErrorMessage } from '@/features/projects/utils'
import { ApiError } from '@/lib/apiClient'

export function InternalProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, isError, error } = useInternalProject(id)
  const {
    data: summary,
    isLoading: summaryLoading,
    isError: summaryError,
  } = useProjectSummary(id)

  if (isLoading) {
    return <LoadingState message="Loading internal project…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Internal project not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <ProjectDetail
      project={data}
      summary={summaryError ? undefined : summary}
      summaryLoading={summaryLoading}
      variant="internal-projects"
    />
  )
}
