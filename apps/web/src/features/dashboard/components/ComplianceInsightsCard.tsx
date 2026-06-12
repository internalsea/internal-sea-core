import { Link } from 'react-router-dom'

import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { formatCount, formatDate } from '@/features/dashboard/utils'
import type { ComplianceInsights } from '@/features/dashboard/types'

interface ComplianceInsightsCardProps {
  data: ComplianceInsights | undefined
  isLoading: boolean
  error: string | null
}

export function ComplianceInsightsCard({ data, isLoading, error }: ComplianceInsightsCardProps) {
  return (
    <DashboardSection
      title="Compliance insights"
      description="Open checks, overdue items and evidence gaps."
      isLoading={isLoading}
      error={error}
      action={<Link to="/compliance" className="text-sm text-core-blue hover:underline">Compliance</Link>}
    >
      {data ? (
        <div className="space-y-4">
          <dl className="grid grid-cols-2 gap-3 text-sm">
            <div><dt className="text-gray-500">Open</dt><dd className="font-semibold">{formatCount(data.checks_open)}</dd></div>
            <div><dt className="text-gray-500">Overdue</dt><dd className="font-semibold">{formatCount(data.checks_overdue)}</dd></div>
            <div><dt className="text-gray-500">Non-compliant</dt><dd className="font-semibold">{formatCount(data.checks_non_compliant)}</dd></div>
            <div><dt className="text-gray-500">Missing evidence</dt><dd className="font-semibold">{formatCount(data.evidence_missing)}</dd></div>
          </dl>
          {data.top_overdue_checks.length > 0 ? (
            <div>
              <p className="mb-2 text-xs font-medium uppercase text-gray-500">Top overdue</p>
              <ul className="space-y-2 text-sm">
                {data.top_overdue_checks.map((check) => (
                  <li key={check.id}>
                    <Link
                      to={`/compliance/checks/${check.id}`}
                      className="font-medium text-core-blue hover:underline"
                    >
                      {check.title}
                    </Link>
                    <span className="text-gray-500"> · due {formatDate(check.due_date)}</span>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      ) : null}
    </DashboardSection>
  )
}
