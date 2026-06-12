import { Link } from 'react-router-dom'

import { Badge } from '@/components/ui/Badge'
import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { formatDateTime, formatEntityType, getDashboardEntityHref } from '@/features/dashboard/utils'
import type { RecentActivityResponse } from '@/features/dashboard/types'

interface RecentActivityCardProps {
  data: RecentActivityResponse | undefined
  isLoading: boolean
  error: string | null
}

export function RecentActivityCard({ data, isLoading, error }: RecentActivityCardProps) {
  return (
    <DashboardSection
      title="Recent activity"
      description="Latest changes across entities."
      isLoading={isLoading}
      error={error}
    >
      {data && data.items.length === 0 ? (
        <p className="text-sm text-gray-500">No recent activity.</p>
      ) : null}
      {data && data.items.length > 0 ? (
        <ul className="divide-y divide-app-border">
          {data.items.map((item) => {
            const href = getDashboardEntityHref(item.entity_type, item.entity_id)
            return (
              <li key={item.id} className="py-3 first:pt-0">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant="neutral">{item.action}</Badge>
                  <span className="text-xs text-gray-500">{formatEntityType(item.entity_type)}</span>
                </div>
                {href ? (
                  <Link to={href} className="mt-1 block font-medium text-core-blue hover:underline">
                    {item.title}
                  </Link>
                ) : (
                  <p className="mt-1 font-medium text-gray-900">{item.title}</p>
                )}
                {item.description ? <p className="mt-1 text-sm text-gray-600">{item.description}</p> : null}
                <p className="mt-1 text-xs text-gray-500">{formatDateTime(item.created_at)}</p>
              </li>
            )
          })}
        </ul>
      ) : null}
    </DashboardSection>
  )
}
