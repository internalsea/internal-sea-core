import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import type { ProjectSummary } from '@/features/projects/types'

interface ProjectSummaryCardsProps {
  summary?: ProjectSummary
  isLoading?: boolean
}

const metrics = [
  { key: 'total_work_items', label: 'Total Work' },
  { key: 'open_work_items', label: 'Open' },
  { key: 'completed_work_items', label: 'Completed' },
  { key: 'overdue_work_items', label: 'Overdue' },
] as const

export function ProjectSummaryCards({ summary, isLoading = false }: ProjectSummaryCardsProps) {
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
