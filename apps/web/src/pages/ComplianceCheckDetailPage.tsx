import { useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { ComplianceCheckDetail } from '@/features/compliance/components/ComplianceCheckDetail'
import { useComplianceCheck, useDeleteComplianceCheck } from '@/features/compliance/hooks'
import { confirmCheckDelete, getApiErrorMessage } from '@/features/compliance/utils'
import { ApiError } from '@/lib/apiClient'

export function ComplianceCheckDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: check, isLoading, isError, error } = useComplianceCheck(id)
  const deleteMutation = useDeleteComplianceCheck()

  if (isLoading) return <LoadingState message="Loading compliance check…" />
  if (isError || !check) {
    const message = error instanceof ApiError && error.status === 404 ? 'Check not found' : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <ComplianceCheckDetail
      check={check}
      onEdit={() => navigate(`/compliance/checks/${check.id}/edit`)}
      onDelete={async () => {
        if (!confirmCheckDelete(check.title)) return
        await deleteMutation.mutateAsync(check.id)
        navigate('/compliance')
      }}
    />
  )
}
