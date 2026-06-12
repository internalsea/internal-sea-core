import { EntityTypeBadge } from '@/features/entity-picker/components/EntityTypeBadge'
import type { EntityPickerResult } from '@/features/entity-picker/types'
import { formatLabel } from '@/lib/utils'

interface EntityPickerResultItemProps {
  result: EntityPickerResult
  isActive?: boolean
  onSelect: (result: EntityPickerResult) => void
}

function formatMeta(result: EntityPickerResult): string | null {
  const parts: string[] = []
  if (result.description) {
    parts.push(result.description)
  }
  if (result.status) {
    parts.push(formatLabel(result.status))
  }
  if (result.secondary_status) {
    parts.push(formatLabel(result.secondary_status))
  }
  return parts.length > 0 ? parts.join(' · ') : null
}

export function EntityPickerResultItem({
  result,
  isActive = false,
  onSelect,
}: EntityPickerResultItemProps) {
  const meta = formatMeta(result)

  return (
    <button
      type="button"
      role="option"
      aria-selected={isActive}
      onClick={() => onSelect(result)}
      className={`flex w-full items-start gap-2 px-3 py-2 text-left hover:bg-app-muted ${
        isActive ? 'bg-app-muted' : ''
      }`}
    >
      <EntityTypeBadge type={result.type} />
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium text-gray-900">{result.title}</p>
        {meta ? <p className="truncate text-xs text-gray-500">{meta}</p> : null}
      </div>
    </button>
  )
}
