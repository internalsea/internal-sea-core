import { Link } from 'react-router-dom'

import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { MetricCard } from '@/features/dashboard/components/MetricCard'
import type { DashboardSummary } from '@/features/dashboard/types'
import { formatCount } from '@/features/dashboard/utils'

interface GovernancePlaceholderCardProps {
  summary?: DashboardSummary
}

export function GovernancePlaceholderCard({ summary }: GovernancePlaceholderCardProps) {
  const overdueVariant =
    (summary?.compliance_checks_overdue ?? 0) > 0 ? 'danger' : 'neutral'
  const nonCompliantVariant =
    (summary?.compliance_checks_non_compliant ?? 0) > 0 ? 'warning' : 'success'

  return (
    <DashboardSection
      title="Governance & Compliance"
      description="Policies, rules, controls, checks and evidence."
      action={
        <Link to="/compliance" className="text-sm text-core-blue hover:underline">
          Open compliance
        </Link>
      }
    >
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Compliance Checks"
          value={formatCount(summary?.compliance_checks_total ?? 0)}
          variant="info"
          href="/compliance"
        />
        <MetricCard
          title="Open Checks"
          value={formatCount(summary?.compliance_checks_open ?? 0)}
          variant="info"
          href="/compliance"
        />
        <MetricCard
          title="Non-Compliant"
          value={formatCount(summary?.compliance_checks_non_compliant ?? 0)}
          variant={nonCompliantVariant}
          href="/compliance"
        />
        <MetricCard
          title="Overdue Checks"
          value={formatCount(summary?.compliance_checks_overdue ?? 0)}
          variant={overdueVariant}
          href="/compliance"
        />
      </div>
      <p className="mt-4 text-xs text-gray-500">
        Automated rules, approvals, schedules and external audit export are planned for later phases.
      </p>
    </DashboardSection>
  )
}
