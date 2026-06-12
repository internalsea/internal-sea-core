import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  EntityFilesResponse,
  FileAsset,
  FileAssetListResponse,
  FileAttachment,
  FileAttachmentInput,
  FileCreateInput,
  FileEntityType,
  FileFilters,
  FileStorage,
  FileUpdateInput,
} from '@/features/files/types'

function toQueryParams(
  filters?: FileFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) {
    return undefined
  }
  return {
    search: filters.search,
    file_type: filters.file_type,
    status: filters.status,
    sensitivity: filters.sensitivity,
    storage_id: filters.storage_id,
    owner_id: filters.owner_id,
    is_evidence: filters.is_evidence,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getFileStorages(): Promise<{ items: FileStorage[] }> {
  return apiGet<{ items: FileStorage[] }>('/files/storages')
}

export function createFileStorage(payload: Partial<FileStorage>): Promise<FileStorage> {
  return apiPost<FileStorage>('/files/storages', payload)
}

export function updateFileStorage(id: string, payload: Partial<FileStorage>): Promise<FileStorage> {
  return apiPatch<FileStorage>(`/files/storages/${id}`, payload)
}

export function deleteFileStorage(id: string): Promise<void> {
  return apiDelete(`/files/storages/${id}`)
}

export function getFiles(filters?: FileFilters): Promise<FileAssetListResponse> {
  return apiGet<FileAssetListResponse>('/files', toQueryParams(filters))
}

export function getFile(id: string): Promise<FileAsset> {
  return apiGet<FileAsset>(`/files/${id}`)
}

export function createFile(payload: FileCreateInput): Promise<FileAsset> {
  return apiPost<FileAsset>('/files', payload)
}

export function updateFile(id: string, payload: FileUpdateInput): Promise<FileAsset> {
  return apiPatch<FileAsset>(`/files/${id}`, payload)
}

export function deleteFile(id: string): Promise<void> {
  return apiDelete(`/files/${id}`)
}

export function getFileAttachments(
  fileId: string,
): Promise<{ items: FileAttachment[]; total: number }> {
  return apiGet<{ items: FileAttachment[]; total: number }>(`/files/${fileId}/attachments`)
}

export function attachFile(payload: FileAttachmentInput): Promise<FileAttachment> {
  return apiPost<FileAttachment>('/files/attachments', payload)
}

export function detachFile(attachmentId: string): Promise<void> {
  return apiDelete(`/files/attachments/${attachmentId}`)
}

export function getEntityFiles(
  entityType: FileEntityType,
  entityId: string,
): Promise<EntityFilesResponse> {
  return apiGet<EntityFilesResponse>(`/files/entity/${entityType}/${entityId}`)
}
