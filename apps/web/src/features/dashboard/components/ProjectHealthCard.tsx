import { Link } from 'react-router-dom'

import { EmptyState } from '@/components/ui/EmptyState'
import { Badge } from '@/components/ui/Badge'
import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import type { ProjectHealthItem } from '@/features/dashboard/types'
import {
  formatDate,
  formatEntityType,
  getHealthVariant,
  getProjectHref,
} from '@/features/dashboard/utils'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { formatLabel } from '@/lib/utils'

interface ProjectHealthCardProps {
  items?: ProjectHealthItem[]
  isLoading?: boolean
  error?: string | null
}

export function ProjectHealthCard({
  items = [],
  isLoading = false,
  error = null,
}: ProjectHealthCardProps) {
  return (
    <DashboardSection
      title="Project Health"
      description="Active and at-risk projects with open and overdue work."
      isLoading={isLoading}
      error={error}
      action={
        <div className="flex items-center gap-3">
          <Link to="/projects" className="text-sm font-medium text-core-blue hover:underline">
            View projects
          </Link>
          <Link
            to="/internal-projects"
            className="text-sm font-medium text-core-blue hover:underline"
          >
            View internal
          </Link>
        </div>
      }
    >
      {items.length === 0 ? (
        <EmptyState
          title="No active projects"
          description="Active projects and projects with health warnings will appear here."
        />
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-app-border text-left text-xs uppercase tracking-wide text-gray-500">
                <th className="pb-2 pr-4 font-medium">Project</th>
                <th className="pb-2 pr-4 font-medium">Type</th>
                <th className="pb-2 pr-4 font-medium">Health</th>
                <th className="pb-2 pr-4 font-medium">Status</th>
                <th className="pb-2 pr-4 font-medium">Target End</th>
                <th className="pb-2 pr-4 font-medium">Open</th>
                <th className="pb-2 font-medium">Overdue</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-app-border">
              {items.map((item) => (
                <tr key={item.id}>
                  <td className="py-2.5 pr-4">
                    <Link
                      to={getProjectHref(item)}
                      className="font-medium text-gray-900 hover:text-core-blue"
                    >
                      {item.name}
                    </Link>
                    {item.client_name ? (
                      <p className="mt-0.5 text-xs text-gray-500">{item.client_name}</p>
                    ) : null}
                  </td>
                  <td className="py-2.5 pr-4">
                    <Badge variant="neutral">{formatEntityType(item.project_type)}</Badge>
                  </td>
                  <td className="py-2.5 pr-4">
                    <Badge variant={getHealthVariant(item.health_status)}>
                      {formatLabel(item.health_status ?? 'unknown')}
                    </Badge>
                  </td>
                  <td className="py-2.5 pr-4">
                    <StatusBadge status={item.status} />
                  </td>
                  <td className="py-2.5 pr-4 text-gray-500">{formatDate(item.target_end_date)}</td>
                  <td className="py-2.5 pr-4 text-gray-700">{item.open_work_items}</td>
                  <td
                    className={
                      item.overdue_work_items > 0
                        ? 'py-2.5 font-medium text-status-danger'
                        : 'py-2.5 text-gray-700'
                    }
                  >
                    {item.overdue_work_items}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </DashboardSection>
  )
}
