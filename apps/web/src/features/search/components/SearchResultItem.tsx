import { SearchResultTypeBadge } from '@/features/search/components/SearchResultTypeBadge'
import type { SearchResult } from '@/features/search/types'
import { buildResultMeta, formatSearchDate } from '@/features/search/utils'

interface SearchResultItemProps {
  result: SearchResult
  onSelect: (result: SearchResult) => void
}

export function SearchResultItem({ result, onSelect }: SearchResultItemProps) {
  const meta = buildResultMeta(result)
  const updatedLabel = formatSearchDate(result.updated_at)

  return (
    <button
      type="button"
      onClick={() => onSelect(result)}
      className="flex w-full items-start gap-3 px-4 py-3 text-left transition-colors hover:bg-app-muted"
    >
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <SearchResultTypeBadge type={result.type} />
          <span className="truncate text-sm font-medium text-gray-900">{result.title}</span>
        </div>
        {meta ? <p className="mt-1 truncate text-sm text-gray-500">{meta}</p> : null}
        {updatedLabel ? <p className="mt-1 text-xs text-gray-400">Updated {updatedLabel}</p> : null}
      </div>
    </button>
  )
}
