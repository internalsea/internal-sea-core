import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { ActivityTimeline } from '@/features/activity/components/ActivityTimeline'
import { useEntityActivity } from '@/features/activity/hooks'
import { getApiErrorMessage } from '@/features/activity/utils'

interface ActivitySectionProps {
  entityType: string
  entityId: string
  title?: string
}

export function ActivitySection({
  entityType,
  entityId,
  title = 'Activity',
}: ActivitySectionProps) {
  const { data, isLoading, isError, error } = useEntityActivity(entityType, entityId)

  return (
    <Card>
      <SectionHeader
        title={title}
        description="Read-only system history for create, update, delete and status changes."
      />
      {isLoading ? (
        <p className="text-sm text-gray-500">Loading activity…</p>
      ) : isError ? (
        <div className="rounded-md border border-status-dangerSoft bg-status-dangerSoft px-3 py-2 text-sm text-status-danger">
          {getApiErrorMessage(error)}
        </div>
      ) : (
        <ActivityTimeline events={data?.items ?? []} />
      )}
    </Card>
  )
}
