import { Link } from 'react-router-dom'

import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { InsightSeverityBadge } from '@/features/dashboard/components/InsightSeverityBadge'
import { formatInsightCategory } from '@/features/dashboard/utils'
import type { ActionableInsightsResponse } from '@/features/dashboard/types'

interface ActionableInsightsCardProps {
  data: ActionableInsightsResponse | undefined
  isLoading: boolean
  error: string | null
}

export function ActionableInsightsCard({ data, isLoading, error }: ActionableInsightsCardProps) {
  return (
    <DashboardSection
      title="Actionable insights"
      description="Deterministic rules highlighting ownership, delivery, compliance and automation gaps."
      isLoading={isLoading}
      error={error}
      className="xl:col-span-2"
    >
      {data && data.items.length === 0 ? (
        <p className="text-sm text-gray-500">No critical insights found.</p>
      ) : null}
      {data && data.items.length > 0 ? (
        <ul className="divide-y divide-app-border">
          {data.items.map((item) => (
            <li key={item.id} className="py-3 first:pt-0">
              <div className="flex flex-wrap items-center gap-2">
                <InsightSeverityBadge severity={item.severity} />
                <span className="text-xs text-gray-500">{formatInsightCategory(item.category)}</span>
              </div>
              <p className="mt-1 font-medium text-gray-900">{item.title}</p>
              <p className="mt-1 text-sm text-gray-600">{item.description}</p>
              {item.recommended_action ? (
                <p className="mt-1 text-sm text-gray-700">
                  <span className="font-medium">Action:</span> {item.recommended_action}
                </p>
              ) : null}
              {item.url ? (
                <Link to={item.url} className="mt-2 inline-block text-sm text-core-blue hover:underline">
                  View details
                </Link>
              ) : null}
            </li>
          ))}
        </ul>
      ) : null}
    </DashboardSection>
  )
}
