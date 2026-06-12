import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { ComplianceCheckForm } from '@/features/compliance/components/ComplianceCheckForm'
import { useComplianceCheck, useUpdateComplianceCheck } from '@/features/compliance/hooks'
import { checkToFormValues, getApiErrorMessage } from '@/features/compliance/utils'
import { ApiError } from '@/lib/apiClient'

export function ComplianceCheckEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: check, isLoading, isError, error } = useComplianceCheck(id)
  const updateMutation = useUpdateComplianceCheck()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) return <LoadingState message="Loading compliance check…" />
  if (isError || !check) {
    const message = error instanceof ApiError && error.status === 404 ? 'Check not found' : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Edit: ${check.title}`}
        actions={<Link to={`/compliance/checks/${check.id}`}><Button variant="secondary">Back to detail</Button></Link>}
      />
      <Card>
        <ComplianceCheckForm
          mode="edit"
          initialValues={checkToFormValues(check)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/compliance/checks/${check.id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id: check.id, payload })
              navigate(`/compliance/checks/${check.id}`)
            } catch (submitErr) {
              setSubmitError(getApiErrorMessage(submitErr))
            }
          }}
        />
      </Card>
    </div>
  )
}
