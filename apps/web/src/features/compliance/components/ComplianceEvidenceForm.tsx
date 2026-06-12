import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import { EVIDENCE_STATUSES, selectClassName } from '@/features/compliance/constants'
import type { EvidenceStatus } from '@/features/compliance/types'
import { cleanEvidencePayload } from '@/features/compliance/utils'

interface ComplianceEvidenceFormProps {
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: ReturnType<typeof cleanEvidencePayload>) => void
  onCancel?: () => void
}

export function ComplianceEvidenceForm({
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: ComplianceEvidenceFormProps) {
  const [selectedFile, setSelectedFile] = useState<EntityPickerValue | null>(null)
  const [status, setStatus] = useState<EvidenceStatus>('submitted')
  const [description, setDescription] = useState('')
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
    onSubmit(cleanEvidencePayload({ file_id: fileId, status, description }))
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
        />
      ) : (
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">File ID *</label>
          <Input value={manualFileId} onChange={(e) => setManualFileId(e.target.value)} />
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
        <label className="mb-1 block text-sm font-medium text-gray-700">Status</label>
        <select className={selectClassName} value={status} onChange={(e) => setStatus(e.target.value as EvidenceStatus)}>
          {EVIDENCE_STATUSES.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
        </select>
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Description</label>
        <Input value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}
      <div className="flex gap-2">
        <Button type="submit" size="sm" disabled={isSubmitting}>{isSubmitting ? 'Adding…' : 'Add evidence'}</Button>
        {onCancel ? <Button type="button" variant="secondary" size="sm" onClick={onCancel}>Cancel</Button> : null}
      </div>
    </form>
  )
}
