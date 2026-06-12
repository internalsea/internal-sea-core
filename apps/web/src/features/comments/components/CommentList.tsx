import { EmptyState } from '@/components/ui/EmptyState'
import { CommentItem } from '@/features/comments/components/CommentItem'
import type { Comment } from '@/features/comments/types'

interface CommentListProps {
  comments: Comment[]
}

export function CommentList({ comments }: CommentListProps) {
  if (comments.length === 0) {
    return (
      <EmptyState
        title="No comments yet"
        description="Add a comment to capture context, decisions or updates."
      />
    )
  }

  return (
    <ul className="divide-y divide-app-border">
      {comments.map((comment) => (
        <CommentItem key={comment.id} comment={comment} />
      ))}
    </ul>
  )
}
