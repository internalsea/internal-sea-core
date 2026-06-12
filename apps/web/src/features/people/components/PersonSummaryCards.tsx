import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import type { PersonSummary } from '@/features/people/types'

interface PersonSummaryCardsProps {
  summary?: PersonSummary
  isLoading?: boolean
}

const metrics = [
  { key: 'assigned_work_items', label: 'Assigned Work' },
  { key: 'owned_data_products_business', label: 'Business Products' },
  { key: 'owned_data_products_technical', label: 'Technical Products' },
  { key: 'owned_projects', label: 'Owned Projects' },
] as const

export function PersonSummaryCards({ summary, isLoading = false }: PersonSummaryCardsProps) {
  if (isLoading) {
    return <LoadingState message="Loading summary…" />
  }

  if (!summary) {
    return null
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric) => (
        <Card key={metric.key}>
          <p className="text-xs font-medium uppercase tracking-wide text-gray-500">{metric.label}</p>
          <p className="mt-2 text-2xl font-semibold text-gray-900">{summary[metric.key]}</p>
        </Card>
      ))}
    </div>
  )
}
