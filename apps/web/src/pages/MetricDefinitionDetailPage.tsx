import { Link, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { PageHeader } from '@/components/ui/PageHeader'
import { MetricDefinitionDetail } from '@/features/performance/components/MetricDefinitionDetail'
import { useMetricDefinition, useMetricValues } from '@/features/performance/hooks'
import { getApiErrorMessage } from '@/features/performance/utils'

export function MetricDefinitionDetailPage() {
  const { id } = useParams<{ id: string }>()
  const definitionQuery = useMetricDefinition(id)
  const valuesQuery = useMetricValues({
    metric_definition_id: id,
    page: 1,
    page_size: 10,
  })

  if (definitionQuery.isLoading) {
    return <LoadingState message="Loading metric definition…" />
  }

  if (definitionQuery.isError || !definitionQuery.data) {
    return <ErrorState message={getApiErrorMessage(definitionQuery.error)} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={definitionQuery.data.name}
        description={definitionQuery.data.code ?? undefined}
        actions={
          <Link to="/performance">
            <Button variant="secondary">Back to Performance</Button>
          </Link>
        }
      />
      <MetricDefinitionDetail
        definition={definitionQuery.data}
        recentValues={valuesQuery.data?.items ?? []}
      />
    </div>
  )
}
