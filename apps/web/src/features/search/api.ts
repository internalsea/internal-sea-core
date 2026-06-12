import { apiGet } from '@/lib/apiClient'
import type { SearchFilters, SearchResponse } from '@/features/search/types'

export async function searchGlobal(filters: SearchFilters): Promise<SearchResponse> {
  const params = new URLSearchParams()
  params.set('q', filters.q)
  if (filters.limit !== undefined) {
    params.set('limit', String(filters.limit))
  }
  filters.types?.forEach((type) => {
    params.append('types', type)
  })

  return apiGet<SearchResponse>(`/search?${params.toString()}`)
}
