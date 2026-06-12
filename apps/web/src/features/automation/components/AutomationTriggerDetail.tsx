import { useState, type ReactNode } from 'react'
import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { EntityReference } from '@/features/entity-picker/components/EntityReference'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { AutomationActionTypeBadge } from '@/features/automation/components/AutomationActionTypeBadge'
import { AutomationRunsTable } from '@/features/automation/components/AutomationRunsTable'
import { AutomationStatusBadge } from '@/features/automation/components/AutomationStatusBadge'
import { RunTriggerDialog } from '@/features/automation/components/RunTriggerDialog'
import { useAutomationSchedule, useRunAutomationTrigger, useTriggerRuns } from '@/features/automation/hooks'
import type { AutomationTrigger } from '@/features/automation/types'
import {
  formatDateTime,
  formatTriggerType,
  getApiErrorMessage,
  isActionImplementedInMvp,
  stringifyJsonField,
} from '@/features/automation/utils'

interface AutomationTriggerDetailProps {
  trigger: AutomationTrigger
}

export function AutomationTriggerDetail({ trigger }: AutomationTriggerDetailProps) {
  const [dialogMode, setDialogMode] = useState<'simulate' | 'real' | null>(null)
  const [runMessage, setRunMessage] = useState<string | null>(null)
  const { data: schedule } = useAutomationSchedule(trigger.schedule_id ?? undefined)
  const { data: runsData, isLoading: runsLoading } = useTriggerRuns(trigger.id)
  const runMutation = useRunAutomationTrigger(trigger.id)

  const handleRun = async (simulate: boolean) => {
    try {
      const result = await runMutation.mutateAsync({ simulate })
      setRunMessage(result.message)
      setDialogMode(null)
    } catch (error) {
      setRunMessage(getApiErrorMessage(error))
      setDialogMode(null)
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <SectionHeader title={trigger.name} description={trigger.description ?? undefined} />
          <div className="flex flex-wrap gap-2">
            <PermissionGate require="editor">
              <Link to={`/automation/triggers/${trigger.id}/edit`}>
                <Button variant="secondary" size="sm">Edit</Button>
              </Link>
              <Button variant="secondary" size="sm" onClick={() => setDialogMode('simulate')}>
                Run Simulation
              </Button>
              <Button
                size="sm"
                onClick={() => setDialogMode('real')}
                disabled={!isActionImplementedInMvp(trigger.action_type)}
              >
                Run Real Action
              </Button>
            </PermissionGate>
          </div>
        </div>

        <dl className="mt-4 grid gap-4 sm:grid-cols-2">
          <DetailItem label="Status">
            <AutomationStatusBadge status={trigger.status} />
          </DetailItem>
          <DetailItem label="Trigger type">{formatTriggerType(trigger.trigger_type)}</DetailItem>
          <DetailItem label="Action type">
            <AutomationActionTypeBadge actionType={trigger.action_type} />
          </DetailItem>
          <DetailItem label="Schedule">
            {schedule ? (
              <Link
                to={`/automation/schedules/${schedule.id}/edit`}
                className="text-core-blue hover:underline"
              >
                {schedule.name}
              </Link>
            ) : (
              '—'
            )}
          </DetailItem>
          <DetailItem label="Target">
            {trigger.target_type && trigger.target_id ? (
              <EntityReference
                entityType={trigger.target_type}
                entityId={trigger.target_id}
                showType
                link
              />
            ) : (
              '—'
            )}
          </DetailItem>
          <DetailItem label="Last run">{formatDateTime(trigger.last_run_at)}</DetailItem>
          <DetailItem label="Next run">{formatDateTime(trigger.next_run_at)}</DetailItem>
        </dl>
      </Card>

      <Card title="Conditions">
        <pre className="overflow-x-auto rounded-md bg-app-muted/40 p-3 text-xs text-gray-800">
          {stringifyJsonField(trigger.conditions) || '{}'}
        </pre>
      </Card>

      <Card title="Action config">
        <pre className="overflow-x-auto rounded-md bg-app-muted/40 p-3 text-xs text-gray-800">
          {stringifyJsonField(trigger.action_config) || '{}'}
        </pre>
      </Card>

      {trigger.locked_by || trigger.lock_expires_at ? (
        <Card title="Worker lock (technical)">
          <dl className="grid gap-3 sm:grid-cols-2">
            <DetailItem label="Locked by">{trigger.locked_by ?? '—'}</DetailItem>
            <DetailItem label="Lock expires">{formatDateTime(trigger.lock_expires_at)}</DetailItem>
          </dl>
        </Card>
      ) : null}

      <Card>
        <SectionHeader title="Run history" description="Manual and simulated runs for this trigger." />
        {runMessage ? <p className="mt-3 text-sm text-gray-700">{runMessage}</p> : null}
        <div className="mt-4">
          {runsLoading ? (
            <p className="text-sm text-gray-500">Loading runs…</p>
          ) : (
            <AutomationRunsTable items={runsData?.items ?? []} showTriggerLink={false} />
          )}
        </div>
      </Card>

      <RunTriggerDialog
        open={dialogMode !== null}
        simulate={dialogMode === 'simulate'}
        isRunning={runMutation.isPending}
        onConfirm={() => void handleRun(dialogMode === 'simulate')}
        onCancel={() => setDialogMode(null)}
      />
    </div>
  )
}

function DetailItem({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-900">{children}</dd>
    </div>
  )
}
