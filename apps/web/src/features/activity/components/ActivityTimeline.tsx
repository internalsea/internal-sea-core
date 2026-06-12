import { EmptyState } from '@/components/ui/EmptyState'
import { ActivityTimelineItem } from '@/features/activity/components/ActivityTimelineItem'
import type { ActivityEvent } from '@/features/activity/types'

interface ActivityTimelineProps {
  events: ActivityEvent[]
}

export function ActivityTimeline({ events }: ActivityTimelineProps) {
  if (events.length === 0) {
    return (
      <EmptyState
        title="No activity yet"
        description="Create or update this record to see system-generated history."
      />
    )
  }

  return (
    <ol className="space-y-0">
      {events.map((event) => (
        <ActivityTimelineItem key={event.id} event={event} />
      ))}
    </ol>
  )
}
