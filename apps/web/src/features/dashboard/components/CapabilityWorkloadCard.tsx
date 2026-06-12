import { Link } from 'react-router-dom'

import { EmptyState } from '@/components/ui/EmptyState'
import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import type { CapabilityWorkloadItem } from '@/features/dashboard/types'
import { formatCount } from '@/features/dashboard/utils'

interface CapabilityWorkloadCardProps {
  items?: CapabilityWorkloadItem[]
  isLoading?: boolean
  error?: string | null
}

export function CapabilityWorkloadCard({
  items = [],
  isLoading = false,
  error = null,
}: CapabilityWorkloadCardProps) {
  return (
    <DashboardSection
      title="Capability Workload"
      description="People, open work and active delivery load by capability."
      isLoading={isLoading}
      error={error}
      action={
        <Link to="/capabilities" className="text-sm font-medium text-core-blue hover:underline">
          View capabilities
        </Link>
      }
    >
      {items.length === 0 ? (
        <EmptyState
          title="No capabilities yet"
          description="Capability workload appears once capabilities and linked records exist."
        />
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-app-border text-left text-xs uppercase tracking-wide text-gray-500">
                <th className="pb-2 pr-4 font-medium">Capability</th>
                <th className="pb-2 pr-4 font-medium">People</th>
                <th className="pb-2 pr-4 font-medium">Open Work</th>
                <th className="pb-2 pr-4 font-medium">Projects</th>
                <th className="pb-2 font-medium">Products</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-app-border">
              {items.map((item) => (
                <tr key={item.capability_id}>
                  <td className="py-2.5 pr-4">
                    <Link
                      to={`/capabilities/${item.capability_id}`}
                      className="font-medium text-gray-900 hover:text-core-blue"
                    >
                      {item.capability_name}
                    </Link>
                  </td>
                  <td className="py-2.5 pr-4 text-gray-700">
                    {formatCount(item.active_people_count)}
                    <span className="text-gray-400"> / {formatCount(item.people_count)}</span>
                  </td>
                  <td className="py-2.5 pr-4 text-gray-700">{formatCount(item.open_work_items)}</td>
                  <td className="py-2.5 pr-4 text-gray-700">
                    {formatCount(item.active_projects)}
                  </td>
                  <td className="py-2.5 text-gray-700">
                    {formatCount(item.active_data_products)}
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
