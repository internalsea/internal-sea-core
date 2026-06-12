import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { HealthScoreBadge } from '@/features/dashboard/components/HealthScoreBadge'
import { MiniProgressBar } from '@/features/dashboard/components/MiniProgressBar'
import type { OperationalHealth } from '@/features/dashboard/types'

interface OperationalHealthPanelProps {
  data: OperationalHealth | undefined
  isLoading: boolean
  error: string | null
}

export function OperationalHealthPanel({ data, isLoading, error }: OperationalHealthPanelProps) {
  return (
    <DashboardSection
      title="Operational health"
      description="Transparent health scores across delivery, projects, compliance, performance and automation."
      isLoading={isLoading}
      error={error}
    >
      {data ? (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Overall</span>
            <HealthScoreBadge status={data.status} />
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <MiniProgressBar value={data.work_health_score} label="Work delivery" />
            <MiniProgressBar value={data.project_health_score} label="Projects" />
            <MiniProgressBar value={data.compliance_health_score} label="Compliance" />
            <MiniProgressBar value={data.performance_health_score} label="Performance" />
            <MiniProgressBar value={data.automation_health_score} label="Automation" />
          </div>
          <dl className="grid gap-2 text-sm sm:grid-cols-3">
            <div><dt className="text-gray-500">Critical work</dt><dd className="font-medium">{data.critical_work_items_count}</dd></div>
            <div><dt className="text-gray-500">Overdue items</dt><dd className="font-medium">{data.overdue_items_count}</dd></div>
            <div><dt className="text-gray-500">At-risk projects</dt><dd className="font-medium">{data.blocked_or_warning_projects}</dd></div>
          </dl>
        </div>
      ) : null}
    </DashboardSection>
  )
}
