import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import type { NotificationOverview } from '@/features/notifications/types'
import { getApiErrorMessage } from '@/features/notifications/utils'

interface NotificationOverviewCardsProps {
  overview?: NotificationOverview
  isLoading?: boolean
  error?: unknown
}

export function NotificationOverviewCards({
  overview,
  isLoading = false,
  error,
}: NotificationOverviewCardsProps) {
  if (isLoading) return <LoadingState message="Loading notification overview…" />
  if (error) return <p className="text-sm text-status-danger">{getApiErrorMessage(error)}</p>
  if (!overview) return null

  const cards = [
    { label: 'Active Channels', value: overview.channels_active, sub: `${overview.channels_total} total` },
    { label: 'Active Templates', value: overview.templates_active, sub: `${overview.templates_total} total` },
    { label: 'Messages', value: overview.messages_total, sub: `${overview.messages_simulated} simulated` },
    { label: 'Sent', value: overview.messages_sent, sub: 'In-app delivered' },
    { label: 'Failed', value: overview.messages_failed, sub: 'Needs review' },
    { label: 'Delivery Attempts', value: overview.delivery_attempts_total, sub: `${overview.delivery_attempts_failed} failed` },
  ]

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {cards.map((card) => (
        <Card key={card.label}>
          <p className="text-xs font-medium text-gray-500">{card.label}</p>
          <p className="mt-1 text-2xl font-semibold text-gray-900">{card.value}</p>
          <p className="mt-1 text-xs text-gray-500">{card.sub}</p>
        </Card>
      ))}
    </div>
  )
}
