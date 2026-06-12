import type { PaginatedResponse } from '@/types/common'

export type FileStorageType =
  | 'local'
  | 's3'
  | 'azure_blob'
  | 'google_drive'
  | 'sharepoint'
  | 'external_url'

export type FileAssetType =
  | 'document'
  | 'spreadsheet'
  | 'presentation'
  | 'image'
  | 'pdf'
  | 'contract'
  | 'evidence'
  | 'specification'
  | 'report'
  | 'other'

export type FileSensitivity = 'public' | 'internal' | 'confidential' | 'restricted'

export type FileStatus = 'draft' | 'active' | 'archived' | 'deleted'

export type FileEntityType =
  | 'data_product'
  | 'work_item'
  | 'project'
  | 'internal_project'
  | 'person'
  | 'team'
  | 'capability'
  | 'compliance_check'
  | 'policy'
  | 'rule'
  | 'meeting'
  | 'deal'

export interface FileStorage {
  id: string
  name: string
  storage_type: FileStorageType
  base_url: string | null
  description: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface FileAsset {
  id: string
  name: string
  description: string | null
  file_type: FileAssetType
  status: FileStatus
  sensitivity: FileSensitivity
  storage_id: string | null
  original_filename: string | null
  mime_type: string | null
  file_size_bytes: number | null
  external_url: string | null
  storage_path: string | null
  checksum: string | null
  version: string | null
  owner_id: string | null
  uploaded_by_id: string | null
  created_at: string
  updated_at: string
}

export interface FileAssetListItem {
  id: string
  name: string
  description: string | null
  file_type: FileAssetType
  status: FileStatus
  sensitivity: FileSensitivity
  storage_id: string | null
  external_url: string | null
  owner_id: string | null
  version: string | null
  updated_at: string
}

export type FileAssetListResponse = PaginatedResponse<FileAssetListItem>

export interface FileAttachment {
  id: string
  file_id: string
  entity_type: FileEntityType
  entity_id: string
  purpose: string | null
  is_evidence: boolean
  evidence_type: string | null
  attached_by_id: string | null
  created_at: string
  updated_at: string
  file?: FileAssetListItem | null
}

export interface EntityFilesResponse {
  entity_type: FileEntityType
  entity_id: string
  files: FileAttachment[]
  total: number
}

export interface FileFilters {
  search?: string
  file_type?: FileAssetType
  status?: FileStatus
  sensitivity?: FileSensitivity
  storage_id?: string
  owner_id?: string
  is_evidence?: boolean
  page?: number
  page_size?: number
}

export interface FileCreateInput {
  name: string
  description?: string | null
  file_type?: FileAssetType
  status?: FileStatus
  sensitivity?: FileSensitivity
  storage_id?: string | null
  original_filename?: string | null
  mime_type?: string | null
  file_size_bytes?: number | null
  external_url?: string | null
  storage_path?: string | null
  checksum?: string | null
  version?: string | null
  owner_id?: string | null
  uploaded_by_id?: string | null
}

export type FileUpdateInput = Partial<FileCreateInput>

export interface FileAttachmentInput {
  file_id: string
  entity_type: FileEntityType
  entity_id: string
  purpose?: string | null
  is_evidence?: boolean
  evidence_type?: string | null
}

export interface FileFormValues {
  name: string
  description: string
  file_type: FileAssetType
  status: FileStatus
  sensitivity: FileSensitivity
  version: string
  external_url: string
  storage_id: string
  storage_path: string
  original_filename: string
  mime_type: string
  file_size_bytes: string
  owner_id: string
  uploaded_by_id: string
  checksum: string
}

export interface FileAttachmentFormValues {
  file_id: string
  purpose: string
  is_evidence: boolean
  evidence_type: string
}
