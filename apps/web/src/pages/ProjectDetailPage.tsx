import { useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { ProjectDetail } from '@/features/projects/components/ProjectDetail'
import { useProject, useProjectSummary } from '@/features/projects/hooks'
import { getApiErrorMessage } from '@/features/projects/utils'
import { ApiError } from '@/lib/apiClient'

export function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, isError, error } = useProject(id)
  const {
    data: summary,
    isLoading: summaryLoading,
    isError: summaryError,
  } = useProjectSummary(id)

  if (isLoading) {
    return <LoadingState message="Loading project…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Project not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <ProjectDetail
      project={data}
      summary={summaryError ? undefined : summary}
      summaryLoading={summaryLoading}
      variant="projects"
    />
  )
}
