import { useQuery } from '@tanstack/react-query'

import { searchGlobal } from '@/features/search/api'
import type { SearchResultType } from '@/features/search/types'

export const searchKeys = {
  all: ['search'] as const,
  query: (query: string, types?: SearchResultType[], limit?: number) =>
    ['search', query, types ?? [], limit ?? 20] as const,
}

export function useGlobalSearch(
  query: string,
  options?: {
    types?: SearchResultType[]
    limit?: number
    enabled?: boolean
  },
) {
  const trimmedQuery = query.trim()

  return useQuery({
    queryKey: searchKeys.query(trimmedQuery, options?.types, options?.limit),
    queryFn: () =>
      searchGlobal({
        q: trimmedQuery,
        types: options?.types,
        limit: options?.limit,
      }),
    enabled: (options?.enabled ?? true) && trimmedQuery.length >= 2,
    staleTime: 30_000,
  })
}
