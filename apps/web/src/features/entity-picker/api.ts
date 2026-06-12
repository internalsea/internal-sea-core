import { apiGet } from '@/lib/apiClient'
import type { EntityPickerResult, EntityPickerType } from '@/features/entity-picker/types'

interface SearchResponse {
  query: string
  total: number
  items: EntityPickerResult[]
}

export async function searchEntities(
  query: string,
  allowedTypes: EntityPickerType[],
  limit = 10,
): Promise<EntityPickerResult[]> {
  const params = new URLSearchParams()
  params.set('q', query)
  params.set('limit', String(limit))
  allowedTypes.forEach((type) => {
    params.append('types', type)
  })

  const response = await apiGet<SearchResponse>(`/search?${params.toString()}`)
  return response.items
}

export async function getEntityReference(
  entityType: EntityPickerType,
  entityId: string,
): Promise<EntityPickerResult> {
  const lookup = await apiGet<Omit<EntityPickerResult, 'matched_field' | 'updated_at'>>(
    `/search/entity/${entityType}/${entityId}`,
  )
  return {
    ...lookup,
    matched_field: null,
    updated_at: null,
  }
}
