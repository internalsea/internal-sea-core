import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { DetailEntityField } from '@/features/entity-picker/components/DetailEntityField'
import { FileAttachmentList } from '@/features/files/components/FileAttachmentList'
import { FileSensitivityBadge } from '@/features/files/components/FileSensitivityBadge'
import { FileStatusBadge } from '@/features/files/components/FileStatusBadge'
import { FileTypeBadge } from '@/features/files/components/FileTypeBadge'
import { useFileAttachments } from '@/features/files/hooks'
import type { FileAsset } from '@/features/files/types'
import { formatDateTime, formatFileSize, getFileHref } from '@/features/files/utils'

interface FileDetailProps {
  file: FileAsset
  onEdit: () => void
  onDelete: () => void
}

function DetailField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-900 break-all">{value}</dd>
    </div>
  )
}

export function FileDetail({ file, onEdit, onDelete }: FileDetailProps) {
  const { data: attachmentsData, isLoading: attachmentsLoading } = useFileAttachments(file.id)
  const externalHref = getFileHref(file)

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="text-2xl font-semibold text-gray-900">{file.name}</h1>
            <FileTypeBadge fileType={file.file_type} />
            <FileStatusBadge status={file.status} />
            <FileSensitivityBadge sensitivity={file.sensitivity} />
          </div>
          {file.description ? <p className="text-gray-600">{file.description}</p> : null}
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={onEdit}>
            Edit
          </Button>
          <Button variant="ghost" onClick={onDelete}>
            Delete
          </Button>
        </div>
      </div>

      <Card title="Overview">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField label="Version" value={file.version ?? '—'} />
          <DetailField label="File type" value={file.file_type} />
          <DetailField label="Status" value={file.status} />
          <DetailField label="Sensitivity" value={file.sensitivity} />
        </dl>
      </Card>

      <Card title="Location">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField label="External URL" value={file.external_url ?? '—'} />
          <DetailField label="Storage ID" value={file.storage_id ?? '—'} />
          <DetailField label="Storage path" value={file.storage_path ?? '—'} />
          <DetailField label="Original filename" value={file.original_filename ?? '—'} />
          <DetailField label="MIME type" value={file.mime_type ?? '—'} />
          <DetailField label="File size" value={formatFileSize(file.file_size_bytes)} />
        </dl>
        {externalHref ? (
          <div className="mt-4">
            <a
              href={externalHref}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-core-blue hover:underline"
            >
              Open external link
            </a>
          </div>
        ) : null}
      </Card>

      <Card title="Ownership">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailEntityField label="Owner" entityType="person" entityId={file.owner_id} />
          <DetailEntityField label="Uploaded by" entityType="person" entityId={file.uploaded_by_id} />
        </dl>
      </Card>

      <Card title="Technical metadata">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField label="Checksum" value={file.checksum ?? '—'} />
          <DetailField label="Created" value={formatDateTime(file.created_at)} />
          <DetailField label="Updated" value={formatDateTime(file.updated_at)} />
          <DetailField label="ID" value={file.id} />
        </dl>
      </Card>

      <Card title="Attachments">
        <p className="mb-4 text-sm text-gray-600">
          Entities where this file is attached. Manage attachments from entity detail pages.
        </p>
        {attachmentsLoading ? (
          <p className="text-sm text-gray-500">Loading attachments…</p>
        ) : (
          <FileAttachmentList attachments={attachmentsData?.items ?? []} showEntityReference />
        )}
      </Card>

      <Card title="Activity">
        <p className="text-sm text-gray-500">
          File-level activity timeline will be added with compliance workflows.
        </p>
        <Link to="/files" className="mt-2 inline-block text-sm text-core-blue hover:underline">
          Back to files
        </Link>
      </Card>
    </div>
  )
}
