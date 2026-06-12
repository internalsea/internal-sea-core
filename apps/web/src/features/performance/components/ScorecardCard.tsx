import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import type { PerformanceScorecard } from '@/features/performance/types'
import { formatDateTime, formatScore, getHealthVariantFromScore } from '@/features/performance/utils'

interface ScorecardCardProps {
  scorecard: PerformanceScorecard
}

export function ScorecardCard({ scorecard }: ScorecardCardProps) {
  const healthVariant = getHealthVariantFromScore(scorecard.average_score)

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <Card>
        <p className="text-xs font-medium uppercase tracking-wide text-gray-500">Average score</p>
        <p className="mt-2 text-2xl font-semibold text-gray-900">
          {formatScore(scorecard.average_score)}
        </p>
      </Card>
      <Card>
        <p className="text-xs font-medium uppercase tracking-wide text-gray-500">Health</p>
        <div className="mt-2">
          <Badge variant={healthVariant}>{scorecard.health_status ?? 'unknown'}</Badge>
        </div>
      </Card>
      <Card>
        <p className="text-xs font-medium uppercase tracking-wide text-gray-500">Metrics</p>
        <p className="mt-2 text-2xl font-semibold text-gray-900">
          {scorecard.metrics_with_values}/{scorecard.metrics_total}
        </p>
      </Card>
      <Card>
        <p className="text-xs font-medium uppercase tracking-wide text-gray-500">Updated</p>
        <p className="mt-2 text-sm text-gray-700">{formatDateTime(scorecard.updated_at)}</p>
      </Card>
    </div>
  )
}
