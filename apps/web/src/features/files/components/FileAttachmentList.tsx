import { Link } from 'react-router-dom'

import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { EntityReference } from '@/features/entity-picker/components/EntityReference'
import { ENTITY_PICKER_TYPES } from '@/features/entity-picker/constants'
import type { EntityPickerType } from '@/features/entity-picker/types'
import { FileSensitivityBadge } from '@/features/files/components/FileSensitivityBadge'
import { FileTypeBadge } from '@/features/files/components/FileTypeBadge'
import type { FileAttachment } from '@/features/files/types'
import { formatDateTime, getFileHref } from '@/features/files/utils'

interface FileAttachmentListProps {
  attachments: FileAttachment[]
  onDetach?: (attachment: FileAttachment) => void
  isDetaching?: boolean
  showEntityReference?: boolean
}

function isPickerType(type: string): type is EntityPickerType {
  return ENTITY_PICKER_TYPES.includes(type as EntityPickerType)
}

export function FileAttachmentList({
  attachments,
  onDetach,
  isDetaching = false,
  showEntityReference = false,
}: FileAttachmentListProps) {
  if (attachments.length === 0) {
    return <p className="text-sm text-gray-500">No files attached yet.</p>
  }

  return (
    <ul className="divide-y divide-app-border">
      {attachments.map((attachment) => {
        const file = attachment.file
        const href = file ? getFileHref(file) : null

        return (
          <li key={attachment.id} className="flex flex-wrap items-start justify-between gap-3 py-3">
            <div className="min-w-0 flex-1 space-y-1">
              <div className="flex flex-wrap items-center gap-2">
                {file ? (
                  <Link to={`/files/${file.id}`} className="font-medium text-core-blue hover:underline">
                    {file.name}
                  </Link>
                ) : (
                  <span className="font-medium text-gray-900">{attachment.file_id}</span>
                )}
                {attachment.is_evidence ? (
                  <Badge variant="teal">Evidence</Badge>
                ) : null}
                {file ? <FileTypeBadge fileType={file.file_type} /> : null}
                {file ? <FileSensitivityBadge sensitivity={file.sensitivity} /> : null}
              </div>
              {attachment.purpose ? (
                <p className="text-sm text-gray-600">{attachment.purpose}</p>
              ) : null}
              {attachment.evidence_type ? (
                <p className="text-xs text-gray-500">Evidence type: {attachment.evidence_type}</p>
              ) : null}
              {href ? (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-core-blue hover:underline"
                >
                  Open external link
                </a>
              ) : null}
              {showEntityReference && isPickerType(attachment.entity_type) ? (
                <p className="text-xs text-gray-500">
                  Attached to{' '}
                  <EntityReference
                    entityType={attachment.entity_type}
                    entityId={attachment.entity_id}
                  />
                </p>
              ) : null}
              <p className="text-xs text-gray-400">Attached {formatDateTime(attachment.created_at)}</p>
            </div>
            {onDetach ? (
              <Button
                variant="ghost"
                size="sm"
                disabled={isDetaching}
                onClick={() => onDetach(attachment)}
              >
                Detach
              </Button>
            ) : null}
          </li>
        )
      })}
    </ul>
  )
}
