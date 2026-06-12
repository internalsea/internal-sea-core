import type { PaginatedResponse } from '@/types/common'
import type { ProjectStatus, ProjectType } from '@/types/enums'

export type ProjectHealthStatus = 'unknown' | 'healthy' | 'warning' | 'critical'

export interface Project {
  id: string
  name: string
  description: string | null
  project_type: ProjectType
  status: ProjectStatus
  client_name: string | null
  account_name: string | null
  owner_id: string | null
  team_id: string | null
  capability_id: string | null
  start_date: string | null
  target_end_date: string | null
  actual_end_date: string | null
  budget_amount: string | number | null
  budget_currency: string | null
  priority: string | null
  health_status: ProjectHealthStatus | string | null
  delivery_notes: string | null
  created_at: string
  updated_at: string
}

export interface ProjectListItem {
  id: string
  name: string
  description: string | null
  project_type: ProjectType
  status: ProjectStatus
  client_name: string | null
  owner_id: string | null
  team_id: string | null
  capability_id: string | null
  start_date: string | null
  target_end_date: string | null
  health_status: string | null
  updated_at: string
}

export type ProjectListResponse = PaginatedResponse<ProjectListItem>

export interface ProjectCreateInput {
  name: string
  description?: string | null
  project_type?: ProjectType
  status?: ProjectStatus
  client_name?: string | null
  account_name?: string | null
  owner_id?: string | null
  team_id?: string | null
  capability_id?: string | null
  start_date?: string | null
  target_end_date?: string | null
  actual_end_date?: string | null
  budget_amount?: number | string | null
  budget_currency?: string | null
  priority?: string | null
  health_status?: string | null
  delivery_notes?: string | null
}

export type ProjectUpdateInput = Partial<ProjectCreateInput>

export interface ProjectFilters {
  search?: string
  project_type?: ProjectType
  status?: ProjectStatus
  client_name?: string
  account_name?: string
  owner_id?: string
  team_id?: string
  capability_id?: string
  health_status?: string
  page?: number
  page_size?: number
}

export interface ProjectSummary {
  project: Project
  open_work_items: number
  completed_work_items: number
  total_work_items: number
  overdue_work_items: number
}

export interface ProjectFormValues {
  name: string
  description: string
  project_type: ProjectType
  status: ProjectStatus
  health_status: string
  priority: string
  client_name: string
  account_name: string
  start_date: string
  target_end_date: string
  actual_end_date: string
  budget_amount: string
  budget_currency: string
  owner_id: string
  team_id: string
  capability_id: string
  delivery_notes: string
}

export type ProjectVariant = 'projects' | 'internal-projects'
