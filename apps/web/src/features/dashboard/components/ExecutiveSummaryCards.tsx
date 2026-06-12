import { MetricCard } from '@/features/dashboard/components/MetricCard'
import { HealthScoreBadge } from '@/features/dashboard/components/HealthScoreBadge'
import { formatCount, formatScore } from '@/features/dashboard/utils'
import type { ExecutiveSummary } from '@/features/dashboard/types'

interface ExecutiveSummaryCardsProps {
  summary: ExecutiveSummary | undefined
  isLoading: boolean
}

export function ExecutiveSummaryCards({ summary, isLoading }: ExecutiveSummaryCardsProps) {
  if (isLoading) {
    return <p className="text-sm text-gray-500">Loading executive summary…</p>
  }
  if (!summary) {
    return null
  }

  const scoreVariant =
    summary.overall_status === 'good'
      ? 'success'
      : summary.overall_status === 'warning'
        ? 'warning'
        : summary.overall_status === 'critical'
          ? 'danger'
          : 'neutral'

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <h2 className="text-lg font-semibold text-gray-900">Executive overview</h2>
        <HealthScoreBadge status={summary.overall_status} />
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Overall score"
          value={formatScore(summary.overall_score)}
          variant={scoreVariant}
        />
        <MetricCard
          title="Active projects"
          value={formatCount(summary.active_projects + summary.active_internal_projects)}
          href="/projects"
        />
        <MetricCard
          title="Active data products"
          value={formatCount(summary.active_data_products)}
          href="/data-products"
        />
        <MetricCard title="Open work" value={formatCount(summary.open_work_items)} href="/work-items" />
        <MetricCard
          title="Overdue work"
          value={formatCount(summary.overdue_work_items)}
          variant={summary.overdue_work_items > 0 ? 'warning' : 'neutral'}
          href="/work-items"
        />
        <MetricCard
          title="Open compliance"
          value={formatCount(summary.compliance_open_checks)}
          href="/compliance"
        />
        <MetricCard
          title="Ownership gaps"
          value={formatCount(summary.ownership_gaps)}
          variant={summary.ownership_gaps > 0 ? 'warning' : 'neutral'}
        />
        <MetricCard
          title="Automation due"
          value={formatCount(summary.automation_due_triggers)}
          variant={summary.automation_due_triggers > 0 ? 'warning' : 'neutral'}
          href="/automation"
        />
      </div>
    </div>
  )
}
