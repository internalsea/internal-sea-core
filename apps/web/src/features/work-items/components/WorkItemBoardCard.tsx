import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import { WorkItemPriorityBadge } from '@/features/work-items/components/WorkItemPriorityBadge'
import { WorkItemTypeBadge } from '@/features/work-items/components/WorkItemTypeBadge'
import { workItemStatusLabels } from '@/features/work-items/constants'
import type { WorkItemListItem, WorkItemStatus } from '@/features/work-items/types'
import { formatDate, getNextWorkItemStatus, isWorkItemOverdue } from '@/features/work-items/utils'
import { cn } from '@/lib/utils'

interface WorkItemBoardCardProps {
  item: WorkItemListItem
  onOpenItem: (id: string) => void
  onEditItem: (id: string) => void
  onStatusChange: (id: string, status: WorkItemStatus) => void
  isUpdating?: boolean
}

export function WorkItemBoardCard({
  item,
  onOpenItem,
  onEditItem,
  onStatusChange,
  isUpdating = false,
}: WorkItemBoardCardProps) {
  const canWrite = useCanWrite()
  const nextStatus = getNextWorkItemStatus(item.status)

  return (
    <div className="rounded-md border border-app-border bg-app-surface p-3">
      <button
        type="button"
        onClick={() => onOpenItem(item.id)}
        className="text-left text-sm font-medium text-gray-900 hover:text-core-blue"
      >
        {item.title}
      </button>

      <div className="mt-2 flex flex-wrap gap-1.5">
        <WorkItemTypeBadge type={item.type} />
        <WorkItemPriorityBadge priority={item.priority} />
      </div>

      <div className="mt-2 space-y-1 text-xs text-gray-500">
        {item.due_date ? (
          <p className={cn(isWorkItemOverdue(item) && 'font-medium text-status-danger')}>
            Due {formatDate(item.due_date)}
          </p>
        ) : null}
        {item.estimate_points !== null && item.estimate_points !== undefined ? (
          <p>{item.estimate_points} pts</p>
        ) : null}
        {item.data_product_id ? (
          <p className="truncate" title={item.data_product_id}>
            Product: {item.data_product_id.slice(0, 8)}…
          </p>
        ) : null}
      </div>

      <div className="mt-3 flex flex-wrap gap-1.5">
        <Button type="button" variant="ghost" size="sm" onClick={() => onOpenItem(item.id)}>
          Open
        </Button>
        {canWrite ? (
          <>
            <Button type="button" variant="ghost" size="sm" onClick={() => onEditItem(item.id)}>
              Edit
            </Button>
            {nextStatus ? (
              <Button
                type="button"
                variant="secondary"
                size="sm"
                disabled={isUpdating}
                onClick={() => onStatusChange(item.id, nextStatus)}
              >
                Move to {workItemStatusLabels[nextStatus]}
              </Button>
            ) : null}
          </>
        ) : null}
      </div>
    </div>
  )
}
