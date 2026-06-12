import { useState } from 'react'
import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { NotificationDeliveryAttemptsTable } from '@/features/notifications/components/NotificationDeliveryAttemptsTable'
import { NotificationPriorityBadge } from '@/features/notifications/components/NotificationPriorityBadge'
import { NotificationStatusBadge } from '@/features/notifications/components/NotificationStatusBadge'
import { SendNotificationDialog } from '@/features/notifications/components/SendNotificationDialog'
import { useMessageDeliveryAttempts, useNotificationChannel } from '@/features/notifications/hooks'
import type { NotificationMessage } from '@/features/notifications/types'
import {
  canSendRealInMvp,
  formatDateTime,
  getNotificationEntityHref,
} from '@/features/notifications/utils'

interface NotificationMessageDetailProps {
  message: NotificationMessage
}

export function NotificationMessageDetail({ message }: NotificationMessageDetailProps) {
  const [showSendDialog, setShowSendDialog] = useState(false)
  const attemptsQuery = useMessageDeliveryAttempts(message.id)
  const channelQuery = useNotificationChannel(message.channel_id ?? undefined)
  const entityHref = getNotificationEntityHref(message.entity_type, message.entity_id)
  const canSendReal = canSendRealInMvp(channelQuery.data?.channel_type ?? null)

  return (
    <div className="space-y-6">
      <Card>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <SectionHeader
            title={message.subject ?? 'Notification message'}
            description={`Event: ${message.event_type}`}
          />
          <PermissionGate require="editor">
            <div className="flex gap-2">
              <Button onClick={() => setShowSendDialog(true)}>Send (simulation)</Button>
              <Button variant="secondary" disabled={!canSendReal} title={canSendReal ? undefined : 'Only in-app channels can be marked sent in MVP'}>
                Send real
              </Button>
              <Link to={`/notifications/messages/${message.id}/edit`}>
                <Button variant="secondary">Edit</Button>
              </Link>
            </div>
          </PermissionGate>
        </div>
        <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
          <div><dt className="text-gray-500">Status</dt><dd><NotificationStatusBadge status={message.status} /></dd></div>
          <div><dt className="text-gray-500">Priority</dt><dd><NotificationPriorityBadge priority={message.priority} /></dd></div>
          <div><dt className="text-gray-500">Recipient</dt><dd>{message.recipient_type ?? '—'} {message.recipient_value ?? ''}</dd></div>
          <div><dt className="text-gray-500">Entity</dt><dd>
            {entityHref ? <Link className="text-core-blue hover:underline" to={entityHref}>{message.entity_type}/{message.entity_id}</Link> : '—'}
          </dd></div>
          <div><dt className="text-gray-500">Simulated at</dt><dd>{formatDateTime(message.simulated_at)}</dd></div>
          <div><dt className="text-gray-500">Sent at</dt><dd>{formatDateTime(message.sent_at)}</dd></div>
        </dl>
        {message.error_message ? (
          <p className="mt-4 text-sm text-status-danger">{message.error_message}</p>
        ) : null}
        <div className="mt-4">
          <p className="text-sm font-medium text-gray-700">Body</p>
          <pre className="mt-2 whitespace-pre-wrap rounded-md bg-app-muted p-3 text-sm">{message.body}</pre>
        </div>
      </Card>

      <Card>
        <SectionHeader title="Delivery attempts" description="Simulation and delivery history for this message." />
        <div className="mt-4">
          <NotificationDeliveryAttemptsTable items={attemptsQuery.data?.items ?? []} />
        </div>
      </Card>

      {showSendDialog ? (
        <SendNotificationDialog
          messageId={message.id}
          onClose={() => setShowSendDialog(false)}
          onConfirm={() => setShowSendDialog(false)}
        />
      ) : null}
    </div>
  )
}
