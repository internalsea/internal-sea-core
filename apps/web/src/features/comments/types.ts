import type { PaginatedResponse } from '@/types/common'

export type CommentTargetType = 'data_product' | 'work_item' | 'project' | 'internal_project'

export interface Comment {
  id: string
  body: string
  author_id: string | null
  data_product_id: string | null
  work_item_id: string | null
  project_id: string | null
  created_at: string
  updated_at: string
}

export interface CommentCreateInput {
  body: string
  author_id?: string | null
}

export interface CommentUpdateInput {
  body: string
}

export type CommentListResponse = PaginatedResponse<Comment>
