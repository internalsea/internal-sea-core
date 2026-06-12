import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import {
  NOTIFICATION_CHANNEL_TYPES,
  NOTIFICATION_EVENT_TYPES,
} from '@/features/notifications/constants'
import type { NotificationPreferenceCreateInput } from '@/features/notifications/types'
import { cleanPreferencePayload } from '@/features/notifications/utils'

interface NotificationPreferenceFormProps {
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: NotificationPreferenceCreateInput) => Promise<void>
}

export function NotificationPreferenceForm({
  isSubmitting = false,
  submitError,
  onSubmit,
}: NotificationPreferenceFormProps) {
  const [userId, setUserId] = useState('')
  const [person, setPerson] = useState<EntityPickerValue | null>(null)
  const [channelType, setChannelType] = useState('in_app')
  const [eventType, setEventType] = useState('manual')
  const [isEnabled, setIsEnabled] = useState(true)

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    await onSubmit(
      cleanPreferencePayload({
        user_id: userId || null,
        person_id: person?.entity_id ?? null,
        channel_type: channelType as NotificationPreferenceCreateInput['channel_type'],
        event_type: eventType as NotificationPreferenceCreateInput['event_type'],
        is_enabled: isEnabled,
      }),
    )
  }

  return (
    <form className="space-y-4" onSubmit={(event) => void handleSubmit(event)}>
      <Input
        label="User ID (optional)"
        value={userId}
        onChange={(event) => setUserId(event.target.value)}
      />
      <EntityPicker
        label="Person (optional)"
        value={person}
        onChange={setPerson}
        allowedTypes={['person']}
      />
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Channel type</span>
        <select className="w-full rounded-md border border-app-border px-3 py-2 text-sm" value={channelType} onChange={(e) => setChannelType(e.target.value)}>
          {NOTIFICATION_CHANNEL_TYPES.map((value) => <option key={value} value={value}>{value}</option>)}
        </select>
      </label>
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Event type</span>
        <select className="w-full rounded-md border border-app-border px-3 py-2 text-sm" value={eventType} onChange={(e) => setEventType(e.target.value)}>
          {NOTIFICATION_EVENT_TYPES.map((value) => <option key={value} value={value}>{value}</option>)}
        </select>
      </label>
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" checked={isEnabled} onChange={(e) => setIsEnabled(e.target.checked)} />
        Enabled
      </label>
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}
      <Button type="submit" disabled={isSubmitting}>Add preference</Button>
    </form>
  )
}
