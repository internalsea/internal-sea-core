import type { PerformanceScorecardMetric } from '@/features/performance/types'
import { formatMetricValue, formatScore } from '@/features/performance/utils'
import { TrendBadge } from '@/features/performance/components/TrendBadge'

interface ScorecardMetricListProps {
  metrics: PerformanceScorecardMetric[]
}

export function ScorecardMetricList({ metrics }: ScorecardMetricListProps) {
  if (metrics.length === 0) {
    return <p className="text-sm text-gray-500">No active metrics defined for this entity.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead>
          <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
            <th className="px-3 py-2">Metric</th>
            <th className="px-3 py-2">Current</th>
            <th className="px-3 py-2">Target</th>
            <th className="px-3 py-2">Score</th>
            <th className="px-3 py-2">Trend</th>
            <th className="px-3 py-2">Interpretation</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {metrics.map((metric) => (
            <tr key={metric.metric_definition_id}>
              <td className="px-3 py-2 font-medium text-gray-900">{metric.name}</td>
              <td className="px-3 py-2">
                {formatMetricValue(
                  metric.current_value_numeric,
                  metric.current_value_text,
                  metric.current_value_bool,
                  metric.unit,
                )}
              </td>
              <td className="px-3 py-2">
                {metric.target_value != null
                  ? formatMetricValue(metric.target_value, null, null, metric.unit)
                  : '—'}
              </td>
              <td className="px-3 py-2">{formatScore(metric.score)}</td>
              <td className="px-3 py-2">
                <TrendBadge trend={metric.trend} />
              </td>
              <td className="px-3 py-2 text-gray-600">{metric.interpretation ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
