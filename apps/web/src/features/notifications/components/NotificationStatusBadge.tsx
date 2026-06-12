import { Badge } from '@/components/ui/Badge'
import { messageStatusBadgeVariants } from '@/features/notifications/constants'
import type { NotificationMessageStatus } from '@/features/notifications/types'
import { formatMessageStatus } from '@/features/notifications/utils'

interface NotificationStatusBadgeProps {
  status: NotificationMessageStatus | string
}

export function NotificationStatusBadge({ status }: NotificationStatusBadgeProps) {
  const normalized = status as NotificationMessageStatus
  return (
    <Badge variant={messageStatusBadgeVariants[normalized] ?? 'neutral'}>
      {formatMessageStatus(status)}
    </Badge>
  )
}
