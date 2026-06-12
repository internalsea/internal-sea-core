import { ApiError } from '@/lib/apiClient'
import type { Comment } from '@/features/comments/types'

export const MAX_COMMENT_LENGTH = 5000

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    const detail = error.body?.detail
    if (typeof detail === 'string') {
      return detail
    }
    return `Request failed (${error.status})`
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'Something went wrong.'
}

export function formatCommentAuthor(comment: Comment): string {
  if (!comment.author_id) {
    return 'System'
  }
  return `User ${comment.author_id.slice(0, 8)}`
}

export function formatDateTime(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleString()
}

export function validateCommentBody(body: string): string | null {
  const trimmed = body.trim()
  if (!trimmed) {
    return 'Comment cannot be empty.'
  }
  if (trimmed.length > MAX_COMMENT_LENGTH) {
    return `Comment cannot exceed ${MAX_COMMENT_LENGTH} characters.`
  }
  return null
}
