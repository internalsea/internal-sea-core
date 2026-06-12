import { Badge } from '@/components/ui/Badge'
import { TREND_BADGE } from '@/features/performance/constants'
import type { PerformanceTrend } from '@/features/performance/types'

interface TrendBadgeProps {
  trend: PerformanceTrend
}

export function TrendBadge({ trend }: TrendBadgeProps) {
  return <Badge variant={TREND_BADGE[trend]}>{trend}</Badge>
}
