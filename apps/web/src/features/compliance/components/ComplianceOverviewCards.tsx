import { MetricCard } from '@/features/dashboard/components/MetricCard'
import { useComplianceOverview } from '@/features/compliance/hooks'
import { formatCount } from '@/features/dashboard/utils'
import { getApiErrorMessage } from '@/features/compliance/utils'

export function ComplianceOverviewCards() {
  const { data, isLoading, isError, error } = useComplianceOverview()

  if (isLoading) {
    return <p className="text-sm text-gray-500">Loading compliance overview…</p>
  }

  if (isError) {
    return <p className="text-sm text-status-danger">{getApiErrorMessage(error)}</p>
  }

  if (!data) return null

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <MetricCard title="Policies" value={formatCount(data.policies_active)} description={`${data.policies_total} total`} variant="info" href="/compliance" />
      <MetricCard title="Active Rules" value={formatCount(data.active_rules)} description={`${data.rules_total} total`} variant="neutral" href="/compliance" />
      <MetricCard title="Open Checks" value={formatCount(data.checks_open)} description={`${data.checks_total} total`} variant="info" href="/compliance" />
      <MetricCard title="Non-Compliant" value={formatCount(data.checks_non_compliant)} variant={data.checks_non_compliant > 0 ? 'warning' : 'success'} href="/compliance" />
      <MetricCard title="Overdue Checks" value={formatCount(data.checks_overdue)} variant={data.checks_overdue > 0 ? 'danger' : 'neutral'} href="/compliance" />
      <MetricCard title="Compliant Checks" value={formatCount(data.checks_compliant)} variant="success" href="/compliance" />
      <MetricCard title="Active Controls" value={formatCount(data.active_controls)} description={`${data.controls_total} total`} variant="neutral" href="/compliance" />
      <MetricCard title="Missing Evidence" value={formatCount(data.evidence_missing)} variant={data.evidence_missing > 0 ? 'warning' : 'neutral'} href="/compliance" />
    </div>
  )
}
