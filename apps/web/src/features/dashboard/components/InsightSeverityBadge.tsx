import { Badge } from '@/components/ui/Badge'
import { getSeverityVariant } from '@/features/dashboard/utils'
import type { InsightSeverity } from '@/features/dashboard/types'

interface InsightSeverityBadgeProps {
  severity: InsightSeverity | string
}

export function InsightSeverityBadge({ severity }: InsightSeverityBadgeProps) {
  return <Badge variant={getSeverityVariant(severity)}>{severity}</Badge>
}
