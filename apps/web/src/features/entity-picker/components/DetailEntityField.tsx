import { EntityReference } from '@/features/entity-picker/components/EntityReference'
import { ENTITY_PICKER_TYPES } from '@/features/entity-picker/constants'
import type { EntityPickerType } from '@/features/entity-picker/types'
import { shortId } from '@/features/entity-picker/utils'

interface DetailEntityFieldProps {
  label: string
  entityType: EntityPickerType | string
  entityId: string | null | undefined
}

function isPickerType(type: string): type is EntityPickerType {
  return ENTITY_PICKER_TYPES.includes(type as EntityPickerType)
}

export function DetailEntityField({ label, entityType, entityId }: DetailEntityFieldProps) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-700">
        {!entityId ? (
          '—'
        ) : isPickerType(entityType) ? (
          <EntityReference entityType={entityType} entityId={entityId} />
        ) : (
          <span className="font-mono text-xs text-gray-600">{shortId(entityId)}</span>
        )}
      </dd>
    </div>
  )
}
