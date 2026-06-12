import { EntityPickerResultItem } from '@/features/entity-picker/components/EntityPickerResultItem'
import type { EntityPickerResult } from '@/features/entity-picker/types'

interface EntityPickerDropdownProps {
  results: EntityPickerResult[]
  isLoading: boolean
  isError: boolean
  query: string
  activeIndex: number
  onSelect: (result: EntityPickerResult) => void
}

export function EntityPickerDropdown({
  results,
  isLoading,
  isError,
  query,
  activeIndex,
  onSelect,
}: EntityPickerDropdownProps) {
  return (
    <div
      role="listbox"
      className="absolute z-20 mt-1 max-h-80 w-full overflow-y-auto rounded-md border border-app-border bg-white shadow-lg"
    >
      {isLoading ? (
        <p className="px-3 py-2 text-sm text-gray-500">Searching…</p>
      ) : isError ? (
        <p className="px-3 py-2 text-sm text-status-danger">Search failed. Try again.</p>
      ) : results.length === 0 ? (
        <p className="px-3 py-2 text-sm text-gray-500">
          {query.trim().length < 2 ? 'Type at least 2 characters to search' : 'No results found'}
        </p>
      ) : (
        results.map((result, index) => (
          <EntityPickerResultItem
            key={`${result.type}-${result.id}`}
            result={result}
            isActive={index === activeIndex}
            onSelect={onSelect}
          />
        ))
      )}
    </div>
  )
}
