import type { PaginatedResponse } from '@/types/common'

export interface Capability {
  id: string
  name: string
  description: string | null
  created_at: string
  updated_at: string
}

export interface CapabilityListItem {
  id: string
  name: string
  description: string | null
  updated_at: string
}

export type CapabilityListResponse = PaginatedResponse<CapabilityListItem>

export interface CapabilityCreateInput {
  name: string
  description?: string | null
}

export type CapabilityUpdateInput = Partial<CapabilityCreateInput>

export interface CapabilityFilters {
  search?: string
  page?: number
  page_size?: number
}

export interface CapabilitySummary {
  capability: Capability
  people_count: number
  active_people_count: number
  data_products_count: number
  open_work_items_count: number
  projects_count: number
  internal_projects_count: number
}

export interface CapabilityFormValues {
  name: string
  description: string
}
