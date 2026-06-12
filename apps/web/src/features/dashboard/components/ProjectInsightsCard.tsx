import { Link } from 'react-router-dom'

import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { HealthScoreBadge } from '@/features/dashboard/components/HealthScoreBadge'
import { formatCount, formatDate, formatScore } from '@/features/dashboard/utils'
import type { ProjectInsightItem } from '@/features/dashboard/types'

interface ProjectInsightsCardProps {
  data: { items: ProjectInsightItem[]; active: number; warning_or_critical: number } | undefined
  isLoading: boolean
  error: string | null
}

function projectHref(item: ProjectInsightItem): string {
  return item.project_type === 'internal_project'
    ? `/internal-projects/${item.id}`
    : `/projects/${item.id}`
}

export function ProjectInsightsCard({ data, isLoading, error }: ProjectInsightsCardProps) {
  return (
    <DashboardSection
      title="Project insights"
      description="Active projects with health, work and compliance signals."
      isLoading={isLoading}
      error={error}
      action={<Link to="/projects" className="text-sm text-core-blue hover:underline">All projects</Link>}
    >
      {data ? (
        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            {formatCount(data.active)} active · {formatCount(data.warning_or_critical)} warning/critical
          </p>
          <ul className="divide-y divide-app-border">
            {data.items.map((item) => (
              <li key={item.id} className="py-3 first:pt-0">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <Link to={projectHref(item)} className="font-medium text-core-blue hover:underline">
                    {item.name}
                  </Link>
                  <HealthScoreBadge status={item.insight_status} />
                </div>
                <p className="mt-1 text-xs text-gray-500">
                  {item.project_type} · ends {formatDate(item.target_end_date)}
                </p>
                <p className="mt-1 text-sm text-gray-600">
                  Open {item.open_work_items} · overdue {item.overdue_work_items} · risks {item.risks}
                  {item.performance_score != null ? ` · score ${formatScore(item.performance_score)}` : ''}
                </p>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </DashboardSection>
  )
}
