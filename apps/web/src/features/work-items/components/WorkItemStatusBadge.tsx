import { Badge } from '@/components/ui/Badge'
import { workStatusVariantMap } from '@/lib/designTokens'
import { workItemStatusLabels } from '@/features/work-items/constants'
import type { WorkItemStatus } from '@/features/work-items/types'

interface WorkItemStatusBadgeProps {
  status: WorkItemStatus
}

export function WorkItemStatusBadge({ status }: WorkItemStatusBadgeProps) {
  return (
    <Badge variant={workStatusVariantMap[status] ?? 'neutral'}>
      {workItemStatusLabels[status]}
    </Badge>
  )
}
