import type { PaginatedResponse } from '@/types/common'

export interface ActivityEvent {
  id: string
  entity_type: string
  entity_id: string
  action: string
  actor_id: string | null
  title: string
  description: string | null
  details: Record<string, unknown> | null
  created_at: string
}

export type ActivityEventListResponse = PaginatedResponse<ActivityEvent>

export interface ActivityFilters {
  entity_type?: string
  entity_id?: string
  action?: string
  actor_id?: string
  page?: number
  page_size?: number
}
