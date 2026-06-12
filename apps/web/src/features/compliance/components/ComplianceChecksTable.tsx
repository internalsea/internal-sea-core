import { Button } from '@/components/ui/Button'
import { ComplianceStatusBadge } from '@/features/compliance/components/ComplianceStatusBadge'
import type { ComplianceCheckListItem } from '@/features/compliance/types'
import { formatDate, formatDateTime, formatSubjectType, isOverdueCheck } from '@/features/compliance/utils'

interface ComplianceChecksTableProps {
  items: ComplianceCheckListItem[]
  isLoading?: boolean
  showWriteActions?: boolean
  onOpen: (id: string) => void
  onEdit: (id: string) => void
  onDelete: (item: ComplianceCheckListItem) => void
}

export function ComplianceChecksTable({
  items,
  isLoading = false,
  showWriteActions = true,
  onOpen,
  onEdit,
  onDelete,
}: ComplianceChecksTableProps) {
  if (isLoading) return <p className="text-sm text-gray-500">Loading compliance checks…</p>

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead className="bg-app-muted">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Title</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Subject</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Status</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Type</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Due</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Updated</th>
            <th className="px-4 py-3 text-right font-medium text-gray-600">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border bg-app-surface">
          {items.map((item) => (
            <tr key={item.id}>
              <td className="px-4 py-3">
                <button type="button" className="font-medium text-core-blue hover:underline" onClick={() => onOpen(item.id)}>
                  {item.title}
                </button>
                {isOverdueCheck(item) ? (
                  <span className="ml-2 text-xs font-medium text-status-danger">Overdue</span>
                ) : null}
              </td>
              <td className="px-4 py-3 text-gray-600">{formatSubjectType(item.subject_type)}</td>
              <td className="px-4 py-3"><ComplianceStatusBadge status={item.status} /></td>
              <td className="px-4 py-3 text-gray-600">{item.check_type.replace('_', ' ')}</td>
              <td className="px-4 py-3 text-gray-600">{formatDate(item.due_date)}</td>
              <td className="px-4 py-3 text-gray-600">{formatDateTime(item.updated_at)}</td>
              <td className="px-4 py-3 text-right">
                <div className="flex justify-end gap-2">
                  <Button variant="ghost" size="sm" onClick={() => onOpen(item.id)}>View</Button>
                  {showWriteActions ? (
                    <>
                      <Button variant="ghost" size="sm" onClick={() => onEdit(item.id)}>Edit</Button>
                      <Button variant="ghost" size="sm" onClick={() => onDelete(item)}>Delete</Button>
                    </>
                  ) : null}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
