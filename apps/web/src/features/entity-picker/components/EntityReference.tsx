import { Link } from 'react-router-dom'

import { EntityTypeBadge } from '@/features/entity-picker/components/EntityTypeBadge'
import { useEntityReference } from '@/features/entity-picker/hooks'
import type { EntityReferenceProps } from '@/features/entity-picker/types'
import { getEntityHref, shortId } from '@/features/entity-picker/utils'

export function EntityReference({
  entityType,
  entityId,
  showType = true,
  link = true,
  fallbackLabel,
}: EntityReferenceProps) {
  const { data, isLoading, isError } = useEntityReference(entityType, entityId)

  if (isLoading) {
    return <span className="text-sm text-gray-500">{shortId(entityId)}</span>
  }

  if (isError || !data) {
    return (
      <span className="text-sm text-gray-500" title="Could not load entity name">
        {fallbackLabel ?? shortId(entityId)}
      </span>
    )
  }

  const href = data.url || getEntityHref(data.type, data.id)
  const content = (
    <span className="inline-flex flex-wrap items-center gap-2">
      {showType ? <EntityTypeBadge type={data.type} /> : null}
      <span className="text-sm text-gray-900">{data.title}</span>
    </span>
  )

  if (link) {
    return (
      <Link to={href} className="hover:underline">
        {content}
      </Link>
    )
  }

  return content
}
