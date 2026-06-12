import type { BadgeVariant } from '@/lib/designTokens'
import type { ApiError } from '@/lib/apiClient'
import {
  fileStatusVariantMap,
  fileTypeVariantMap,
  sensitivityVariantMap,
} from '@/features/files/constants'
import type {
  FileAsset,
  FileAssetListItem,
  FileAssetType,
  FileAttachmentInput,
  FileCreateInput,
  FileFormValues,
  FileSensitivity,
  FileStatus,
} from '@/features/files/types'

const URL_PATTERN = /^https?:\/\/.+/i

export function formatFileSize(bytes: number | null | undefined): string {
  if (bytes === null || bytes === undefined) {
    return '—'
  }
  if (bytes < 1024) {
    return `${bytes} B`
  }
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`
  }
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return '—'
  }
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function truncateText(value: string | null | undefined, maxLength = 80): string {
  if (!value) {
    return '—'
  }
  if (value.length <= maxLength) {
    return value
  }
  return `${value.slice(0, maxLength)}…`
}

export function getFileHref(file: FileAsset | FileAssetListItem): string | null {
  return file.external_url
}

export function getFileTypeVariant(fileType: FileAssetType): BadgeVariant {
  return fileTypeVariantMap[fileType] ?? 'neutral'
}

export function getSensitivityVariant(sensitivity: FileSensitivity): BadgeVariant {
  return sensitivityVariantMap[sensitivity] ?? 'neutral'
}

export function getFileStatusVariant(status: FileStatus): BadgeVariant {
  return fileStatusVariantMap[status] ?? 'neutral'
}

function emptyToNull(value: string): string | null {
  const trimmed = value.trim()
  return trimmed === '' ? null : trimmed
}

export function cleanFilePayload(values: FileFormValues): FileCreateInput {
  const payload: FileCreateInput = {
    name: values.name.trim(),
    description: emptyToNull(values.description),
    file_type: values.file_type,
    status: values.status,
    sensitivity: values.sensitivity,
    version: emptyToNull(values.version),
    external_url: emptyToNull(values.external_url),
    storage_id: emptyToNull(values.storage_id),
    storage_path: emptyToNull(values.storage_path),
    original_filename: emptyToNull(values.original_filename),
    mime_type: emptyToNull(values.mime_type),
    checksum: emptyToNull(values.checksum),
    owner_id: emptyToNull(values.owner_id),
    uploaded_by_id: emptyToNull(values.uploaded_by_id),
  }

  if (values.file_size_bytes.trim() !== '') {
    const size = Number.parseInt(values.file_size_bytes, 10)
    if (!Number.isNaN(size) && size >= 0) {
      payload.file_size_bytes = size
    }
  }

  return payload
}

export function cleanFileAttachmentPayload(
  values: {
    file_id: string
    purpose: string
    is_evidence: boolean
    evidence_type: string
  },
  entityType: FileAttachmentInput['entity_type'],
  entityId: string,
): FileAttachmentInput {
  return {
    file_id: values.file_id.trim(),
    entity_type: entityType,
    entity_id: entityId,
    purpose: emptyToNull(values.purpose),
    is_evidence: values.is_evidence,
    evidence_type: emptyToNull(values.evidence_type),
  }
}

export function fileToFormValues(file: FileAsset): FileFormValues {
  return {
    name: file.name,
    description: file.description ?? '',
    file_type: file.file_type,
    status: file.status,
    sensitivity: file.sensitivity,
    version: file.version ?? '',
    external_url: file.external_url ?? '',
    storage_id: file.storage_id ?? '',
    storage_path: file.storage_path ?? '',
    original_filename: file.original_filename ?? '',
    mime_type: file.mime_type ?? '',
    file_size_bytes: file.file_size_bytes?.toString() ?? '',
    owner_id: file.owner_id ?? '',
    uploaded_by_id: file.uploaded_by_id ?? '',
    checksum: file.checksum ?? '',
  }
}

export function isValidUrl(value: string): boolean {
  if (!value.trim()) {
    return true
  }
  return URL_PATTERN.test(value.trim())
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof Error && 'status' in error) {
    const apiError = error as ApiError
    return apiError.message || `Request failed (${apiError.status})`
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'An unexpected error occurred'
}

export function confirmFileDelete(name: string): boolean {
  return window.confirm(`Delete file "${name}"? This will mark the file as deleted.`)
}
