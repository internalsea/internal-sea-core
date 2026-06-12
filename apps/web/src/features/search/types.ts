export type SearchResultType =
  | 'data_product'
  | 'work_item'
  | 'project'
  | 'internal_project'
  | 'person'
  | 'team'
  | 'capability'
  | 'file'
  | 'policy'
  | 'compliance_check'
  | 'automation_trigger'

export interface SearchResult {
  id: string
  type: SearchResultType
  title: string
  description: string | null
  status: string | null
  secondary_status: string | null
  url: string
  matched_field: string | null
  updated_at: string | null
}

export interface SearchResponse {
  query: string
  total: number
  items: SearchResult[]
}

export interface SearchFilters {
  q: string
  types?: SearchResultType[]
  limit?: number
}
