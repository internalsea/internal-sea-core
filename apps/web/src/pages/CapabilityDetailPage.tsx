import { useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { CapabilityDetail } from '@/features/capabilities/components/CapabilityDetail'
import { useCapability, useCapabilitySummary } from '@/features/capabilities/hooks'
import { getApiErrorMessage } from '@/features/capabilities/utils'
import { ApiError } from '@/lib/apiClient'

export function CapabilityDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, isError, error } = useCapability(id)
  const {
    data: summary,
    isLoading: summaryLoading,
    isError: summaryError,
  } = useCapabilitySummary(id)

  if (isLoading) {
    return <LoadingState message="Loading capability…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Capability not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <CapabilityDetail
      capability={data}
      summary={summaryError ? undefined : summary}
      summaryLoading={summaryLoading}
    />
  )
}
