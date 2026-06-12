import { Link } from 'react-router-dom'

import { EmptyState } from '@/components/ui/EmptyState'
import { Badge } from '@/components/ui/Badge'
import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import type { HighPriorityWorkItem } from '@/features/dashboard/types'
import {
  formatDate,
  formatEntityType,
  getPriorityVariant,
  isOverdue,
} from '@/features/dashboard/utils'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { formatLabel } from '@/lib/utils'
import { cn } from '@/lib/utils'

interface HighPriorityWorkItemsCardProps {
  items?: HighPriorityWorkItem[]
  isLoading?: boolean
  error?: string | null
}

export function HighPriorityWorkItemsCard({
  items = [],
  isLoading = false,
  error = null,
}: HighPriorityWorkItemsCardProps) {
  return (
    <DashboardSection
      title="High Priority Work"
      description="Open high and critical priority items needing attention."
      isLoading={isLoading}
      error={error}
      action={
        <div className="flex items-center gap-3">
          <Link to="/work-board" className="text-sm font-medium text-core-blue hover:underline">
            View board
          </Link>
          <Link to="/work-items" className="text-sm font-medium text-core-blue hover:underline">
            View all
          </Link>
        </div>
      }
    >
      {items.length === 0 ? (
        <EmptyState
          title="No high priority work"
          description="High and critical open work items will appear here."
        />
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <div
              key={item.id}
              className="flex flex-col gap-2 border-b border-app-border pb-3 last:border-b-0 last:pb-0 sm:flex-row sm:items-center sm:justify-between"
            >
              <div className="min-w-0">
                <Link
                  to={`/work-items/${item.id}`}
                  className="font-medium text-gray-900 hover:text-core-blue"
                >
                  {item.title}
                </Link>
                <div className="mt-1 flex flex-wrap items-center gap-2">
                  <Badge variant="neutral">{formatEntityType(item.type)}</Badge>
                  <Badge variant={getPriorityVariant(item.priority)}>
                    {formatLabel(item.priority)}
                  </Badge>
                  <StatusBadge status={item.status} />
                </div>
              </div>
              <div
                className={cn(
                  'shrink-0 text-sm',
                  isOverdue(item.due_date) ? 'font-medium text-status-danger' : 'text-gray-500',
                )}
              >
                Due {formatDate(item.due_date)}
              </div>
            </div>
          ))}
        </div>
      )}
    </DashboardSection>
  )
}
