import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { MAX_COMMENT_LENGTH, getApiErrorMessage, validateCommentBody } from '@/features/comments/utils'

interface CommentFormProps {
  onSubmit: (body: string) => Promise<void>
  isSubmitting?: boolean
}

export function CommentForm({ onSubmit, isSubmitting = false }: CommentFormProps) {
  const [body, setBody] = useState('')
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    const validationError = validateCommentBody(body)
    if (validationError) {
      setError(validationError)
      return
    }
    setError(null)
    try {
      await onSubmit(body.trim())
      setBody('')
    } catch (submitError) {
      setError(getApiErrorMessage(submitError))
    }
  }

  return (
    <form onSubmit={(event) => void handleSubmit(event)} className="space-y-3">
      <div>
        <label htmlFor="comment-body" className="sr-only">
          Comment
        </label>
        <textarea
          id="comment-body"
          value={body}
          onChange={(event) => setBody(event.target.value)}
          rows={3}
          maxLength={MAX_COMMENT_LENGTH}
          placeholder="Write a plain-text comment…"
          className="w-full rounded-md border border-app-border bg-white px-3 py-2 text-sm text-gray-900 placeholder:text-gray-400 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
        />
        <p className="mt-1 text-xs text-gray-400">
          {body.length}/{MAX_COMMENT_LENGTH}
        </p>
      </div>
      {error ? <p className="text-sm text-status-danger">{error}</p> : null}
      <div>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Posting…' : 'Post comment'}
        </Button>
      </div>
    </form>
  )
}
