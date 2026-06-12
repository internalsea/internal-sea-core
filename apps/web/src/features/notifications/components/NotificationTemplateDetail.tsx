import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { NotificationMessagesTable } from '@/features/notifications/components/NotificationMessagesTable'
import {
  useNotificationMessages,
  useRenderNotificationTemplate,
} from '@/features/notifications/hooks'
import type { NotificationTemplate } from '@/features/notifications/types'
import { formatDateTime, getApiErrorMessage, parseJsonField } from '@/features/notifications/utils'

interface NotificationTemplateDetailProps {
  template: NotificationTemplate
}

export function NotificationTemplateDetail({ template }: NotificationTemplateDetailProps) {
  const [contextJson, setContextJson] = useState('{\n  "title": "Demo title",\n  "status": "active"\n}')
  const [renderError, setRenderError] = useState<string | null>(null)
  const [preview, setPreview] = useState<{ subject: string | null; body: string } | null>(null)
  const renderMutation = useRenderNotificationTemplate()
  const messagesQuery = useNotificationMessages({
    template_id: template.id,
    page: 1,
    page_size: 10,
  })

  async function handleRenderTest() {
    setRenderError(null)
    try {
      const context = parseJsonField(contextJson) ?? {}
      const result = await renderMutation.mutateAsync({
        template_id: template.id,
        context,
      })
      setPreview(result)
    } catch (error) {
      setRenderError(getApiErrorMessage(error))
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <SectionHeader title={template.name} description={template.description ?? undefined} />
        <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
          <div><dt className="text-gray-500">Status</dt><dd>{template.status}</dd></div>
          <div><dt className="text-gray-500">Event type</dt><dd>{template.event_type ?? '—'}</dd></div>
          <div><dt className="text-gray-500">Updated</dt><dd>{formatDateTime(template.updated_at)}</dd></div>
        </dl>
        <div className="mt-4 space-y-2 text-sm">
          <p className="font-medium text-gray-700">Subject template</p>
          <pre className="rounded-md bg-app-muted p-3 text-xs">{template.subject_template ?? '—'}</pre>
          <p className="font-medium text-gray-700">Body template</p>
          <pre className="whitespace-pre-wrap rounded-md bg-app-muted p-3 text-xs">{template.body_template}</pre>
        </div>
      </Card>

      <Card>
        <SectionHeader title="Render test" description="Preview placeholder substitution with JSON context." />
        <textarea
          className="mt-3 w-full rounded-md border border-app-border px-3 py-2 font-mono text-xs"
          rows={5}
          value={contextJson}
          onChange={(event) => setContextJson(event.target.value)}
        />
        <div className="mt-3 flex gap-2">
          <Button size="sm" onClick={() => void handleRenderTest()} disabled={renderMutation.isPending}>
            Render preview
          </Button>
        </div>
        {renderError ? <p className="mt-2 text-sm text-status-danger">{renderError}</p> : null}
        {preview ? (
          <div className="mt-4 space-y-2 text-sm">
            <p><span className="font-medium">Subject:</span> {preview.subject ?? '—'}</p>
            <pre className="whitespace-pre-wrap rounded-md bg-app-muted p-3 text-xs">{preview.body}</pre>
          </div>
        ) : null}
      </Card>

      <Card>
        <SectionHeader title="Related messages" description="Messages created from this template." />
        <div className="mt-4">
          <NotificationMessagesTable items={messagesQuery.data?.items ?? []} />
        </div>
      </Card>
    </div>
  )
}
