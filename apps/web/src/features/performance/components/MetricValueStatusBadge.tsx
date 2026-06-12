import { Badge } from '@/components/ui/Badge'
import { METRIC_VALUE_STATUS_BADGE } from '@/features/performance/constants'
import type { MetricValueStatus } from '@/features/performance/types'

interface MetricValueStatusBadgeProps {
  status: MetricValueStatus
}

export function MetricValueStatusBadge({ status }: MetricValueStatusBadgeProps) {
  return <Badge variant={METRIC_VALUE_STATUS_BADGE[status]}>{status}</Badge>
}
