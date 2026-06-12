import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { EvidenceStatusBadge } from '@/features/compliance/components/EvidenceStatusBadge'
import type { ComplianceEvidence } from '@/features/compliance/types'
import { formatDateTime } from '@/features/compliance/utils'

interface ComplianceEvidenceListProps {
  items: ComplianceEvidence[]
  onDelete?: (item: ComplianceEvidence) => void
  isDeleting?: boolean
}

export function ComplianceEvidenceList({ items, onDelete, isDeleting = false }: ComplianceEvidenceListProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No evidence linked yet.</p>
  }

  return (
    <ul className="divide-y divide-app-border">
      {items.map((item) => (
        <li key={item.id} className="flex items-start justify-between gap-3 py-3">
          <div className="space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <Link to={`/files/${item.file_id}`} className="font-medium text-core-blue hover:underline">
                {item.file_id}
              </Link>
              <EvidenceStatusBadge status={item.status} />
            </div>
            {item.description ? <p className="text-sm text-gray-600">{item.description}</p> : null}
            <p className="text-xs text-gray-400">Added {formatDateTime(item.created_at)}</p>
          </div>
          {onDelete ? (
            <Button variant="ghost" size="sm" disabled={isDeleting} onClick={() => onDelete(item)}>
              Remove
            </Button>
          ) : null}
        </li>
      ))}
    </ul>
  )
}
