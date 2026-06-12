import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { activityKeys } from '@/features/activity/hooks'
import {
  attachFile,
  createFile,
  deleteFile,
  detachFile,
  getEntityFiles,
  getFile,
  getFileAttachments,
  getFiles,
  getFileStorages,
  updateFile,
} from '@/features/files/api'
import type {
  FileAttachmentInput,
  FileCreateInput,
  FileEntityType,
  FileFilters,
  FileUpdateInput,
} from '@/features/files/types'

export const fileKeys = {
  all: ['files'] as const,
  lists: () => [...fileKeys.all, 'list'] as const,
  list: (filters: FileFilters) => [...fileKeys.lists(), filters] as const,
  details: () => [...fileKeys.all, 'detail'] as const,
  detail: (id: string) => [...fileKeys.details(), id] as const,
  storages: () => [...fileKeys.all, 'storages'] as const,
  attachments: (fileId: string) => [...fileKeys.all, 'attachments', fileId] as const,
  entity: (entityType: FileEntityType, entityId: string) =>
    [...fileKeys.all, 'entity', entityType, entityId] as const,
}

export function useFiles(filters: FileFilters) {
  return useQuery({
    queryKey: fileKeys.list(filters),
    queryFn: () => getFiles(filters),
  })
}

export function useFile(id: string | undefined) {
  return useQuery({
    queryKey: fileKeys.detail(id ?? ''),
    queryFn: () => getFile(id!),
    enabled: Boolean(id),
  })
}

export function useCreateFile() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: FileCreateInput) => createFile(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: fileKeys.lists() })
    },
  })
}

export function useUpdateFile() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: FileUpdateInput }) =>
      updateFile(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: fileKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: fileKeys.detail(variables.id) })
    },
  })
}

export function useDeleteFile() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => deleteFile(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: fileKeys.lists() })
    },
  })
}

export function useFileStorages() {
  return useQuery({
    queryKey: fileKeys.storages(),
    queryFn: () => getFileStorages(),
  })
}

export function useFileAttachments(fileId: string | undefined) {
  return useQuery({
    queryKey: fileKeys.attachments(fileId ?? ''),
    queryFn: () => getFileAttachments(fileId!),
    enabled: Boolean(fileId),
  })
}

export function useEntityFiles(entityType: FileEntityType, entityId: string | undefined) {
  return useQuery({
    queryKey: fileKeys.entity(entityType, entityId ?? ''),
    queryFn: () => getEntityFiles(entityType, entityId!),
    enabled: Boolean(entityId),
  })
}

export function useAttachFile(entityType: FileEntityType, entityId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: Omit<FileAttachmentInput, 'entity_type' | 'entity_id'>) =>
      attachFile({ ...payload, entity_type: entityType, entity_id: entityId }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: fileKeys.entity(entityType, entityId) })
      void queryClient.invalidateQueries({ queryKey: activityKeys.entity(entityType, entityId) })
    },
  })
}

export function useDetachFile(entityType: FileEntityType, entityId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (attachmentId: string) => detachFile(attachmentId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: fileKeys.entity(entityType, entityId) })
      void queryClient.invalidateQueries({ queryKey: activityKeys.entity(entityType, entityId) })
    },
  })
}
