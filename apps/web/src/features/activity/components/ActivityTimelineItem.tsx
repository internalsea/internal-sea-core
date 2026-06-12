import { Badge } from '@/components/ui/Badge'
import type { ActivityEvent } from '@/features/activity/types'
import {
  actionBadgeVariant,
  formatActionLabel,
  formatActorLabel,
  formatDateTime,
} from '@/features/activity/utils'

interface ActivityTimelineItemProps {
  event: ActivityEvent
}

export function ActivityTimelineItem({ event }: ActivityTimelineItemProps) {
  return (
    <li className="relative border-l border-app-border pl-4 pb-6 last:pb-0">
      <span className="absolute -left-1.5 top-1.5 h-3 w-3 rounded-full border border-app-border bg-white" />
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant={actionBadgeVariant(event.action)}>{formatActionLabel(event.action)}</Badge>
        <time className="text-xs text-gray-400" dateTime={event.created_at}>
          {formatDateTime(event.created_at)}
        </time>
      </div>
      <p className="mt-2 text-sm font-medium text-gray-900">{event.title}</p>
      {event.description ? (
        <p className="mt-1 text-sm text-gray-600">{event.description}</p>
      ) : null}
      <p className="mt-2 text-xs text-gray-500">{formatActorLabel(event.actor_id)}</p>
    </li>
  )
}
