import { Link } from 'react-router-dom'

import { EmptyState } from '@/components/ui/EmptyState'
import { Badge } from '@/components/ui/Badge'
import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import type { OwnershipGapItem } from '@/features/dashboard/types'
import {
  formatEntityType,
  getOwnershipGapHref,
  getSeverityVariant,
} from '@/features/dashboard/utils'
import { formatLabel } from '@/lib/utils'

interface OwnershipGapsCardProps {
  items?: OwnershipGapItem[]
  isLoading?: boolean
  error?: string | null
}

export function OwnershipGapsCard({
  items = [],
  isLoading = false,
  error = null,
}: OwnershipGapsCardProps) {
  return (
    <DashboardSection
      title="Ownership Gaps"
      description="Missing owners, teams and assignees across catalog and delivery."
      isLoading={isLoading}
      error={error}
    >
      {items.length === 0 ? (
        <EmptyState title="No ownership gaps found" description="All tracked records have required ownership." />
      ) : (
        <div className="space-y-3">
          {items.map((item) => {
            const href = getOwnershipGapHref(item)
            const name = href ? (
              <Link to={href} className="font-medium text-gray-900 hover:text-core-blue">
                {item.name}
              </Link>
            ) : (
              <span className="font-medium text-gray-900">{item.name}</span>
            )

            return (
              <div
                key={`${item.entity_type}-${item.entity_id}-${item.gap_type}`}
                className="border-b border-app-border pb-3 last:border-b-0 last:pb-0"
              >
                <div className="flex flex-wrap items-center gap-2">
                  {name}
                  <Badge variant="neutral">{formatEntityType(item.entity_type)}</Badge>
                  <Badge variant={getSeverityVariant(item.severity)}>
                    {formatLabel(item.severity)}
                  </Badge>
                </div>
                <p className="mt-1 text-sm text-gray-600">{item.description}</p>
                <p className="mt-1 text-xs text-gray-400">{formatLabel(item.gap_type)}</p>
              </div>
            )
          })}
        </div>
      )}
    </DashboardSection>
  )
}
