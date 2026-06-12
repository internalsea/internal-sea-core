import { Badge } from '@/components/ui/Badge'
import { WorkItemBoardCard } from '@/features/work-items/components/WorkItemBoardCard'
import type { WorkItemBoardColumn, WorkItemStatus } from '@/features/work-items/types'

interface WorkItemBoardColumnProps {
  column: WorkItemBoardColumn
  onOpenItem: (id: string) => void
  onEditItem: (id: string) => void
  onStatusChange: (id: string, status: WorkItemStatus) => void
  updatingItemId?: string | null
}

export function WorkItemBoardColumnView({
  column,
  onOpenItem,
  onEditItem,
  onStatusChange,
  updatingItemId,
}: WorkItemBoardColumnProps) {
  return (
    <div className="flex w-72 shrink-0 flex-col rounded-card border border-app-border bg-app-background">
      <div className="flex items-center justify-between border-b border-app-border px-4 py-3">
        <h3 className="text-sm font-semibold text-gray-900">{column.title}</h3>
        <Badge variant="neutral">{String(column.count)}</Badge>
      </div>
      <div className="flex-1 space-y-3 overflow-y-auto p-3">
        {column.items.length === 0 ? (
          <p className="py-6 text-center text-xs text-gray-500">No items</p>
        ) : (
          column.items.map((item) => (
            <WorkItemBoardCard
              key={item.id}
              item={item}
              onOpenItem={onOpenItem}
              onEditItem={onEditItem}
              onStatusChange={onStatusChange}
              isUpdating={updatingItemId === item.id}
            />
          ))
        )}
      </div>
    </div>
  )
}
