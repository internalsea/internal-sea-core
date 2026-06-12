import type { PaginatedResponse, UUID } from '@/types/common'

export type WorkItemType =
  | 'epic'
  | 'story'
  | 'task'
  | 'bug'
  | 'risk'
  | 'decision'
  | 'technical_debt'
  | 'improvement'
  | 'support_request'

export type WorkItemStatus =
  | 'backlog'
  | 'ready'
  | 'in_progress'
  | 'review'
  | 'done'
  | 'closed'

export type WorkItemPriority = 'low' | 'medium' | 'high' | 'critical'

export interface WorkItem {
  id: UUID
  title: string
  description: string | null
  type: WorkItemType
  status: WorkItemStatus
  priority: WorkItemPriority
  assignee_id: UUID | null
  reporter_id: UUID | null
  data_product_id: UUID | null
  project_id: UUID | null
  capability_id: UUID | null
  team_id: UUID | null
  due_date: string | null
  estimate_points: number | null
  created_at: string
  updated_at: string
}

export type WorkItemListItem = WorkItem

export type WorkItemListResponse = PaginatedResponse<WorkItemListItem>

export interface WorkItemCreateInput {
  title: string
  description?: string | null
  type?: WorkItemType
  status?: WorkItemStatus
  priority?: WorkItemPriority
  assignee_id?: UUID | null
  reporter_id?: UUID | null
  data_product_id?: UUID | null
  project_id?: UUID | null
  capability_id?: UUID | null
  team_id?: UUID | null
  due_date?: string | null
  estimate_points?: number | null
}

export type WorkItemUpdateInput = Partial<WorkItemCreateInput>

export interface WorkItemFilters {
  search?: string
  type?: WorkItemType
  status?: WorkItemStatus
  priority?: WorkItemPriority
  assignee_id?: UUID
  data_product_id?: UUID
  capability_id?: UUID
  team_id?: UUID
  page?: number
  page_size?: number
}

export interface WorkItemBoardColumn {
  status: WorkItemStatus
  title: string
  items: WorkItemListItem[]
  count: number
}

export interface WorkItemBoardResponse {
  columns: WorkItemBoardColumn[]
}

export interface WorkItemFormValues {
  title: string
  description: string
  type: WorkItemType
  status: WorkItemStatus
  priority: WorkItemPriority
  due_date: string
  estimate_points: string
  assignee_id: string
  reporter_id: string
  data_product_id: string
  project_id: string
  capability_id: string
  team_id: string
}
