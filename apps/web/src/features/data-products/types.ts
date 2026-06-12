import type { PaginatedResponse, UUID } from '@/types/common'
import type { DataProductStatus, DataProductType, QualityStatus } from '@/types/enums'

export interface DataProduct {
  id: UUID
  name: string
  description: string | null
  type: DataProductType
  status: DataProductStatus
  quality_status: QualityStatus
  business_domain_id: UUID | null
  business_owner_id: UUID | null
  technical_owner_id: UUID | null
  capability_id: UUID | null
  team_id: UUID | null
  refresh_frequency: string | null
  source_systems: string | null
  consumers: string | null
  documentation_url: string | null
  created_at: string
  updated_at: string
}

export type DataProductListItem = DataProduct

export type DataProductListResponse = PaginatedResponse<DataProductListItem>

export interface DataProductCreateInput {
  name: string
  description?: string | null
  type?: DataProductType
  status?: DataProductStatus
  quality_status?: QualityStatus
  business_domain_id?: UUID | null
  business_owner_id?: UUID | null
  technical_owner_id?: UUID | null
  capability_id?: UUID | null
  team_id?: UUID | null
  refresh_frequency?: string | null
  source_systems?: string | null
  consumers?: string | null
  documentation_url?: string | null
}

export type DataProductUpdateInput = Partial<DataProductCreateInput>

export interface DataProductListParams {
  search?: string
  status?: DataProductStatus
  type?: DataProductType
  quality_status?: QualityStatus
  business_domain_id?: UUID
  capability_id?: UUID
  team_id?: UUID
  business_owner_id?: UUID
  technical_owner_id?: UUID
  page?: number
  page_size?: number
}
