import { Link } from 'react-router-dom'

import { Badge } from '@/components/ui/Badge'
import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { HealthScoreBadge } from '@/features/dashboard/components/HealthScoreBadge'
import { formatCount, formatScore, getQualityVariant } from '@/features/dashboard/utils'
import type { DataProductHealthResponse } from '@/features/dashboard/types'

interface DataProductHealthCardProps {
  data: DataProductHealthResponse | undefined
  isLoading: boolean
  error: string | null
}

export function DataProductHealthCard({ data, isLoading, error }: DataProductHealthCardProps) {
  return (
    <DashboardSection
      title="Data product health"
      description="Quality, ownership and operational signals for active catalog objects."
      isLoading={isLoading}
      error={error}
      action={<Link to="/data-products" className="text-sm text-core-blue hover:underline">Catalog</Link>}
    >
      {data ? (
        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            {formatCount(data.active)} active · {formatCount(data.missing_owner_count)} missing owner
          </p>
          <ul className="divide-y divide-app-border">
            {data.items.map((item) => (
              <li key={item.id} className="py-3 first:pt-0">
                <div className="flex flex-wrap items-center gap-2">
                  <Link to={`/data-products/${item.id}`} className="font-medium text-core-blue hover:underline">
                    {item.name}
                  </Link>
                  <HealthScoreBadge status={item.health_status} />
                  {item.quality_status ? (
                    <Badge variant={getQualityVariant(item.quality_status)}>{item.quality_status}</Badge>
                  ) : null}
                </div>
                <p className="mt-1 text-sm text-gray-600">
                  Work {item.open_work_items} · compliance {item.compliance_open_checks}
                  {item.latest_performance_score != null
                    ? ` · score ${formatScore(item.latest_performance_score)}`
                    : ''}
                </p>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </DashboardSection>
  )
}
