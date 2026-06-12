import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import type { FileAttachmentFormValues } from '@/features/files/types'

interface FileAttachmentFormProps {
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: FileAttachmentFormValues) => void
  onCancel?: () => void
}

const defaultValues: Omit<FileAttachmentFormValues, 'file_id'> = {
  purpose: '',
  is_evidence: false,
  evidence_type: '',
}

export function FileAttachmentForm({
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: FileAttachmentFormProps) {
  const [selectedFile, setSelectedFile] = useState<EntityPickerValue | null>(null)
  const [values, setValues] = useState(defaultValues)
  const [fileIdError, setFileIdError] = useState<string | null>(null)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [manualFileId, setManualFileId] = useState('')

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    const fileId = showAdvanced ? manualFileId.trim() : selectedFile?.entity_id.trim() ?? ''
    if (!fileId) {
      setFileIdError('Select or enter a file ID.')
      return
    }
    setFileIdError(null)
    onSubmit({ ...values, file_id: fileId })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-md border border-app-border bg-app-muted/30 p-4">
      {!showAdvanced ? (
        <EntityPicker
          label="File"
          allowedTypes={['file']}
          value={selectedFile}
          onChange={setSelectedFile}
          required
          error={fileIdError ?? undefined}
          helperText="Search for an existing file by name."
        />
      ) : (
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">
            File ID <span className="text-status-danger">*</span>
          </label>
          <Input
            value={manualFileId}
            onChange={(event) => setManualFileId(event.target.value)}
            placeholder="UUID of an existing file"
            disabled={isSubmitting}
          />
          {fileIdError ? <p className="mt-1 text-sm text-status-danger">{fileIdError}</p> : null}
        </div>
      )}

      <button
        type="button"
        onClick={() => setShowAdvanced((current) => !current)}
        className="text-xs text-core-blue hover:underline"
      >
        {showAdvanced ? 'Use file picker' : 'Use manual file ID'}
      </button>

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Purpose</label>
        <Input
          value={values.purpose}
          onChange={(event) => setValues((current) => ({ ...current, purpose: event.target.value }))}
          placeholder="e.g. Functional specification"
          disabled={isSubmitting}
        />
      </div>
      <div className="flex items-center gap-2">
        <input
          id="is_evidence"
          type="checkbox"
          checked={values.is_evidence}
          onChange={(event) =>
            setValues((current) => ({ ...current, is_evidence: event.target.checked }))
          }
          disabled={isSubmitting}
        />
        <label htmlFor="is_evidence" className="text-sm text-gray-700">
          Mark as evidence
        </label>
      </div>
      {values.is_evidence ? (
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Evidence type</label>
          <Input
            value={values.evidence_type}
            onChange={(event) =>
              setValues((current) => ({ ...current, evidence_type: event.target.value }))
            }
            placeholder="e.g. kpi_certification"
            disabled={isSubmitting}
          />
        </div>
      ) : null}
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}
      <div className="flex gap-2">
        <Button type="submit" size="sm" disabled={isSubmitting}>
          {isSubmitting ? 'Attaching…' : 'Attach file'}
        </Button>
        {onCancel ? (
          <Button type="button" variant="secondary" size="sm" onClick={onCancel} disabled={isSubmitting}>
            Cancel
          </Button>
        ) : null}
      </div>
    </form>
  )
}
