import type {
  FileAssetType,
  FileEntityType,
  FileSensitivity,
  FileStatus,
  FileStorageType,
} from '@/features/files/types'
import type { BadgeVariant } from '@/lib/designTokens'

export interface SelectOption<T extends string = string> {
  value: T
  label: string
}

export const FILE_STORAGE_TYPES: SelectOption<FileStorageType>[] = [
  { value: 'local', label: 'Local' },
  { value: 's3', label: 'S3' },
  { value: 'azure_blob', label: 'Azure Blob' },
  { value: 'google_drive', label: 'Google Drive' },
  { value: 'sharepoint', label: 'SharePoint' },
  { value: 'external_url', label: 'External URL' },
]

export const FILE_ASSET_TYPES: SelectOption<FileAssetType>[] = [
  { value: 'document', label: 'Document' },
  { value: 'spreadsheet', label: 'Spreadsheet' },
  { value: 'presentation', label: 'Presentation' },
  { value: 'image', label: 'Image' },
  { value: 'pdf', label: 'PDF' },
  { value: 'contract', label: 'Contract' },
  { value: 'evidence', label: 'Evidence' },
  { value: 'specification', label: 'Specification' },
  { value: 'report', label: 'Report' },
  { value: 'other', label: 'Other' },
]

export const FILE_SENSITIVITIES: SelectOption<FileSensitivity>[] = [
  { value: 'public', label: 'Public' },
  { value: 'internal', label: 'Internal' },
  { value: 'confidential', label: 'Confidential' },
  { value: 'restricted', label: 'Restricted' },
]

export const FILE_STATUSES: SelectOption<FileStatus>[] = [
  { value: 'draft', label: 'Draft' },
  { value: 'active', label: 'Active' },
  { value: 'archived', label: 'Archived' },
  { value: 'deleted', label: 'Deleted' },
]

export const FILE_ENTITY_TYPES: SelectOption<FileEntityType>[] = [
  { value: 'data_product', label: 'Data Product' },
  { value: 'work_item', label: 'Work Item' },
  { value: 'project', label: 'Project' },
  { value: 'internal_project', label: 'Internal Project' },
  { value: 'person', label: 'Person' },
  { value: 'team', label: 'Team' },
  { value: 'capability', label: 'Capability' },
  { value: 'compliance_check', label: 'Compliance Check' },
  { value: 'policy', label: 'Policy' },
  { value: 'rule', label: 'Rule' },
  { value: 'meeting', label: 'Meeting' },
  { value: 'deal', label: 'Deal' },
]

export const fileTypeLabels: Record<FileAssetType, string> = Object.fromEntries(
  FILE_ASSET_TYPES.map((item) => [item.value, item.label]),
) as Record<FileAssetType, string>

export const fileSensitivityLabels: Record<FileSensitivity, string> = Object.fromEntries(
  FILE_SENSITIVITIES.map((item) => [item.value, item.label]),
) as Record<FileSensitivity, string>

export const fileStatusLabels: Record<FileStatus, string> = Object.fromEntries(
  FILE_STATUSES.map((item) => [item.value, item.label]),
) as Record<FileStatus, string>

export const fileTypeVariantMap: Record<FileAssetType, BadgeVariant> = {
  pdf: 'danger',
  spreadsheet: 'success',
  presentation: 'warning',
  document: 'info',
  evidence: 'teal',
  contract: 'warning',
  image: 'neutral',
  report: 'info',
  specification: 'info',
  other: 'neutral',
}

export const sensitivityVariantMap: Record<FileSensitivity, BadgeVariant> = {
  public: 'success',
  internal: 'info',
  confidential: 'warning',
  restricted: 'danger',
}

export const fileStatusVariantMap: Record<FileStatus, BadgeVariant> = {
  draft: 'neutral',
  active: 'success',
  archived: 'neutral',
  deleted: 'danger',
}

export const DEFAULT_PAGE_SIZE = 20

export const selectClassName =
  'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue disabled:cursor-not-allowed disabled:bg-app-muted disabled:text-gray-400'
