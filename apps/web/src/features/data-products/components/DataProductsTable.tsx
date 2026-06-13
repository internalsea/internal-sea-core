import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { useCanWrite } from '@/features/auth/hooks'
import type { DataProductListItem } from '@/features/data-products/types'
import { formatDateTime, truncateText } from '@/features/data-products/utils'
import { cn } from '@/lib/utils'

interface DataProductsTableProps {
  items: DataProductListItem[]
  isLoading?: boolean
  onOpen: (id: string) => void
  onEdit: (id: string) => void
  onDelete: (item: DataProductListItem) => void
}

export function DataProductsTable({
  items,
  isLoading = false,
  onOpen,
  onEdit,
  onDelete,
}: DataProductsTableProps) {
  const canWrite = useCanWrite()

  if (isLoading) {
    return <LoadingState message="Loading data products…" />
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
              {['Name', 'Type', 'Status', 'Quality', 'Updated', 'Actions'].map((header) => (
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
              ))}
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
                    {item.name}
                  </button>
                  {item.description ? (
                    <p className="mt-0.5 text-xs text-gray-500">{truncateText(item.description, 80)}</p>
                  ) : null}
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <StatusBadge status={item.type} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <StatusBadge status={item.status} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <StatusBadge status={item.quality_status} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {formatDateTime(item.updated_at)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-right text-sm">
                  <div className="inline-flex items-center gap-2">
                    <Button type="button" variant="ghost" size="sm" onClick={() => onOpen(item.id)}>
                      View
                    </Button>
                    {canWrite ? (
                      <>
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
                      </>
                    ) : null}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
