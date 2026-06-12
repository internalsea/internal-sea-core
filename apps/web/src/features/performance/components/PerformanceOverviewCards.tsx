import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import type { PerformanceOverview } from '@/features/performance/types'

interface PerformanceOverviewCardsProps {
  overview?: PerformanceOverview
  isLoading?: boolean
}

export function PerformanceOverviewCards({
  overview,
  isLoading = false,
}: PerformanceOverviewCardsProps) {
  if (isLoading) {
    return <LoadingState message="Loading performance overview…" />
  }

  if (!overview) return null

  const cards = [
    { label: 'Metric definitions', value: overview.metric_definitions_total },
    { label: 'Active definitions', value: overview.metric_definitions_active },
    { label: 'Recorded values', value: overview.metric_values_total },
    { label: 'Scorecards', value: overview.scorecards_available },
    { label: 'People metrics', value: overview.people_metrics_count },
    { label: 'Team metrics', value: overview.team_metrics_count },
    { label: 'Capability metrics', value: overview.capability_metrics_count },
    { label: 'Project metrics', value: overview.project_metrics_count },
    { label: 'Data product metrics', value: overview.data_product_metrics_count },
  ]

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {cards.map((card) => (
        <Card key={card.label}>
          <p className="text-xs font-medium uppercase tracking-wide text-gray-500">{card.label}</p>
          <p className="mt-2 text-2xl font-semibold text-gray-900">{card.value}</p>
        </Card>
      ))}
    </div>
  )
}
