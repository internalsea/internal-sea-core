import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import { PolicyStatusBadge } from '@/features/compliance/components/PolicyStatusBadge'
import type { PolicyListItem } from '@/features/compliance/types'
import { formatDateTime } from '@/features/compliance/utils'

interface PoliciesTableProps {
  items: PolicyListItem[]
  isLoading?: boolean
  onOpen: (id: string) => void
  onEdit: (id: string) => void
  onDelete: (item: PolicyListItem) => void
}

export function PoliciesTable({
  items,
  isLoading = false,
  onOpen,
  onEdit,
  onDelete,
}: PoliciesTableProps) {
  const canWrite = useCanWrite()

  if (isLoading) return <p className="text-sm text-gray-500">Loading policies…</p>

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead className="bg-app-muted">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Name</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Status</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Version</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Effective</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Updated</th>
            <th className="px-4 py-3 text-right font-medium text-gray-600">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border bg-app-surface">
          {items.map((item) => (
            <tr key={item.id}>
              <td className="px-4 py-3">
                <button type="button" className="font-medium text-core-blue hover:underline" onClick={() => onOpen(item.id)}>
                  {item.name}
                </button>
              </td>
              <td className="px-4 py-3"><PolicyStatusBadge status={item.status} /></td>
              <td className="px-4 py-3 text-gray-600">{item.version ?? '—'}</td>
              <td className="px-4 py-3 text-gray-600">
                {item.effective_from || item.effective_to
                  ? `${item.effective_from ?? '…'} – ${item.effective_to ?? '…'}`
                  : '—'}
              </td>
              <td className="px-4 py-3 text-gray-600">{formatDateTime(item.updated_at)}</td>
              <td className="px-4 py-3 text-right">
                <div className="flex justify-end gap-2">
                  <Link to={`/compliance/policies/${item.id}`}><Button variant="ghost" size="sm">View</Button></Link>
                  {canWrite ? (
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
