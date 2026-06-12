import { Button } from '@/components/ui/Button'
import { EntityReference } from '@/features/entity-picker/components/EntityReference'
import { ENTITY_PICKER_TYPES } from '@/features/entity-picker/constants'
import type { EntityPickerType } from '@/features/entity-picker/types'
import { shortId } from '@/features/entity-picker/utils'
import { EntityTypeBadge } from '@/features/relationships/components/EntityTypeBadge'
import { RelationshipTypeBadge } from '@/features/relationships/components/RelationshipTypeBadge'
import type { EntityLink, EntityType } from '@/features/relationships/types'
import { formatDateTime } from '@/features/relationships/utils'

interface RelationshipItemProps {
  link: EntityLink
  direction: 'outgoing' | 'incoming'
  onDelete?: (linkId: string) => void
  isDeleting?: boolean
}

function isPickerType(type: EntityType): type is EntityPickerType {
  return ENTITY_PICKER_TYPES.includes(type as EntityPickerType)
}

function RelatedEntityDisplay({
  entityType,
  entityId,
}: {
  entityType: EntityType
  entityId: string
}) {
  if (isPickerType(entityType)) {
    return <EntityReference entityType={entityType} entityId={entityId} />
  }

  return <span className="font-mono text-xs text-gray-600">{shortId(entityId)}</span>
}

export function RelationshipItem({
  link,
  direction,
  onDelete,
  isDeleting = false,
}: RelationshipItemProps) {
  const isOutgoing = direction === 'outgoing'
  const relatedType = isOutgoing ? link.target_type : link.source_type
  const relatedId = isOutgoing ? link.target_id : link.source_id

  return (
    <li className="border-b border-app-border py-4 last:border-b-0">
      <div className="flex flex-wrap items-center gap-2">
        <RelationshipTypeBadge linkType={link.link_type} />
        <EntityTypeBadge entityType={relatedType} />
        <span className="text-xs text-gray-400">{formatDateTime(link.created_at)}</span>
      </div>
      <p className="mt-2 flex flex-wrap items-center gap-1 text-sm text-gray-700">
        {isOutgoing ? (
          <>
            <span>This object →</span>
            <RelatedEntityDisplay entityType={relatedType} entityId={relatedId} />
          </>
        ) : (
          <>
            <RelatedEntityDisplay entityType={relatedType} entityId={relatedId} />
            <span>→ this object</span>
          </>
        )}
      </p>
      {link.title ? <p className="mt-1 text-sm font-medium text-gray-900">{link.title}</p> : null}
      {link.description ? (
        <p className="mt-1 text-sm text-gray-600">{link.description}</p>
      ) : null}
      {onDelete ? (
        <div className="mt-3">
          <Button
            variant="ghost"
            className="text-status-danger hover:text-status-danger"
            disabled={isDeleting}
            onClick={() => onDelete(link.id)}
          >
            {isDeleting ? 'Removing…' : 'Remove'}
          </Button>
        </div>
      ) : null}
    </li>
  )
}
