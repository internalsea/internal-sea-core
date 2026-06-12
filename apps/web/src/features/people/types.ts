import type { PaginatedResponse } from '@/types/common'

export type SeniorityLevel =
  | 'intern'
  | 'junior'
  | 'medior'
  | 'senior'
  | 'lead'
  | 'principal'
  | 'director'
  | 'partner'

export interface Person {
  id: string
  full_name: string
  email: string | null
  role_title: string | null
  seniority_level: SeniorityLevel | null
  user_id: string | null
  team_id: string | null
  capability_id: string | null
  availability_percent: number | null
  location: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PersonListItem {
  id: string
  full_name: string
  email: string | null
  role_title: string | null
  seniority_level: SeniorityLevel | null
  team_id: string | null
  capability_id: string | null
  availability_percent: number | null
  location: string | null
  is_active: boolean
  updated_at: string
}

export type PersonListResponse = PaginatedResponse<PersonListItem>

export interface PersonCreateInput {
  full_name: string
  email?: string | null
  role_title?: string | null
  seniority_level?: SeniorityLevel | null
  user_id?: string | null
  team_id?: string | null
  capability_id?: string | null
  availability_percent?: number | null
  location?: string | null
  is_active?: boolean
}

export type PersonUpdateInput = Partial<PersonCreateInput>

export interface PersonFilters {
  search?: string
  team_id?: string
  capability_id?: string
  seniority_level?: SeniorityLevel
  is_active?: boolean
  location?: string
  min_availability?: number
  max_availability?: number
  page?: number
  page_size?: number
}

export interface PersonSummary {
  person: Person
  assigned_work_items: number
  owned_data_products_business: number
  owned_data_products_technical: number
  owned_projects: number
}

export interface PersonFormValues {
  full_name: string
  email: string
  role_title: string
  seniority_level: string
  user_id: string
  team_id: string
  capability_id: string
  availability_percent: string
  location: string
  is_active: boolean
}
