import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { WorkItemForm } from '@/features/work-items/components/WorkItemForm'
import { useUpdateWorkItem, useWorkItem } from '@/features/work-items/hooks'
import { getApiErrorMessage, workItemToFormValues } from '@/features/work-items/utils'
import { ApiError } from '@/lib/apiClient'

export function WorkItemEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data, isLoading, isError, error } = useWorkItem(id)
  const updateMutation = useUpdateWorkItem()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) {
    return <LoadingState message="Loading work item…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Work item not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit Work Item"
        description={data.title}
        actions={
          <Link to={`/work-items/${data.id}`}>
            <Button variant="secondary">Back to detail</Button>
          </Link>
        }
      />

      <Card>
        <WorkItemForm
          mode="edit"
          initialValues={workItemToFormValues(data)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/work-items/${data.id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id: data.id, payload })
              navigate(`/work-items/${data.id}`)
            } catch (submitErr) {
              setSubmitError(getApiErrorMessage(submitErr))
            }
          }}
        />
      </Card>
    </div>
  )
}
