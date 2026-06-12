import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { MetricDefinitionForm } from '@/features/performance/components/MetricDefinitionForm'
import { useCreateMetricDefinition } from '@/features/performance/hooks'
import { getApiErrorMessage } from '@/features/performance/utils'

export function MetricDefinitionCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateMetricDefinition()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Metric Definition"
        description="Define what to measure and how to interpret performance."
        actions={
          <Link to="/performance">
            <Button variant="secondary">Back to Performance</Button>
          </Link>
        }
      />
      <Card>
        <MetricDefinitionForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/performance')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/performance/metrics/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
