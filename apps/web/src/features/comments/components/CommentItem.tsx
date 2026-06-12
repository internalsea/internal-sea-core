import type { Comment } from '@/features/comments/types'
import { formatCommentAuthor, formatDateTime } from '@/features/comments/utils'

interface CommentItemProps {
  comment: Comment
}

export function CommentItem({ comment }: CommentItemProps) {
  return (
    <li className="border-b border-app-border py-4 last:border-b-0">
      <div className="flex items-center justify-between gap-3">
        <span className="text-xs font-medium text-gray-500">{formatCommentAuthor(comment)}</span>
        <time className="text-xs text-gray-400" dateTime={comment.created_at}>
          {formatDateTime(comment.created_at)}
        </time>
      </div>
      <p className="mt-2 whitespace-pre-wrap text-sm text-gray-700">{comment.body}</p>
    </li>
  )
}
