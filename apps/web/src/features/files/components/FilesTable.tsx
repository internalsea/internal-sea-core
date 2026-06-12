import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import { FileSensitivityBadge } from '@/features/files/components/FileSensitivityBadge'
import { FileStatusBadge } from '@/features/files/components/FileStatusBadge'
import { FileTypeBadge } from '@/features/files/components/FileTypeBadge'
import type { FileAssetListItem } from '@/features/files/types'
import { formatDateTime } from '@/features/files/utils'

interface FilesTableProps {
  items: FileAssetListItem[]
  isLoading?: boolean
  onOpen: (id: string) => void
  onEdit: (id: string) => void
  onDelete: (item: FileAssetListItem) => void
}

export function FilesTable({
  items,
  isLoading = false,
  onOpen,
  onEdit,
  onDelete,
}: FilesTableProps) {
  const canWrite = useCanWrite()

  if (isLoading) {
    return <p className="text-sm text-gray-500">Loading files…</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead className="bg-app-muted">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Name</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Type</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Status</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Sensitivity</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Version</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Owner</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Updated</th>
            <th className="px-4 py-3 text-right font-medium text-gray-600">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border bg-app-surface">
          {items.map((item) => (
            <tr key={item.id} className="hover:bg-app-muted/50">
              <td className="px-4 py-3">
                <button
                  type="button"
                  className="font-medium text-core-blue hover:underline"
                  onClick={() => onOpen(item.id)}
                >
                  {item.name}
                </button>
              </td>
              <td className="px-4 py-3">
                <FileTypeBadge fileType={item.file_type} />
              </td>
              <td className="px-4 py-3">
                <FileStatusBadge status={item.status} />
              </td>
              <td className="px-4 py-3">
                <FileSensitivityBadge sensitivity={item.sensitivity} />
              </td>
              <td className="px-4 py-3 text-gray-600">{item.version ?? '—'}</td>
              <td className="px-4 py-3 font-mono text-xs text-gray-500">
                {item.owner_id ? (
                  <Link to={`/people/${item.owner_id}`} className="hover:text-core-blue">
                    {item.owner_id.slice(0, 8)}…
                  </Link>
                ) : (
                  '—'
                )}
              </td>
              <td className="px-4 py-3 text-gray-600">{formatDateTime(item.updated_at)}</td>
              <td className="px-4 py-3 text-right">
                {canWrite ? (
                  <div className="flex justify-end gap-2">
                    <Button variant="ghost" size="sm" onClick={() => onEdit(item.id)}>
                      Edit
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => onDelete(item)}>
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
  )
}
