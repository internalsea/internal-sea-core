import { Link } from 'react-router-dom'

import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { formatCount, formatScore } from '@/features/dashboard/utils'
import type { PerformanceInsights } from '@/features/dashboard/types'

interface PerformanceInsightsCardProps {
  data: PerformanceInsights | undefined
  isLoading: boolean
  error: string | null
}

export function PerformanceInsightsCard({ data, isLoading, error }: PerformanceInsightsCardProps) {
  return (
    <DashboardSection
      title="Performance insights"
      description="Metric coverage and weak scorecards."
      isLoading={isLoading}
      error={error}
      action={<Link to="/performance" className="text-sm text-core-blue hover:underline">Performance</Link>}
    >
      {data ? (
        <div className="space-y-4">
          <dl className="grid grid-cols-2 gap-3 text-sm">
            <div><dt className="text-gray-500">Active metrics</dt><dd className="font-semibold">{formatCount(data.metric_definitions_active)}</dd></div>
            <div><dt className="text-gray-500">Avg score</dt><dd className="font-semibold">{formatScore(data.average_score)}</dd></div>
            <div><dt className="text-gray-500">Weak scorecards</dt><dd className="font-semibold">{formatCount(data.weak_scorecards_count)}</dd></div>
          </dl>
          {data.top_metric_gaps.length > 0 ? (
            <ul className="divide-y divide-app-border text-sm">
              {data.top_metric_gaps.map((gap) => (
                <li key={`${gap.metric_definition_id}-${gap.subject_id}`} className="py-2 first:pt-0">
                  <p className="font-medium text-gray-900">{gap.metric_name}</p>
                  <p className="text-gray-600">
                    Score {formatScore(gap.score)} · current {gap.current_value ?? '—'} / target {gap.target_value ?? '—'}
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-gray-500">No significant metric gaps.</p>
          )}
        </div>
      ) : null}
    </DashboardSection>
  )
}
