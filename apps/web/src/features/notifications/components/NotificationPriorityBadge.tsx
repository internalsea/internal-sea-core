import { Badge } from '@/components/ui/Badge'
import { priorityBadgeVariants } from '@/features/notifications/constants'
import type { NotificationPriority } from '@/features/notifications/types'
import { formatPriority } from '@/features/notifications/utils'

interface NotificationPriorityBadgeProps {
  priority: NotificationPriority | string
}

export function NotificationPriorityBadge({ priority }: NotificationPriorityBadgeProps) {
  const normalized = priority as NotificationPriority
  return (
    <Badge variant={priorityBadgeVariants[normalized] ?? 'neutral'}>
      {formatPriority(priority)}
    </Badge>
  )
}
