import { Badge } from '@/components/ui/Badge'
import { channelTypeBadgeVariants } from '@/features/notifications/constants'
import type { NotificationChannelType } from '@/features/notifications/types'
import { formatChannelType } from '@/features/notifications/utils'

interface NotificationChannelTypeBadgeProps {
  channelType: NotificationChannelType | string
}

export function NotificationChannelTypeBadge({ channelType }: NotificationChannelTypeBadgeProps) {
  const normalized = channelType as NotificationChannelType
  return (
    <Badge variant={channelTypeBadgeVariants[normalized] ?? 'neutral'}>
      {formatChannelType(channelType)}
    </Badge>
  )
}
