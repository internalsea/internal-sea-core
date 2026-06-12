import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import type { CapabilityListItem } from '@/features/capabilities/types'
import { formatDateTime, truncateText } from '@/features/capabilities/utils'
import { cn } from '@/lib/utils'

interface CapabilitiesTableProps {
  items: CapabilityListItem[]
  isLoading?: boolean
  onOpen: (id: string) => void
  onEdit: (id: string) => void
  onDelete: (item: CapabilityListItem) => void
}

export function CapabilitiesTable({
  items,
  isLoading = false,
  onOpen,
  onEdit,
  onDelete,
}: CapabilitiesTableProps) {
  const canWrite = useCanWrite()

  if (isLoading) {
    return <LoadingState message="Loading capabilities…" />
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
              {['Name', 'Description', 'Updated', 'Actions'].map((header) => (
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
                </td>
                <td className="px-4 py-3 text-sm text-gray-700">
                  {item.description ? truncateText(item.description, 100) : '—'}
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
