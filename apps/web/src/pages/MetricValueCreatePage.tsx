import { useMemo, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { MetricValueForm } from '@/features/performance/components/MetricValueForm'
import { useCreateMetricValue } from '@/features/performance/hooks'
import type { PerformanceSubjectType } from '@/features/performance/types'
import { getApiErrorMessage } from '@/features/performance/utils'

export function MetricValueCreatePage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const createMutation = useCreateMetricValue()
  const [submitError, setSubmitError] = useState<string | null>(null)

  const initialValues = useMemo(() => {
    const subjectType = searchParams.get('subject_type') as PerformanceSubjectType | null
    const subjectId = searchParams.get('subject_id')
    if (!subjectType || !subjectId) return undefined
    return { subject_type: subjectType, subject_id: subjectId }
  }, [searchParams])

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Metric Value"
        description="Record a performance value for an entity and period."
        actions={
          <Link to="/performance">
            <Button variant="secondary">Back to Performance</Button>
          </Link>
        }
      />
      <Card>
        <MetricValueForm
          mode="create"
          initialValues={initialValues}
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/performance')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/performance/values/${created.id}/edit`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
