import { Badge } from '@/components/ui/Badge'
import { AUTOMATION_RUN_STATUSES, automationRunStatusBadgeVariant } from '@/features/automation/constants'
import type { AutomationRunStatus } from '@/features/automation/types'

interface AutomationRunStatusBadgeProps {
  status: string
}

export function AutomationRunStatusBadge({ status }: AutomationRunStatusBadgeProps) {
  const label = AUTOMATION_RUN_STATUSES.find((item) => item.value === status)?.label ?? status
  const variant = automationRunStatusBadgeVariant[status as AutomationRunStatus] ?? 'neutral'
  return <Badge variant={variant}>{label}</Badge>
}
