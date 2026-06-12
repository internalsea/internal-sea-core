import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { PolicyForm } from '@/features/compliance/components/PolicyForm'
import { usePolicy, useUpdatePolicy } from '@/features/compliance/hooks'
import { getApiErrorMessage, policyToFormValues } from '@/features/compliance/utils'
import { ApiError } from '@/lib/apiClient'

export function PolicyEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: policy, isLoading, isError, error } = usePolicy(id)
  const updateMutation = useUpdatePolicy()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) return <LoadingState message="Loading policy…" />
  if (isError || !policy) {
    const message = error instanceof ApiError && error.status === 404 ? 'Policy not found' : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Edit: ${policy.name}`}
        actions={<Link to={`/compliance/policies/${policy.id}`}><Button variant="secondary">Back to detail</Button></Link>}
      />
      <Card>
        <PolicyForm
          mode="edit"
          initialValues={policyToFormValues(policy)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/compliance/policies/${policy.id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id: policy.id, payload })
              navigate(`/compliance/policies/${policy.id}`)
            } catch (submitErr) {
              setSubmitError(getApiErrorMessage(submitErr))
            }
          }}
        />
      </Card>
    </div>
  )
}
