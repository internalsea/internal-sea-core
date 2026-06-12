import { Badge } from '@/components/ui/Badge'
import { workItemTypeVariantMap } from '@/lib/designTokens'
import { workItemTypeLabels } from '@/features/work-items/constants'
import type { WorkItemType } from '@/features/work-items/types'

interface WorkItemTypeBadgeProps {
  type: WorkItemType
}

export function WorkItemTypeBadge({ type }: WorkItemTypeBadgeProps) {
  return (
    <Badge variant={workItemTypeVariantMap[type] ?? 'neutral'}>
      {workItemTypeLabels[type]}
    </Badge>
  )
}
