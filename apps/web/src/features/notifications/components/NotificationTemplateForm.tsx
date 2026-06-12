import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import {
  NOTIFICATION_EVENT_TYPES,
  NOTIFICATION_TEMPLATE_STATUSES,
  TEMPLATE_PLACEHOLDER_HELP,
} from '@/features/notifications/constants'
import type {
  NotificationTemplate,
  NotificationTemplateCreateInput,
} from '@/features/notifications/types'
import { cleanTemplatePayload } from '@/features/notifications/utils'

interface NotificationTemplateFormProps {
  initial?: NotificationTemplate | null
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: NotificationTemplateCreateInput) => Promise<void>
  onCancel?: () => void
}

export function NotificationTemplateForm({
  initial,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: NotificationTemplateFormProps) {
  const [name, setName] = useState(initial?.name ?? '')
  const [status, setStatus] = useState(initial?.status ?? 'draft')
  const [eventType, setEventType] = useState(initial?.event_type ?? 'manual')
  const [subjectTemplate, setSubjectTemplate] = useState(initial?.subject_template ?? '')
  const [bodyTemplate, setBodyTemplate] = useState(initial?.body_template ?? '')
  const [description, setDescription] = useState(initial?.description ?? '')

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    await onSubmit(
      cleanTemplatePayload({
        name,
        status: status as NotificationTemplateCreateInput['status'],
        event_type: eventType as NotificationTemplateCreateInput['event_type'],
        subject_template: subjectTemplate || null,
        body_template: bodyTemplate,
        description: description || null,
      }),
    )
  }

  return (
    <form className="space-y-4" onSubmit={(event) => void handleSubmit(event)}>
      <Input label="Name" value={name} onChange={(event) => setName(event.target.value)} required />
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Status</span>
        <select
          className="w-full rounded-md border border-app-border px-3 py-2 text-sm"
          value={status}
          onChange={(event) => setStatus(event.target.value as typeof status)}
        >
          {NOTIFICATION_TEMPLATE_STATUSES.map((value) => (
            <option key={value} value={value}>{value}</option>
          ))}
        </select>
      </label>
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Event type</span>
        <select
          className="w-full rounded-md border border-app-border px-3 py-2 text-sm"
          value={eventType}
          onChange={(event) => setEventType(event.target.value as typeof eventType)}
        >
          {NOTIFICATION_EVENT_TYPES.map((value) => (
            <option key={value} value={value}>{value}</option>
          ))}
        </select>
      </label>
      <Input
        label="Subject template"
        value={subjectTemplate}
        onChange={(event) => setSubjectTemplate(event.target.value)}
      />
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Body template</span>
        <textarea
          className="w-full rounded-md border border-app-border px-3 py-2 text-sm"
          rows={6}
          value={bodyTemplate}
          onChange={(event) => setBodyTemplate(event.target.value)}
          required
        />
        <span className="mt-1 block text-xs text-gray-500">{TEMPLATE_PLACEHOLDER_HELP}</span>
      </label>
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Description</span>
        <textarea
          className="w-full rounded-md border border-app-border px-3 py-2 text-sm"
          rows={2}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
        />
      </label>
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}
      <div className="flex gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : initial ? 'Update template' : 'Create template'}
        </Button>
        {onCancel ? (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        ) : null}
      </div>
    </form>
  )
}
