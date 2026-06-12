import { Link } from 'react-router-dom'

import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { formatCount, formatDateTime } from '@/features/dashboard/utils'
import type { NotificationHealth } from '@/features/dashboard/types'

interface NotificationHealthCardProps {
  data: NotificationHealth | undefined
  isLoading: boolean
  error: string | null
}

export function NotificationHealthCard({ data, isLoading, error }: NotificationHealthCardProps) {
  return (
    <DashboardSection
      title="Notification health"
      description="Queued messages and delivery failures."
      isLoading={isLoading}
      error={error}
      action={<Link to="/notifications" className="text-sm text-core-blue hover:underline">Notifications</Link>}
    >
      {data ? (
        <div className="space-y-4">
          <dl className="grid grid-cols-2 gap-3 text-sm">
            <div><dt className="text-gray-500">Queued</dt><dd className="font-semibold">{formatCount(data.messages_queued)}</dd></div>
            <div><dt className="text-gray-500">Failed</dt><dd className="font-semibold">{formatCount(data.messages_failed)}</dd></div>
            <div><dt className="text-gray-500">Failed attempts</dt><dd className="font-semibold">{formatCount(data.delivery_attempts_failed)}</dd></div>
          </dl>
          {data.recent_failed_messages.length > 0 ? (
            <ul className="divide-y divide-app-border text-sm">
              {data.recent_failed_messages.map((msg) => (
                <li key={msg.id} className="py-2 first:pt-0">
                  <Link to={`/notifications/messages/${msg.id}`} className="text-core-blue hover:underline">
                    {msg.subject ?? 'Untitled'}
                  </Link>
                  <p className="text-gray-600">{msg.error_message ?? 'Failed'} · {formatDateTime(msg.updated_at)}</p>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      ) : null}
    </DashboardSection>
  )
}
