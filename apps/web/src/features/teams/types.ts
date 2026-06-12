import type { PaginatedResponse } from '@/types/common'

export interface Team {
  id: string
  name: string
  description: string | null
  created_at: string
  updated_at: string
}

export interface TeamListItem {
  id: string
  name: string
  description: string | null
  updated_at: string
}

export type TeamListResponse = PaginatedResponse<TeamListItem>

export interface TeamCreateInput {
  name: string
  description?: string | null
}

export type TeamUpdateInput = Partial<TeamCreateInput>

export interface TeamFilters {
  search?: string
  page?: number
  page_size?: number
}

export interface TeamSummary {
  team: Team
  people_count: number
  active_people_count: number
  data_products_count: number
  open_work_items_count: number
  projects_count: number
  internal_projects_count: number
}

export interface TeamFormValues {
  name: string
  description: string
}
