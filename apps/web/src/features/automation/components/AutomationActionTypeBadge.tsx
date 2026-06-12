import { Badge } from '@/components/ui/Badge'
import { actionTypeBadgeVariant } from '@/features/automation/constants'
import { formatActionType } from '@/features/automation/utils'
import type { AutomationActionType } from '@/features/automation/types'

interface AutomationActionTypeBadgeProps {
  actionType: string
}

export function AutomationActionTypeBadge({ actionType }: AutomationActionTypeBadgeProps) {
  const variant = actionTypeBadgeVariant[actionType as AutomationActionType] ?? 'neutral'
  return <Badge variant={variant}>{formatActionType(actionType)}</Badge>
}
