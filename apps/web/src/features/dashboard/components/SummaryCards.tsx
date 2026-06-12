import { LoadingState } from '@/components/common/LoadingState'
import { MetricCard } from '@/features/dashboard/components/MetricCard'
import type { DashboardSummary } from '@/features/dashboard/types'
import { formatCount } from '@/features/dashboard/utils'

interface SummaryCardsProps {
  summary?: DashboardSummary
  isLoading?: boolean
  error?: string | null
}

export function SummaryCards({ summary, isLoading = false, error }: SummaryCardsProps) {
  if (isLoading) {
    return <LoadingState message="Loading dashboard summary…" />
  }

  if (error) {
    return null
  }

  if (!summary) {
    return null
  }

  const overdueVariant =
    summary.work_items_overdue > 5 ? 'danger' : summary.work_items_overdue > 0 ? 'warning' : 'neutral'
  const qualityVariant =
    summary.data_products_with_quality_critical > 0
      ? 'danger'
      : summary.data_products_with_quality_warning > 0
        ? 'warning'
        : 'info'

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <MetricCard
        title="Data Products"
        value={formatCount(summary.data_products_total)}
        variant={qualityVariant}
        href="/data-products"
      />
      <MetricCard
        title="Active Products"
        value={formatCount(summary.data_products_active)}
        variant="success"
        href="/data-products"
      />
      <MetricCard
        title="Open Work"
        value={formatCount(summary.work_items_open)}
        variant="info"
        href="/work-items"
      />
      <MetricCard
        title="Overdue Work"
        value={formatCount(summary.work_items_overdue)}
        variant={overdueVariant}
        href="/work-items"
      />
      <MetricCard
        title="Active Projects"
        value={formatCount(summary.projects_active)}
        variant="info"
        href="/projects"
      />
      <MetricCard
        title="Internal Projects"
        value={formatCount(summary.internal_projects_active)}
        variant="neutral"
        href="/internal-projects"
      />
      <MetricCard
        title="Active People"
        value={formatCount(summary.people_active)}
        variant="neutral"
        href="/people"
      />
      <MetricCard
        title="Capabilities"
        value={formatCount(summary.capabilities_total)}
        variant="neutral"
        href="/capabilities"
      />
      <MetricCard
        title="Active Automations"
        value={formatCount(summary.automation_triggers_active)}
        variant="success"
        href="/automation"
      />
      <MetricCard
        title="Failed Automation Runs"
        value={formatCount(summary.automation_runs_failed)}
        variant={summary.automation_runs_failed > 0 ? 'danger' : 'neutral'}
        href="/automation"
      />
      <MetricCard
        title="Upcoming Runs"
        value={formatCount(summary.automation_next_runs)}
        variant="info"
        href="/automation"
      />
      <MetricCard
        title="Performance Metrics"
        value={formatCount(summary.performance_metrics_total)}
        variant="info"
        href="/performance"
      />
      <MetricCard
        title="Notifications"
        value={formatCount(summary.notification_messages_total)}
        variant="info"
        href="/notifications"
      />
      <MetricCard
        title="Failed Notifications"
        value={formatCount(summary.notification_messages_failed)}
        variant={summary.notification_messages_failed > 0 ? 'danger' : 'neutral'}
        href="/notifications"
      />
    </div>
  )
}
