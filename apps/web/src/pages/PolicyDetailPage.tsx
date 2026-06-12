import { useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { PolicyDetail } from '@/features/compliance/components/PolicyDetail'
import { useDeletePolicy, usePolicy } from '@/features/compliance/hooks'
import { confirmPolicyDelete, getApiErrorMessage } from '@/features/compliance/utils'
import { ApiError } from '@/lib/apiClient'

export function PolicyDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: policy, isLoading, isError, error } = usePolicy(id)
  const deleteMutation = useDeletePolicy()

  if (isLoading) return <LoadingState message="Loading policy…" />
  if (isError || !policy) {
    const message = error instanceof ApiError && error.status === 404 ? 'Policy not found' : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <PolicyDetail
      policy={policy}
      onEdit={() => navigate(`/compliance/policies/${policy.id}/edit`)}
      onDelete={async () => {
        if (!confirmPolicyDelete(policy.name)) return
        await deleteMutation.mutateAsync(policy.id)
        navigate('/compliance')
      }}
    />
  )
}
