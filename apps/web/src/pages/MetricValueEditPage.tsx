import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { MetricValueForm } from '@/features/performance/components/MetricValueForm'
import { useMetricValue, useUpdateMetricValue } from '@/features/performance/hooks'
import { getApiErrorMessage, valueToFormValues } from '@/features/performance/utils'

export function MetricValueEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const valueQuery = useMetricValue(id)
  const updateMutation = useUpdateMetricValue()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (valueQuery.isLoading) {
    return <LoadingState message="Loading metric value…" />
  }

  if (valueQuery.isError || !valueQuery.data || !id) {
    return <ErrorState message={getApiErrorMessage(valueQuery.error)} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit Metric Value"
        actions={
          <Link to="/performance">
            <Button variant="secondary">Back to Performance</Button>
          </Link>
        }
      />
      <Card>
        <MetricValueForm
          mode="edit"
          initialValues={valueToFormValues(valueQuery.data)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/performance')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id, payload })
              navigate('/performance')
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
