import { Badge } from '@/components/ui/Badge'
import { getHealthVariant } from '@/features/dashboard/utils'
import type { HealthStatus } from '@/features/dashboard/types'

interface HealthScoreBadgeProps {
  status: HealthStatus | string
  label?: string
}

export function HealthScoreBadge({ status, label }: HealthScoreBadgeProps) {
  return (
    <Badge variant={getHealthVariant(status)}>
      {label ?? status}
    </Badge>
  )
}
