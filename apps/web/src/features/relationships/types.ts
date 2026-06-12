import type { PaginatedResponse } from '@/types/common'

export type EntityType =
  | 'data_product'
  | 'work_item'
  | 'project'
  | 'internal_project'
  | 'person'
  | 'team'
  | 'capability'
  | 'policy'
  | 'rule'
  | 'compliance_check'
  | 'file'
  | 'meeting'
  | 'deal'
  | 'tool'

export type EntityLinkType =
  | 'relates_to'
  | 'depends_on'
  | 'blocks'
  | 'duplicates'
  | 'replaces'
  | 'owns'
  | 'supports'
  | 'improves'
  | 'affects'
  | 'created_from'
  | 'evidence_for'
  | 'decision_for'
  | 'risk_for'

export interface EntityLink {
  id: string
  source_type: EntityType
  source_id: string
  target_type: EntityType
  target_id: string
  link_type: EntityLinkType
  title: string | null
  description: string | null
  created_by_id: string | null
  created_at: string
  updated_at: string
}

export interface EntityLinkCreateInput {
  source_type: EntityType
  source_id: string
  target_type: EntityType
  target_id: string
  link_type: EntityLinkType
  title?: string | null
  description?: string | null
  created_by_id?: string | null
}

export interface EntityLinkUpdateInput {
  link_type?: EntityLinkType
  title?: string | null
  description?: string | null
}

export interface EntityRelationshipView {
  entity_type: EntityType
  entity_id: string
  outgoing: EntityLink[]
  incoming: EntityLink[]
  total: number
}

export type EntityLinkListResponse = PaginatedResponse<EntityLink>

export interface RelationshipFilters {
  entity_type?: EntityType
  entity_id?: string
  source_type?: EntityType
  source_id?: string
  target_type?: EntityType
  target_id?: string
  link_type?: EntityLinkType
  include_reverse?: boolean
  page?: number
  page_size?: number
}
