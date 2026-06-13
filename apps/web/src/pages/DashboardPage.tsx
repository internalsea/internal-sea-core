import { PageHeader } from '@/components/ui/PageHeader'
import { ActionableInsightsCard } from '@/features/dashboard/components/ActionableInsightsCard'
import { AutomationHealthCard } from '@/features/dashboard/components/AutomationHealthCard'
import { ComplianceInsightsCard } from '@/features/dashboard/components/ComplianceInsightsCard'
import { DataProductHealthCard } from '@/features/dashboard/components/DataProductHealthCard'
import { ExecutiveSummaryCards } from '@/features/dashboard/components/ExecutiveSummaryCards'
import { NotificationHealthCard } from '@/features/dashboard/components/NotificationHealthCard'
import { OperationalHealthPanel } from '@/features/dashboard/components/OperationalHealthPanel'
import { PerformanceInsightsCard } from '@/features/dashboard/components/PerformanceInsightsCard'
import { ProjectInsightsCard } from '@/features/dashboard/components/ProjectInsightsCard'
import { RecentActivityCard } from '@/features/dashboard/components/RecentActivityCard'
import { WorkDeliveryCard } from '@/features/dashboard/components/WorkDeliveryCard'
import {
  useActionableInsights,
  useAutomationHealth,
  useComplianceInsights,
  useDataProductHealth,
  useExecutiveSummary,
  useNotificationHealth,
  useOperationalHealth,
  usePerformanceInsights,
  useProjectInsights,
  useRecentActivity,
  useWorkDelivery,
} from '@/features/dashboard/hooks'

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }
  return 'Unable to load this section.'
}

export function DashboardPage() {
  const executive = useExecutiveSummary()
  const operational = useOperationalHealth()
  const insights = useActionableInsights()
  const workDelivery = useWorkDelivery()
  const projectInsights = useProjectInsights()
  const dataProductHealth = useDataProductHealth()
  const compliance = useComplianceInsights()
  const performance = usePerformanceInsights()
  const automation = useAutomationHealth()
  const notifications = useNotificationHealth()
  const activity = useRecentActivity()

  return (
    <div className="space-y-6">
      <PageHeader
        title="Today"
        description="Executive and operational overview of data products, work, projects, compliance, performance and automation."
      />

      <ExecutiveSummaryCards
        summary={executive.data}
        isLoading={executive.isLoading}
      />

      <OperationalHealthPanel
        data={operational.data}
        isLoading={operational.isLoading}
        error={operational.isError ? getErrorMessage(operational.error) : null}
      />

      <div className="grid gap-6 xl:grid-cols-2">
        <ActionableInsightsCard
          data={insights.data}
          isLoading={insights.isLoading}
          error={insights.isError ? getErrorMessage(insights.error) : null}
        />
        <WorkDeliveryCard
          data={workDelivery.data}
          isLoading={workDelivery.isLoading}
          error={workDelivery.isError ? getErrorMessage(workDelivery.error) : null}
        />
        <ProjectInsightsCard
          data={projectInsights.data}
          isLoading={projectInsights.isLoading}
          error={projectInsights.isError ? getErrorMessage(projectInsights.error) : null}
        />
        <DataProductHealthCard
          data={dataProductHealth.data}
          isLoading={dataProductHealth.isLoading}
          error={dataProductHealth.isError ? getErrorMessage(dataProductHealth.error) : null}
        />
        <ComplianceInsightsCard
          data={compliance.data}
          isLoading={compliance.isLoading}
          error={compliance.isError ? getErrorMessage(compliance.error) : null}
        />
        <PerformanceInsightsCard
          data={performance.data}
          isLoading={performance.isLoading}
          error={performance.isError ? getErrorMessage(performance.error) : null}
        />
        <AutomationHealthCard
          data={automation.data}
          isLoading={automation.isLoading}
          error={automation.isError ? getErrorMessage(automation.error) : null}
        />
        <NotificationHealthCard
          data={notifications.data}
          isLoading={notifications.isLoading}
          error={notifications.isError ? getErrorMessage(notifications.error) : null}
        />
        <RecentActivityCard
          data={activity.data}
          isLoading={activity.isLoading}
          error={activity.isError ? getErrorMessage(activity.error) : null}
        />
      </div>
    </div>
  )
}
