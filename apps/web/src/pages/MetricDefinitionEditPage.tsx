import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { MetricDefinitionForm } from '@/features/performance/components/MetricDefinitionForm'
import { useMetricDefinition, useUpdateMetricDefinition } from '@/features/performance/hooks'
import { definitionToFormValues, getApiErrorMessage } from '@/features/performance/utils'

export function MetricDefinitionEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const definitionQuery = useMetricDefinition(id)
  const updateMutation = useUpdateMetricDefinition()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (definitionQuery.isLoading) {
    return <LoadingState message="Loading metric definition…" />
  }

  if (definitionQuery.isError || !definitionQuery.data || !id) {
    return <ErrorState message={getApiErrorMessage(definitionQuery.error)} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Edit ${definitionQuery.data.name}`}
        actions={
          <Link to={`/performance/metrics/${id}`}>
            <Button variant="secondary">Back to detail</Button>
          </Link>
        }
      />
      <Card>
        <MetricDefinitionForm
          mode="edit"
          initialValues={definitionToFormValues(definitionQuery.data)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/performance/metrics/${id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id, payload })
              navigate(`/performance/metrics/${id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
