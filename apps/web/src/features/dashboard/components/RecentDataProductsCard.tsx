import { Link } from 'react-router-dom'

import { EmptyState } from '@/components/ui/EmptyState'
import { Badge } from '@/components/ui/Badge'
import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import type { RecentDataProductItem } from '@/features/dashboard/types'
import {
  formatDateTime,
  formatEntityType,
  getQualityVariant,
  getStatusVariant,
} from '@/features/dashboard/utils'
import { formatLabel } from '@/lib/utils'

interface RecentDataProductsCardProps {
  items?: RecentDataProductItem[]
  isLoading?: boolean
  error?: string | null
}

export function RecentDataProductsCard({
  items = [],
  isLoading = false,
  error = null,
}: RecentDataProductsCardProps) {
  return (
    <DashboardSection
      title="Recent Data Products"
      description="Latest catalog updates across business domains."
      isLoading={isLoading}
      error={error}
      action={
        <Link to="/data-products" className="text-sm font-medium text-core-blue hover:underline">
          View all
        </Link>
      }
    >
      {items.length === 0 ? (
        <EmptyState
          title="No data products yet"
          description="Create a data product or run make seed to load demo catalog records."
        />
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-app-border text-left text-xs uppercase tracking-wide text-gray-500">
                <th className="pb-2 pr-4 font-medium">Name</th>
                <th className="pb-2 pr-4 font-medium">Type</th>
                <th className="pb-2 pr-4 font-medium">Status</th>
                <th className="pb-2 pr-4 font-medium">Quality</th>
                <th className="pb-2 font-medium">Updated</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-app-border">
              {items.map((item) => (
                <tr key={item.id}>
                  <td className="py-2.5 pr-4">
                    <Link
                      to={`/data-products/${item.id}`}
                      className="font-medium text-gray-900 hover:text-core-blue"
                    >
                      {item.name}
                    </Link>
                  </td>
                  <td className="py-2.5 pr-4">
                    <Badge variant="neutral">{formatEntityType(item.type)}</Badge>
                  </td>
                  <td className="py-2.5 pr-4">
                    <Badge variant={getStatusVariant(item.status)}>
                      {formatLabel(item.status)}
                    </Badge>
                  </td>
                  <td className="py-2.5 pr-4">
                    <Badge variant={getQualityVariant(item.quality_status)}>
                      {formatLabel(item.quality_status)}
                    </Badge>
                  </td>
                  <td className="py-2.5 text-gray-500">{formatDateTime(item.updated_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </DashboardSection>
  )
}
