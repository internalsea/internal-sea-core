import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  addDataProductComment,
  addInternalProjectComment,
  addProjectComment,
  addWorkItemComment,
  deleteComment,
  getDataProductComments,
  getInternalProjectComments,
  getProjectComments,
  getWorkItemComments,
  updateComment,
} from '@/features/comments/api'
import type { CommentCreateInput, CommentTargetType, CommentUpdateInput } from '@/features/comments/types'

export const commentKeys = {
  all: ['comments'] as const,
  lists: () => [...commentKeys.all, 'list'] as const,
  list: (targetType: CommentTargetType, targetId: string) =>
    [...commentKeys.lists(), targetType, targetId] as const,
}

export function useDataProductComments(dataProductId: string | undefined) {
  return useQuery({
    queryKey: commentKeys.list('data_product', dataProductId ?? ''),
    queryFn: () => getDataProductComments(dataProductId!),
    enabled: Boolean(dataProductId),
  })
}

export function useAddDataProductComment(dataProductId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CommentCreateInput) => addDataProductComment(dataProductId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: commentKeys.list('data_product', dataProductId),
      })
    },
  })
}

export function useWorkItemComments(workItemId: string | undefined) {
  return useQuery({
    queryKey: commentKeys.list('work_item', workItemId ?? ''),
    queryFn: () => getWorkItemComments(workItemId!),
    enabled: Boolean(workItemId),
  })
}

export function useAddWorkItemComment(workItemId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CommentCreateInput) => addWorkItemComment(workItemId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: commentKeys.list('work_item', workItemId),
      })
    },
  })
}

export function useProjectComments(projectId: string | undefined) {
  return useQuery({
    queryKey: commentKeys.list('project', projectId ?? ''),
    queryFn: () => getProjectComments(projectId!),
    enabled: Boolean(projectId),
  })
}

export function useAddProjectComment(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CommentCreateInput) => addProjectComment(projectId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: commentKeys.list('project', projectId),
      })
    },
  })
}

export function useInternalProjectComments(projectId: string | undefined) {
  return useQuery({
    queryKey: commentKeys.list('internal_project', projectId ?? ''),
    queryFn: () => getInternalProjectComments(projectId!),
    enabled: Boolean(projectId),
  })
}

export function useAddInternalProjectComment(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CommentCreateInput) => addInternalProjectComment(projectId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: commentKeys.list('internal_project', projectId),
      })
    },
  })
}

export function useUpdateComment() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ commentId, payload }: { commentId: string; payload: CommentUpdateInput }) =>
      updateComment(commentId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: commentKeys.lists() })
    },
  })
}

export function useDeleteComment() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (commentId: string) => deleteComment(commentId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: commentKeys.lists() })
    },
  })
}
