import { LoadingState } from '@/components/common/LoadingState'
import { WorkItemBoardColumnView } from '@/features/work-items/components/WorkItemBoardColumn'
import type { WorkItemBoardColumn, WorkItemStatus } from '@/features/work-items/types'

interface WorkItemBoardProps {
  columns: WorkItemBoardColumn[]
  isLoading?: boolean
  onOpenItem: (id: string) => void
  onEditItem: (id: string) => void
  onStatusChange: (id: string, status: WorkItemStatus) => void
  updatingItemId?: string | null
}

export function WorkItemBoard({
  columns,
  isLoading = false,
  onOpenItem,
  onEditItem,
  onStatusChange,
  updatingItemId,
}: WorkItemBoardProps) {
  if (isLoading) {
    return <LoadingState message="Loading board…" />
  }

  return (
    <div className="flex gap-4 overflow-x-auto pb-2">
      {columns.map((column) => (
        <WorkItemBoardColumnView
          key={column.status}
          column={column}
          onOpenItem={onOpenItem}
          onEditItem={onEditItem}
          onStatusChange={onStatusChange}
          updatingItemId={updatingItemId}
        />
      ))}
    </div>
  )
}
