import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { SectionHeader } from '@/components/ui/SectionHeader'
import {
  FILE_ASSET_TYPES,
  FILE_SENSITIVITIES,
  FILE_STATUSES,
  selectClassName,
} from '@/features/files/constants'
import type { FileFormValues } from '@/features/files/types'
import { cleanFilePayload, isValidUrl } from '@/features/files/utils'

interface FileFormProps {
  initialValues?: Partial<FileFormValues>
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: ReturnType<typeof cleanFilePayload>) => void
  onCancel: () => void
}

const defaultValues: FileFormValues = {
  name: '',
  description: '',
  file_type: 'document',
  status: 'active',
  sensitivity: 'internal',
  version: '',
  external_url: '',
  storage_id: '',
  storage_path: '',
  original_filename: '',
  mime_type: '',
  file_size_bytes: '',
  owner_id: '',
  uploaded_by_id: '',
  checksum: '',
}

export function FileForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: FileFormProps) {
  const [values, setValues] = useState<FileFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [nameError, setNameError] = useState<string | null>(null)
  const [urlError, setUrlError] = useState<string | null>(null)
  const [sizeError, setSizeError] = useState<string | null>(null)

  const updateField = <K extends keyof FileFormValues>(field: K, value: FileFormValues[K]) => {
    setValues((current) => ({ ...current, [field]: value }))
  }

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()

    const trimmedName = values.name.trim()
    if (!trimmedName) {
      setNameError('Name is required')
      return
    }
    setNameError(null)

    if (!isValidUrl(values.external_url)) {
      setUrlError('Enter a valid URL starting with http:// or https://')
      return
    }
    setUrlError(null)

    if (values.file_size_bytes.trim() !== '') {
      const size = Number.parseInt(values.file_size_bytes, 10)
      if (Number.isNaN(size) || size < 0) {
        setSizeError('File size must be zero or greater')
        return
      }
    }
    setSizeError(null)

    onSubmit(cleanFilePayload({ ...values, name: trimmedName }))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      <section className="space-y-4">
        <SectionHeader title="Main" />
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Name <span className="text-status-danger">*</span>
            </label>
            <Input
              value={values.name}
              onChange={(event) => updateField('name', event.target.value)}
              disabled={isSubmitting}
            />
            {nameError ? <p className="mt-1 text-sm text-status-danger">{nameError}</p> : null}
          </div>
          <div className="sm:col-span-2">
            <label className="mb-1 block text-sm font-medium text-gray-700">Description</label>
            <textarea
              className="block min-h-24 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm"
              value={values.description}
              onChange={(event) => updateField('description', event.target.value)}
              disabled={isSubmitting}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">File type</label>
            <select
              className={selectClassName}
              value={values.file_type}
              onChange={(event) =>
                updateField('file_type', event.target.value as FileFormValues['file_type'])
              }
              disabled={isSubmitting}
            >
              {FILE_ASSET_TYPES.map((item) => (
                <option key={item.value} value={item.value}>
                  {item.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Status</label>
            <select
              className={selectClassName}
              value={values.status}
              onChange={(event) =>
                updateField('status', event.target.value as FileFormValues['status'])
              }
              disabled={isSubmitting}
            >
              {FILE_STATUSES.map((item) => (
                <option key={item.value} value={item.value}>
                  {item.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Sensitivity</label>
            <select
              className={selectClassName}
              value={values.sensitivity}
              onChange={(event) =>
                updateField('sensitivity', event.target.value as FileFormValues['sensitivity'])
              }
              disabled={isSubmitting}
            >
              {FILE_SENSITIVITIES.map((item) => (
                <option key={item.value} value={item.value}>
                  {item.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Version</label>
            <Input
              value={values.version}
              onChange={(event) => updateField('version', event.target.value)}
              placeholder="v1.0"
              disabled={isSubmitting}
            />
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <SectionHeader
          title="Location"
          description="Binary upload is not implemented yet. Use external URL or storage path for now."
        />
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label className="mb-1 block text-sm font-medium text-gray-700">External URL</label>
            <Input
              value={values.external_url}
              onChange={(event) => updateField('external_url', event.target.value)}
              placeholder="https://example.com/docs/file"
              disabled={isSubmitting}
            />
            {urlError ? <p className="mt-1 text-sm text-status-danger">{urlError}</p> : null}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Storage ID</label>
            <Input
              value={values.storage_id}
              onChange={(event) => updateField('storage_id', event.target.value)}
              disabled={isSubmitting}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Storage path</label>
            <Input
              value={values.storage_path}
              onChange={(event) => updateField('storage_path', event.target.value)}
              disabled={isSubmitting}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Original filename</label>
            <Input
              value={values.original_filename}
              onChange={(event) => updateField('original_filename', event.target.value)}
              disabled={isSubmitting}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">MIME type</label>
            <Input
              value={values.mime_type}
              onChange={(event) => updateField('mime_type', event.target.value)}
              disabled={isSubmitting}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">File size (bytes)</label>
            <Input
              value={values.file_size_bytes}
              onChange={(event) => updateField('file_size_bytes', event.target.value)}
              disabled={isSubmitting}
            />
            {sizeError ? <p className="mt-1 text-sm text-status-danger">{sizeError}</p> : null}
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <SectionHeader title="Ownership" />
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Owner ID</label>
            <Input
              value={values.owner_id}
              onChange={(event) => updateField('owner_id', event.target.value)}
              disabled={isSubmitting}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Uploaded by ID</label>
            <Input
              value={values.uploaded_by_id}
              onChange={(event) => updateField('uploaded_by_id', event.target.value)}
              disabled={isSubmitting}
            />
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <SectionHeader title="Technical" />
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Checksum</label>
          <Input
            value={values.checksum}
            onChange={(event) => updateField('checksum', event.target.value)}
            disabled={isSubmitting}
          />
        </div>
      </section>

      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}

      <div className="flex gap-3">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : mode === 'create' ? 'Create file' : 'Save changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
