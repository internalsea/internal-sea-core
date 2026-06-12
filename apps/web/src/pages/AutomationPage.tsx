import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { AutomationOverviewCards } from '@/features/automation/components/AutomationOverviewCards'
import { AutomationRunsTable } from '@/features/automation/components/AutomationRunsTable'
import { AutomationSchedulesTable } from '@/features/automation/components/AutomationSchedulesTable'
import { AutomationTriggersTable } from '@/features/automation/components/AutomationTriggersTable'
import { DEFAULT_PAGE_SIZE } from '@/features/automation/constants'
import {
  useAutomationOverview,
  useAutomationRuns,
  useAutomationSchedules,
  useAutomationTriggers,
} from '@/features/automation/hooks'
import { DueWorkCard } from '@/features/worker/components/DueWorkCard'
import { RunWorkerOnceButton } from '@/features/worker/components/RunWorkerOnceButton'
import { WorkerStatusCard } from '@/features/worker/components/WorkerStatusCard'
import { useDueWorkSummary, useWorkerStatus } from '@/features/worker/hooks'

export function AutomationPage() {
  const { data: overview, isLoading: overviewLoading, error: overviewError } = useAutomationOverview()
  const { data: triggers } = useAutomationTriggers({ page: 1, page_size: DEFAULT_PAGE_SIZE })
  const { data: schedules } = useAutomationSchedules({ page: 1, page_size: DEFAULT_PAGE_SIZE })
  const { data: runs } = useAutomationRuns({ page: 1, page_size: 10 })
  const workerStatus = useWorkerStatus()
  const dueWork = useDueWorkSummary()

  return (
    <div className="space-y-8">
      <PageHeader
        title="Automation"
        description="Manage schedules, triggers and safe automation runs for reviews, reminders and task generation."
        actions={
          <PermissionGate require="editor">
            <div className="flex gap-2">
              <Link to="/automation/triggers/new">
                <Button>New Trigger</Button>
              </Link>
              <Link to="/automation/schedules/new">
                <Button variant="secondary">New Schedule</Button>
              </Link>
            </div>
          </PermissionGate>
        }
      />

      <AutomationOverviewCards
        overview={overview}
        isLoading={overviewLoading}
        error={overviewError}
      />

      <div className="grid gap-6 lg:grid-cols-2">
        <WorkerStatusCard
          status={workerStatus.data}
          isLoading={workerStatus.isLoading}
          error={workerStatus.error}
        />
        <DueWorkCard summary={dueWork.data} isLoading={dueWork.isLoading} />
      </div>

      <PermissionGate require="editor">
        <Card>
          <SectionHeader
            title="Manual worker cycle"
            description="Process one batch of due automation triggers and queued notifications."
          />
          <div className="mt-4">
            <RunWorkerOnceButton />
          </div>
        </Card>
      </PermissionGate>

      <Card>
        <SectionHeader title="Triggers" description="Automation rules linked to schedules and targets." />
        <div className="mt-4">
          <AutomationTriggersTable items={triggers?.items ?? []} />
        </div>
      </Card>

      <Card>
        <SectionHeader title="Schedules" description="Recurrence definitions for scheduled triggers." />
        <div className="mt-4">
          <AutomationSchedulesTable items={schedules?.items ?? []} />
        </div>
      </Card>

      <Card>
        <SectionHeader title="Recent runs" description="Latest manual and simulated automation runs." />
        <div className="mt-4">
          <AutomationRunsTable items={runs?.items ?? []} />
        </div>
      </Card>

      <Card>
        <SectionHeader
          title="Future capabilities"
          description="Planned automation features not yet available in MVP."
        />
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-gray-600">
          <li>Email and Teams/Slack notifications</li>
          <li>AI tool actions</li>
          <li>Outbound webhooks</li>
        </ul>
      </Card>
    </div>
  )
}
