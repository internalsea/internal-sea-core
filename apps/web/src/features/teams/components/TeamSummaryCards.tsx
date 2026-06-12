import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import type { TeamSummary } from '@/features/teams/types'

interface TeamSummaryCardsProps {
  summary?: TeamSummary
  isLoading?: boolean
}

const metrics = [
  { key: 'people_count', label: 'People' },
  { key: 'active_people_count', label: 'Active People' },
  { key: 'data_products_count', label: 'Data Products' },
  { key: 'open_work_items_count', label: 'Open Work' },
  { key: 'projects_count', label: 'Projects' },
  { key: 'internal_projects_count', label: 'Internal Projects' },
] as const

export function TeamSummaryCards({ summary, isLoading = false }: TeamSummaryCardsProps) {
  if (isLoading) {
    return <LoadingState message="Loading summary…" />
  }

  if (!summary) {
    return null
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {metrics.map((metric) => (
        <Card key={metric.key}>
          <p className="text-xs font-medium uppercase tracking-wide text-gray-500">{metric.label}</p>
          <p className="mt-2 text-2xl font-semibold text-gray-900">{summary[metric.key]}</p>
        </Card>
      ))}
    </div>
  )
}
