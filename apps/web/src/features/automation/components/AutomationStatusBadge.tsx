import { Badge } from '@/components/ui/Badge'
import { AUTOMATION_STATUSES, automationStatusBadgeVariant } from '@/features/automation/constants'
import type { AutomationStatus } from '@/features/automation/types'

interface AutomationStatusBadgeProps {
  status: string
}

export function AutomationStatusBadge({ status }: AutomationStatusBadgeProps) {
  const label = AUTOMATION_STATUSES.find((item) => item.value === status)?.label ?? status
  const variant = automationStatusBadgeVariant[status as AutomationStatus] ?? 'neutral'
  return <Badge variant={variant}>{label}</Badge>
}
