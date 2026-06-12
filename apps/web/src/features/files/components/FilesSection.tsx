import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { FileAttachmentForm } from '@/features/files/components/FileAttachmentForm'
import { FileAttachmentList } from '@/features/files/components/FileAttachmentList'
import { useAttachFile, useDetachFile, useEntityFiles } from '@/features/files/hooks'
import type { FileEntityType } from '@/features/files/types'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { useCanWrite } from '@/features/auth/hooks'
import { cleanFileAttachmentPayload, getApiErrorMessage } from '@/features/files/utils'

interface FilesSectionProps {
  entityType: FileEntityType
  entityId: string
  title?: string
}

export function FilesSection({
  entityType,
  entityId,
  title = 'Files and Evidence',
}: FilesSectionProps) {
  const [showForm, setShowForm] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const { data, isLoading, isError, error } = useEntityFiles(entityType, entityId)
  const canWrite = useCanWrite()
  const attachMutation = useAttachFile(entityType, entityId)
  const detachMutation = useDetachFile(entityType, entityId)

  async function handleAttach(values: {
    file_id: string
    purpose: string
    is_evidence: boolean
    evidence_type: string
  }) {
    setSubmitError(null)
    try {
      await attachMutation.mutateAsync(
        cleanFileAttachmentPayload(values, entityType, entityId),
      )
      setShowForm(false)
    } catch (attachError) {
      setSubmitError(getApiErrorMessage(attachError))
    }
  }

  async function handleDetach(attachmentId: string) {
    if (!window.confirm('Detach this file from the entity?')) {
      return
    }
    try {
      await detachMutation.mutateAsync(attachmentId)
    } catch {
      // mutation error state
    }
  }

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title={title}
          description="Documents, links and evidence attached to this record."
        />
        <PermissionGate require="editor">
          <Button variant="secondary" size="sm" onClick={() => setShowForm((current) => !current)}>
            {showForm ? 'Cancel' : 'Attach file'}
          </Button>
        </PermissionGate>
      </div>

      <div className="mt-4 space-y-4">
        {showForm ? (
          <FileAttachmentForm
            isSubmitting={attachMutation.isPending}
            submitError={submitError}
            onSubmit={handleAttach}
            onCancel={() => setShowForm(false)}
          />
        ) : null}

        {isLoading ? (
          <p className="text-sm text-gray-500">Loading files…</p>
        ) : isError ? (
          <p className="text-sm text-status-danger">{getApiErrorMessage(error)}</p>
        ) : (
          <FileAttachmentList
            attachments={data?.files ?? []}
            onDetach={canWrite ? (attachment) => void handleDetach(attachment.id) : undefined}
            isDetaching={detachMutation.isPending}
          />
        )}
      </div>
    </Card>
  )
}
