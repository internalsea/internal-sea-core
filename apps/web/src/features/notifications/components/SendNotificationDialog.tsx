import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useSendNotificationMessage } from '@/features/notifications/hooks'
import { getApiErrorMessage, parseJsonField } from '@/features/notifications/utils'

interface SendNotificationDialogProps {
  messageId: string
  onClose: () => void
  onConfirm: () => void
}

export function SendNotificationDialog({
  messageId,
  onClose,
  onConfirm,
}: SendNotificationDialogProps) {
  const [simulate, setSimulate] = useState(true)
  const [recipientOverride, setRecipientOverride] = useState('')
  const [contextJson, setContextJson] = useState('{}')
  const [error, setError] = useState<string | null>(null)
  const sendMutation = useSendNotificationMessage(messageId)

  async function handleSend() {
    setError(null)
    try {
      const context = parseJsonField(contextJson) ?? {}
      await sendMutation.mutateAsync({
        simulate,
        recipient_override: recipientOverride || null,
        context,
      })
      onConfirm()
    } catch (sendError) {
      setError(getApiErrorMessage(sendError))
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-lg rounded-lg bg-white p-6 shadow-lg">
        <h2 className="text-lg font-semibold text-gray-900">Send notification</h2>
        <p className="mt-1 text-sm text-gray-600">
          Simulation mode records delivery attempts without calling external providers.
        </p>
        <div className="mt-4 space-y-4">
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={simulate} onChange={(e) => setSimulate(e.target.checked)} />
            Simulate delivery (recommended)
          </label>
          {!simulate ? (
            <p className="text-sm text-status-warning">
              External providers are not implemented. Only in-app delivery can be marked as sent.
            </p>
          ) : null}
          <Input
            label="Recipient override (optional)"
            value={recipientOverride}
            onChange={(event) => setRecipientOverride(event.target.value)}
          />
          <label className="block text-sm">
            <span className="mb-1 block font-medium text-gray-700">Context JSON (optional)</span>
            <textarea
              className="w-full rounded-md border border-app-border px-3 py-2 font-mono text-xs"
              rows={4}
              value={contextJson}
              onChange={(event) => setContextJson(event.target.value)}
            />
          </label>
          {error ? <p className="text-sm text-status-danger">{error}</p> : null}
        </div>
        <div className="mt-6 flex justify-end gap-2">
          <Button variant="secondary" onClick={onClose}>Cancel</Button>
          <Button onClick={() => void handleSend()} disabled={sendMutation.isPending}>
            {sendMutation.isPending ? 'Sending…' : simulate ? 'Simulate send' : 'Send'}
          </Button>
        </div>
      </div>
    </div>
  )
}
