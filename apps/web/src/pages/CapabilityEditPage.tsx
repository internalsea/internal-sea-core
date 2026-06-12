import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { CapabilityForm } from '@/features/capabilities/components/CapabilityForm'
import { useCapability, useUpdateCapability } from '@/features/capabilities/hooks'
import { capabilityToFormValues, getApiErrorMessage } from '@/features/capabilities/utils'
import { ApiError } from '@/lib/apiClient'

export function CapabilityEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data, isLoading, isError, error } = useCapability(id)
  const updateMutation = useUpdateCapability()
  const [submitError, setSubmitError] = useState<string | null>(null)

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
    <div className="space-y-6">
      <PageHeader
        title="Edit Capability"
        description={data.name}
        actions={
          <Link to={`/capabilities/${data.id}`}>
            <Button variant="secondary">Back to detail</Button>
          </Link>
        }
      />

      <Card>
        <CapabilityForm
          mode="edit"
          initialValues={capabilityToFormValues(data)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/capabilities/${data.id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id: data.id, payload })
              navigate(`/capabilities/${data.id}`)
            } catch (err) {
              setSubmitError(getApiErrorMessage(err))
            }
          }}
        />
      </Card>
    </div>
  )
}
