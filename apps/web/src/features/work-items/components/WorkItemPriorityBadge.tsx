import { Badge } from '@/components/ui/Badge'
import { priorityVariantMap } from '@/lib/designTokens'
import { workItemPriorityLabels } from '@/features/work-items/constants'
import type { WorkItemPriority } from '@/features/work-items/types'

interface WorkItemPriorityBadgeProps {
  priority: WorkItemPriority
}

export function WorkItemPriorityBadge({ priority }: WorkItemPriorityBadgeProps) {
  return (
    <Badge variant={priorityVariantMap[priority] ?? 'neutral'}>
      {workItemPriorityLabels[priority]}
    </Badge>
  )
}
