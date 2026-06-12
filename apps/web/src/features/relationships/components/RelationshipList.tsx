import { EmptyState } from '@/components/ui/EmptyState'
import { RelationshipItem } from '@/features/relationships/components/RelationshipItem'
import type { EntityLink } from '@/features/relationships/types'

interface RelationshipListProps {
  outgoing: EntityLink[]
  incoming: EntityLink[]
  onDelete?: (linkId: string) => void
  deletingLinkId?: string | null
}

export function RelationshipList({
  outgoing,
  incoming,
  onDelete,
  deletingLinkId = null,
}: RelationshipListProps) {
  if (outgoing.length === 0 && incoming.length === 0) {
    return (
      <EmptyState
        title="No relationships yet"
        description="Connect this object to related products, work, projects, people, teams or capabilities."
      />
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h4 className="mb-2 text-sm font-semibold text-gray-900">Outgoing relationships</h4>
        {outgoing.length === 0 ? (
          <p className="text-sm text-gray-500">No outgoing links.</p>
        ) : (
          <ul>
            {outgoing.map((link) => (
              <RelationshipItem
                key={link.id}
                link={link}
                direction="outgoing"
                onDelete={onDelete}
                isDeleting={deletingLinkId === link.id}
              />
            ))}
          </ul>
        )}
      </div>
      <div>
        <h4 className="mb-2 text-sm font-semibold text-gray-900">Incoming relationships</h4>
        {incoming.length === 0 ? (
          <p className="text-sm text-gray-500">No incoming links.</p>
        ) : (
          <ul>
            {incoming.map((link) => (
              <RelationshipItem
                key={link.id}
                link={link}
                direction="incoming"
                onDelete={onDelete}
                isDeleting={deletingLinkId === link.id}
              />
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
