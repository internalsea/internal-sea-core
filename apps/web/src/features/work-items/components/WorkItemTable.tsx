import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import { WorkItemPriorityBadge } from '@/features/work-items/components/WorkItemPriorityBadge'
import { WorkItemStatusBadge } from '@/features/work-items/components/WorkItemStatusBadge'
import { WorkItemTypeBadge } from '@/features/work-items/components/WorkItemTypeBadge'
import type { WorkItemListItem } from '@/features/work-items/types'
import { formatDate, formatDateTime, isWorkItemOverdue, truncateText } from '@/features/work-items/utils'
import { cn } from '@/lib/utils'

interface WorkItemTableProps {
  items: WorkItemListItem[]
  isLoading?: boolean
  onOpen: (id: string) => void
  onEdit: (id: string) => void
  onDelete: (item: WorkItemListItem) => void
}

export function WorkItemTable({
  items,
  isLoading = false,
  onOpen,
  onEdit,
  onDelete,
}: WorkItemTableProps) {
  const canWrite = useCanWrite()

  if (isLoading) {
    return <LoadingState message="Loading work items…" />
  }

  if (items.length === 0) {
    return null
  }

  return (
    <div className="overflow-hidden rounded-card border border-app-border bg-app-surface">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-app-border">
          <thead className="bg-app-background">
            <tr>
              {['Title', 'Type', 'Status', 'Priority', 'Due Date', 'Estimate', 'Updated', 'Actions'].map(
                (header) => (
                  <th
                    key={header}
                    scope="col"
                    className={cn(
                      'px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500',
                      header === 'Actions' && 'text-right',
                    )}
                  >
                    {header}
                  </th>
                ),
              )}
            </tr>
          </thead>
          <tbody className="divide-y divide-app-border">
            {items.map((item) => (
              <tr key={item.id} className="hover:bg-app-background">
                <td className="px-4 py-3">
                  <button
                    type="button"
                    onClick={() => onOpen(item.id)}
                    className="text-left text-sm font-medium text-gray-900 hover:text-core-blue"
                  >
                    {item.title}
                  </button>
                  {item.description ? (
                    <p className="mt-0.5 text-xs text-gray-500">
                      {truncateText(item.description, 80)}
                    </p>
                  ) : null}
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <WorkItemTypeBadge type={item.type} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <WorkItemStatusBadge status={item.status} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <WorkItemPriorityBadge priority={item.priority} />
                </td>
                <td
                  className={cn(
                    'px-4 py-3 whitespace-nowrap text-sm',
                    isWorkItemOverdue(item) ? 'text-status-danger' : 'text-gray-700',
                  )}
                >
                  {formatDate(item.due_date)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {item.estimate_points ?? '—'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {formatDateTime(item.updated_at)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-right text-sm">
                  {canWrite ? (
                    <div className="inline-flex items-center gap-2">
                      <Button type="button" variant="ghost" size="sm" onClick={() => onEdit(item.id)}>
                        Edit
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="text-status-danger hover:text-status-danger"
                        onClick={() => onDelete(item)}
                      >
                        Delete
                      </Button>
                    </div>
                  ) : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
