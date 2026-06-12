import { EntityTypeBadge } from '@/features/entity-picker/components/EntityTypeBadge'
import { useEntityReference } from '@/features/entity-picker/hooks'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import { shortId } from '@/features/entity-picker/utils'

interface SelectedEntityPillProps {
  value: EntityPickerValue
  onClear?: () => void
  disabled?: boolean
}

export function SelectedEntityPill({ value, onClear, disabled = false }: SelectedEntityPillProps) {
  const needsLookup = !value.title?.trim()
  const { data: reference } = useEntityReference(
    value.entity_type,
    value.entity_id,
    needsLookup,
  )
  const displayTitle = value.title?.trim() || reference?.title || shortId(value.entity_id)
  const displayType = reference?.type ?? value.entity_type

  return (
    <div className="flex items-center gap-2 rounded-md border border-app-border bg-app-muted px-3 py-2">
      <EntityTypeBadge type={displayType} />
      <span className="min-w-0 flex-1 truncate text-sm font-medium text-gray-900">{displayTitle}</span>
      {onClear ? (
        <button
          type="button"
          onClick={onClear}
          disabled={disabled}
          className="shrink-0 text-xs text-gray-500 hover:text-gray-700 disabled:opacity-50"
          aria-label="Clear selection"
        >
          Clear
        </button>
      ) : null}
    </div>
  )
}
