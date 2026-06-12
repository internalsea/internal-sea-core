import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import {
  NOTIFICATION_CHANNEL_STATUSES,
  NOTIFICATION_CHANNEL_TYPES,
} from '@/features/notifications/constants'
import type {
  NotificationChannel,
  NotificationChannelCreateInput,
} from '@/features/notifications/types'
import { cleanChannelPayload, parseJsonField, stringifyJsonField } from '@/features/notifications/utils'

interface NotificationChannelFormProps {
  initial?: NotificationChannel | null
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: NotificationChannelCreateInput) => Promise<void>
  onCancel?: () => void
}

export function NotificationChannelForm({
  initial,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: NotificationChannelFormProps) {
  const [name, setName] = useState(initial?.name ?? '')
  const [channelType, setChannelType] = useState(initial?.channel_type ?? 'in_app')
  const [status, setStatus] = useState(initial?.status ?? 'draft')
  const [description, setDescription] = useState(initial?.description ?? '')
  const [endpointUrl, setEndpointUrl] = useState(initial?.endpoint_url ?? '')
  const [defaultRecipient, setDefaultRecipient] = useState(initial?.default_recipient ?? '')
  const [providerConfigJson, setProviderConfigJson] = useState(
    stringifyJsonField(initial?.provider_config),
  )
  const [localError, setLocalError] = useState<string | null>(null)

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setLocalError(null)
    try {
      const provider_config = parseJsonField(providerConfigJson)
      await onSubmit(
        cleanChannelPayload({
          name,
          channel_type: channelType as NotificationChannelCreateInput['channel_type'],
          status: status as NotificationChannelCreateInput['status'],
          description: description || null,
          endpoint_url: endpointUrl || null,
          default_recipient: defaultRecipient || null,
          provider_config,
        }),
      )
    } catch (error) {
      setLocalError(error instanceof Error ? error.message : 'Invalid form data')
    }
  }

  return (
    <form className="space-y-4" onSubmit={(event) => void handleSubmit(event)}>
      <Input label="Name" value={name} onChange={(event) => setName(event.target.value)} required />
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Channel type</span>
        <select
          className="w-full rounded-md border border-app-border px-3 py-2 text-sm"
          value={channelType}
          onChange={(event) => setChannelType(event.target.value as typeof channelType)}
        >
          {NOTIFICATION_CHANNEL_TYPES.map((type) => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </label>
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Status</span>
        <select
          className="w-full rounded-md border border-app-border px-3 py-2 text-sm"
          value={status}
          onChange={(event) => setStatus(event.target.value as typeof status)}
        >
          {NOTIFICATION_CHANNEL_STATUSES.map((value) => (
            <option key={value} value={value}>{value}</option>
          ))}
        </select>
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
      <Input
        label="Endpoint URL"
        value={endpointUrl}
        onChange={(event) => setEndpointUrl(event.target.value)}
      />
      <p className="-mt-2 text-xs text-gray-500">Optional. Not called in MVP.</p>
      <Input
        label="Default recipient"
        value={defaultRecipient}
        onChange={(event) => setDefaultRecipient(event.target.value)}
      />
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-gray-700">Provider config (JSON)</span>
        <textarea
          className="w-full rounded-md border border-app-border px-3 py-2 font-mono text-xs"
          rows={4}
          value={providerConfigJson}
          onChange={(event) => setProviderConfigJson(event.target.value)}
        />
        <span className="mt-1 block text-xs text-gray-500">
          External delivery is not implemented yet. Do not store secrets here. Use environment
          variables or a future secret manager for provider credentials.
        </span>
      </label>
      {localError || submitError ? (
        <p className="text-sm text-status-danger">{localError ?? submitError}</p>
      ) : null}
      <div className="flex gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : initial ? 'Update channel' : 'Create channel'}
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
