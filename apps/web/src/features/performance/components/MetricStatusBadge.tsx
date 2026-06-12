import { Badge } from '@/components/ui/Badge'
import { METRIC_STATUS_BADGE } from '@/features/performance/constants'
import type { MetricStatus } from '@/features/performance/types'

interface MetricStatusBadgeProps {
  status: MetricStatus
}

export function MetricStatusBadge({ status }: MetricStatusBadgeProps) {
  return <Badge variant={METRIC_STATUS_BADGE[status]}>{status.replace(/_/g, ' ')}</Badge>
}
