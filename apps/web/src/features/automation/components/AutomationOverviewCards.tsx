import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import type { AutomationOverview } from '@/features/automation/types'
import { getApiErrorMessage } from '@/features/automation/utils'

interface AutomationOverviewCardsProps {
  overview?: AutomationOverview
  isLoading?: boolean
  error?: unknown
}

export function AutomationOverviewCards({
  overview,
  isLoading = false,
  error,
}: AutomationOverviewCardsProps) {
  if (isLoading) {
    return <LoadingState message="Loading automation overview…" />
  }

  if (error) {
    return <p className="text-sm text-status-danger">{getApiErrorMessage(error)}</p>
  }

  if (!overview) {
    return null
  }

  const cards = [
    { label: 'Active Schedules', value: overview.schedules_active, sub: `${overview.schedules_total} total` },
    { label: 'Active Triggers', value: overview.triggers_active, sub: `${overview.triggers_total} total` },
    { label: 'Paused Triggers', value: overview.triggers_paused, sub: 'Manual review' },
    { label: 'Upcoming Runs', value: overview.next_runs_count, sub: 'Scheduled triggers' },
    { label: 'Succeeded Runs', value: overview.runs_succeeded, sub: `${overview.runs_total} total` },
    { label: 'Failed Runs', value: overview.runs_failed, sub: 'Needs attention' },
    { label: 'Simulated Runs', value: overview.runs_simulated, sub: 'Preview only' },
  ]

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => (
        <Card key={card.label}>
          <p className="text-xs font-medium text-gray-500">{card.label}</p>
          <p className="mt-1 text-2xl font-semibold text-gray-900">{card.value}</p>
          <p className="mt-1 text-xs text-gray-500">{card.sub}</p>
        </Card>
      ))}
    </div>
  )
}
