import { SearchEmptyState } from '@/features/search/components/SearchEmptyState'
import { SearchResultItem } from '@/features/search/components/SearchResultItem'
import type { SearchResult } from '@/features/search/types'

interface SearchResultsDropdownProps {
  query: string
  results: SearchResult[]
  isLoading: boolean
  error: string | null
  onSelect: (result: SearchResult) => void
}

export function SearchResultsDropdown({
  query,
  results,
  isLoading,
  error,
  onSelect,
}: SearchResultsDropdownProps) {
  const trimmedQuery = query.trim()

  if (trimmedQuery.length === 0) {
    return <SearchEmptyState variant="no-query" />
  }

  if (trimmedQuery.length < 2) {
    return <SearchEmptyState variant="short-query" />
  }

  if (isLoading) {
    return <p className="px-4 py-6 text-center text-sm text-gray-500">Searching…</p>
  }

  if (error) {
    return <p className="px-4 py-6 text-center text-sm text-red-700">Search is unavailable.</p>
  }

  if (results.length === 0) {
    return <SearchEmptyState variant="no-results" />
  }

  return (
    <div>
      <div className="max-h-[360px] overflow-y-auto divide-y divide-app-border">
        {results.map((result) => (
          <SearchResultItem key={`${result.type}-${result.id}`} result={result} onSelect={onSelect} />
        ))}
      </div>
      <div className="border-t border-app-border px-4 py-2 text-xs text-gray-500">
        Showing {results.length} results
      </div>
    </div>
  )
}
