import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  Comment,
  CommentCreateInput,
  CommentListResponse,
  CommentUpdateInput,
} from '@/features/comments/types'

export function getDataProductComments(
  dataProductId: string,
  page = 1,
): Promise<CommentListResponse> {
  return apiGet<CommentListResponse>(`/data-products/${dataProductId}/comments`, { page })
}

export function addDataProductComment(
  dataProductId: string,
  payload: CommentCreateInput,
): Promise<Comment> {
  return apiPost<Comment>(`/data-products/${dataProductId}/comments`, payload)
}

export function getWorkItemComments(workItemId: string, page = 1): Promise<CommentListResponse> {
  return apiGet<CommentListResponse>(`/work-items/${workItemId}/comments`, { page })
}

export function addWorkItemComment(
  workItemId: string,
  payload: CommentCreateInput,
): Promise<Comment> {
  return apiPost<Comment>(`/work-items/${workItemId}/comments`, payload)
}

export function getProjectComments(projectId: string, page = 1): Promise<CommentListResponse> {
  return apiGet<CommentListResponse>(`/projects/${projectId}/comments`, { page })
}

export function addProjectComment(
  projectId: string,
  payload: CommentCreateInput,
): Promise<Comment> {
  return apiPost<Comment>(`/projects/${projectId}/comments`, payload)
}

export function getInternalProjectComments(
  projectId: string,
  page = 1,
): Promise<CommentListResponse> {
  return apiGet<CommentListResponse>(`/internal-projects/${projectId}/comments`, { page })
}

export function addInternalProjectComment(
  projectId: string,
  payload: CommentCreateInput,
): Promise<Comment> {
  return apiPost<Comment>(`/internal-projects/${projectId}/comments`, payload)
}

export function updateComment(commentId: string, payload: CommentUpdateInput): Promise<Comment> {
  return apiPatch<Comment>(`/comments/${commentId}`, payload)
}

export function deleteComment(commentId: string): Promise<void> {
  return apiDelete(`/comments/${commentId}`)
}
