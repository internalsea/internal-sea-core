import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import { ProjectHealthBadge } from '@/features/projects/components/ProjectHealthBadge'
import { ProjectStatusBadge } from '@/features/projects/components/ProjectStatusBadge'
import { ProjectTypeBadge } from '@/features/projects/components/ProjectTypeBadge'
import type { ProjectListItem, ProjectVariant } from '@/features/projects/types'
import {
  formatDateTime,
  getProjectTimelineLabel,
  isProjectOverdue,
  truncateText,
} from '@/features/projects/utils'
import { cn } from '@/lib/utils'

interface ProjectTableProps {
  items: ProjectListItem[]
  variant?: ProjectVariant
  isLoading?: boolean
  onOpen: (id: string) => void
  onEdit: (id: string) => void
  onDelete: (item: ProjectListItem) => void
}

export function ProjectTable({
  items,
  variant = 'projects',
  isLoading = false,
  onOpen,
  onEdit,
  onDelete,
}: ProjectTableProps) {
  const canWrite = useCanWrite()
  const isInternal = variant === 'internal-projects'

  if (isLoading) {
    return <LoadingState message="Loading projects…" />
  }

  if (items.length === 0) {
    return null
  }

  const headers = [
    'Name',
    ...(isInternal ? [] : ['Type']),
    'Status',
    'Health',
    ...(isInternal ? [] : ['Client']),
    'Timeline',
    'Updated',
    'Actions',
  ]

  return (
    <div className="overflow-hidden rounded-card border border-app-border bg-app-surface">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-app-border">
          <thead className="bg-app-background">
            <tr>
              {headers.map((header) => (
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
                    <p className="mt-0.5 text-xs text-gray-500">
                      {truncateText(item.description, 80)}
                    </p>
                  ) : null}
                </td>
                {!isInternal ? (
                  <td className="px-4 py-3 whitespace-nowrap">
                    <ProjectTypeBadge type={item.project_type} />
                  </td>
                ) : null}
                <td className="px-4 py-3 whitespace-nowrap">
                  <ProjectStatusBadge status={item.status} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <ProjectHealthBadge healthStatus={item.health_status} />
                </td>
                {!isInternal ? (
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                    {item.client_name ?? '—'}
                  </td>
                ) : null}
                <td
                  className={cn(
                    'px-4 py-3 whitespace-nowrap text-sm',
                    isProjectOverdue(item) ? 'text-status-danger' : 'text-gray-700',
                  )}
                >
                  {getProjectTimelineLabel(item)}
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
