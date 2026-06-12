import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { CommentForm } from '@/features/comments/components/CommentForm'
import { CommentList } from '@/features/comments/components/CommentList'
import {
  useAddDataProductComment,
  useAddInternalProjectComment,
  useAddProjectComment,
  useAddWorkItemComment,
  useDataProductComments,
  useInternalProjectComments,
  useProjectComments,
  useWorkItemComments,
} from '@/features/comments/hooks'
import type { CommentTargetType } from '@/features/comments/types'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { getApiErrorMessage } from '@/features/comments/utils'
import { activityKeys } from '@/features/activity/hooks'
import { useQueryClient } from '@tanstack/react-query'

interface CommentsSectionProps {
  targetType: CommentTargetType
  targetId: string
  title?: string
}

function useCommentsForTarget(targetType: CommentTargetType, targetId: string) {
  const dataProduct = useDataProductComments(
    targetType === 'data_product' ? targetId : undefined,
  )
  const workItem = useWorkItemComments(targetType === 'work_item' ? targetId : undefined)
  const project = useProjectComments(targetType === 'project' ? targetId : undefined)
  const internalProject = useInternalProjectComments(
    targetType === 'internal_project' ? targetId : undefined,
  )

  switch (targetType) {
    case 'data_product':
      return dataProduct
    case 'work_item':
      return workItem
    case 'project':
      return project
    case 'internal_project':
      return internalProject
  }
}

function useAddCommentForTarget(targetType: CommentTargetType, targetId: string) {
  const addDataProduct = useAddDataProductComment(targetId)
  const addWorkItem = useAddWorkItemComment(targetId)
  const addProject = useAddProjectComment(targetId)
  const addInternalProject = useAddInternalProjectComment(targetId)

  switch (targetType) {
    case 'data_product':
      return addDataProduct
    case 'work_item':
      return addWorkItem
    case 'project':
      return addProject
    case 'internal_project':
      return addInternalProject
  }
}

function entityTypeForActivity(targetType: CommentTargetType): string {
  return targetType
}

export function CommentsSection({
  targetType,
  targetId,
  title = 'Comments',
}: CommentsSectionProps) {
  const queryClient = useQueryClient()
  const { data, isLoading, isError, error } = useCommentsForTarget(targetType, targetId)
  const addComment = useAddCommentForTarget(targetType, targetId)

  async function handleSubmit(body: string) {
    await addComment.mutateAsync({ body })
    void queryClient.invalidateQueries({
      queryKey: activityKeys.entity(entityTypeForActivity(targetType), targetId),
    })
  }

  return (
    <Card>
      <SectionHeader
        title={title}
        description="Plain-text comments for collaboration and context."
      />
      <div className="space-y-4">
        <PermissionGate require="editor">
          <CommentForm onSubmit={handleSubmit} isSubmitting={addComment.isPending} />
        </PermissionGate>
        {isLoading ? (
          <p className="text-sm text-gray-500">Loading comments…</p>
        ) : isError ? (
          <p className="text-sm text-status-danger">{getApiErrorMessage(error)}</p>
        ) : (
          <CommentList comments={data?.items ?? []} />
        )}
      </div>
    </Card>
  )
}
