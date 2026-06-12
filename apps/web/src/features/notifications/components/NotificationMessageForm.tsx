import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import {
  NOTIFICATION_ENTITY_PICKER_TYPES,
  NOTIFICATION_EVENT_TYPES,
  NOTIFICATION_MESSAGE_STATUSES,
  NOTIFICATION_PRIORITIES,
  NOTIFICATION_RECIPIENT_TYPES,
} from '@/features/notifications/constants'
import {
  useNotificationChannels,
  useNotificationTemplates,
  useRenderNotificationTemplate,
} from '@/features/notifications/hooks'
import type {
  NotificationMessage,
  NotificationMessageCreateInput,
} from '@/features/notifications/types'
import { cleanMessagePayload, parseJsonField, stringifyJsonField } from '@/features/notifications/utils'

interface NotificationMessageFormProps {
  initial?: NotificationMessage | null
  isSubmitting?: boolean
  submitError?: string | null
  defaultEntity?: EntityPickerValue | null
  onSubmit: (values: NotificationMessageCreateInput) => Promise<void>
  onCancel?: () => void
}

export function NotificationMessageForm({
  initial,
  isSubmitting = false,
  submitError,
  defaultEntity = null,
  onSubmit,
  onCancel,
}: NotificationMessageFormProps) {
  const channelsQuery = useNotificationChannels({ page: 1, page_size: 100 })
  const templatesQuery = useNotificationTemplates({ page: 1, page_size: 100 })
  const renderMutation = useRenderNotificationTemplate()

  const [channelId, setChannelId] = useState(initial?.channel_id ?? '')
  const [templateId, setTemplateId] = useState(initial?.template_id ?? '')
  const [status, setStatus] = useState(initial?.status ?? 'draft')
  const [priority, setPriority] = useState(initial?.priority ?? 'normal')
  const [eventType, setEventType] = useState(initial?.event_type ?? 'manual')
  const [subject, setSubject] = useState(initial?.subject ?? '')
  const [body, setBody] = useState(initial?.body ?? '')
  const [recipientType, setRecipientType] = useState(initial?.recipient_type ?? 'email')
  const [recipientValue, setRecipientValue] = useState(initial?.recipient_value ?? '')
  const [entity, setEntity] = useState<EntityPickerValue | null>(
    initial?.entity_type && initial?.entity_id
      ? { entity_type: initial.entity_type as EntityPickerValue['entity_type'], entity_id: initial.entity_id }
      : defaultEntity,
  )
  const [scheduledAt, setScheduledAt] = useState(initial?.scheduled_at?.slice(0, 16) ?? '')
  const [metadataJson, setMetadataJson] = useState(stringifyJsonField(initial?.metadata))
  const [renderContextJson, setRenderContextJson] = useState('{\n  "title": "Demo title"\n}')
  const [localError, setLocalError] = useState<string | null>(null)

  async function handleRenderFromTemplate() {
    if (!templateId) {
      setLocalError('Select a template first')
      return
    }
    setLocalError(null)
    try {
      const context = parseJsonField(renderContextJson) ?? {}
      const result = await renderMutation.mutateAsync({ template_id: templateId, context })
      if (result.subject) setSubject(result.subject)
      setBody(result.body)
    } catch (error) {
      setLocalError(error instanceof Error ? error.message : 'Render failed')
    }
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setLocalError(null)
    try {
      await onSubmit(
        cleanMessagePayload({
          channel_id: channelId || null,
          template_id: templateId || null,
          status: status as NotificationMessageCreateInput['status'],
          priority: priority as NotificationMessageCreateInput['priority'],
          event_type: eventType as NotificationMessageCreateInput['event_type'],
          subject: subject || null,
          body,
          recipient_type: recipientType as NotificationMessageCreateInput['recipient_type'],
          recipient_value: recipientValue || null,
          entity_type: entity?.entity_type ?? null,
          entity_id: entity?.entity_id ?? null,
          scheduled_at: scheduledAt ? new Date(scheduledAt).toISOString() : null,
          metadata: parseJsonField(metadataJson),
        }),
      )
    } catch (error) {
      setLocalError(error instanceof Error ? error.message : 'Invalid form data')
    }
  }

  return (
    <form className="space-y-4" onSubmit={(event) => void handleSubmit(event)}>
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Channel</span>
        <select
          className="w-full rounded-md border border-app-border px-3 py-2 text-sm"
          value={channelId}
          onChange={(event) => setChannelId(event.target.value)}
        >
          <option value="">Select channel</option>
          {(channelsQuery.data?.items ?? []).map((channel) => (
            <option key={channel.id} value={channel.id}>{channel.name}</option>
          ))}
        </select>
      </label>
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Template (optional)</span>
        <select
          className="w-full rounded-md border border-app-border px-3 py-2 text-sm"
          value={templateId}
          onChange={(event) => setTemplateId(event.target.value)}
        >
          <option value="">No template</option>
          {(templatesQuery.data?.items ?? []).map((template) => (
            <option key={template.id} value={template.id}>{template.name}</option>
          ))}
        </select>
      </label>
      {templateId ? (
        <div className="rounded-md border border-app-border p-3">
          <p className="text-sm font-medium text-gray-700">Render from template</p>
          <textarea
            className="mt-2 w-full rounded-md border border-app-border px-3 py-2 font-mono text-xs"
            rows={3}
            value={renderContextJson}
            onChange={(event) => setRenderContextJson(event.target.value)}
          />
          <Button
            type="button"
            className="mt-2"
            size="sm"
            variant="secondary"
            onClick={() => void handleRenderFromTemplate()}
            disabled={renderMutation.isPending}
          >
            Render from template
          </Button>
        </div>
      ) : null}
      <div className="grid gap-4 sm:grid-cols-3">
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-gray-700">Status</span>
          <select className="w-full rounded-md border border-app-border px-3 py-2 text-sm" value={status} onChange={(e) => setStatus(e.target.value as typeof status)}>
            {NOTIFICATION_MESSAGE_STATUSES.map((value) => <option key={value} value={value}>{value}</option>)}
          </select>
        </label>
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-gray-700">Priority</span>
          <select className="w-full rounded-md border border-app-border px-3 py-2 text-sm" value={priority} onChange={(e) => setPriority(e.target.value as typeof priority)}>
            {NOTIFICATION_PRIORITIES.map((value) => <option key={value} value={value}>{value}</option>)}
          </select>
        </label>
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-gray-700">Event type</span>
          <select className="w-full rounded-md border border-app-border px-3 py-2 text-sm" value={eventType} onChange={(e) => setEventType(e.target.value as typeof eventType)}>
            {NOTIFICATION_EVENT_TYPES.map((value) => <option key={value} value={value}>{value}</option>)}
          </select>
        </label>
      </div>
      <Input label="Subject" value={subject} onChange={(event) => setSubject(event.target.value)} />
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Body</span>
        <textarea className="w-full rounded-md border border-app-border px-3 py-2 text-sm" rows={6} value={body} onChange={(e) => setBody(e.target.value)} required />
      </label>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-gray-700">Recipient type</span>
          <select className="w-full rounded-md border border-app-border px-3 py-2 text-sm" value={recipientType} onChange={(e) => setRecipientType(e.target.value as typeof recipientType)}>
            {NOTIFICATION_RECIPIENT_TYPES.map((value) => <option key={value} value={value}>{value}</option>)}
          </select>
        </label>
        <Input label="Recipient value" value={recipientValue} onChange={(e) => setRecipientValue(e.target.value)} />
      </div>
      <EntityPicker
        label="Related entity"
        value={entity}
        onChange={setEntity}
        allowedTypes={[...NOTIFICATION_ENTITY_PICKER_TYPES]}
      />
      <Input label="Scheduled at" type="datetime-local" value={scheduledAt} onChange={(e) => setScheduledAt(e.target.value)} />
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Metadata (JSON)</span>
        <textarea className="w-full rounded-md border border-app-border px-3 py-2 font-mono text-xs" rows={3} value={metadataJson} onChange={(e) => setMetadataJson(e.target.value)} />
      </label>
      {localError || submitError ? <p className="text-sm text-status-danger">{localError ?? submitError}</p> : null}
      <div className="flex gap-2">
        <Button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Saving…' : initial ? 'Update message' : 'Create message'}</Button>
        {onCancel ? <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button> : null}
      </div>
    </form>
  )
}
