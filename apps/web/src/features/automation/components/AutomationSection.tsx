import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { AutomationActionTypeBadge } from '@/features/automation/components/AutomationActionTypeBadge'
import { AutomationStatusBadge } from '@/features/automation/components/AutomationStatusBadge'
import { useEntityAutomations } from '@/features/automation/hooks'
import type { AutomationTargetType } from '@/features/automation/types'
import { formatDateTime, formatTriggerType, getApiErrorMessage } from '@/features/automation/utils'

interface AutomationSectionProps {
  targetType: AutomationTargetType
  targetId: string
  title?: string
}

export function AutomationSection({
  targetType,
  targetId,
  title = 'Automation',
}: AutomationSectionProps) {
  const navigate = useNavigate()
  const { data, isLoading, isError, error } = useEntityAutomations(targetType, targetId)

  const newTriggerUrl = `/automation/triggers/new?target_type=${targetType}&target_id=${targetId}`

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title={title}
          description="Schedules and triggers linked to this record."
        />
        <PermissionGate require="editor">
          <Link to={newTriggerUrl}>
            <Button variant="secondary" size="sm">New automation for this object</Button>
          </Link>
        </PermissionGate>
      </div>

      {isLoading ? (
        <p className="mt-4 text-sm text-gray-500">Loading automations…</p>
      ) : isError ? (
        <p className="mt-4 text-sm text-status-danger">{getApiErrorMessage(error)}</p>
      ) : (data?.triggers.length ?? 0) === 0 ? (
        <p className="mt-4 text-sm text-gray-500">No automation triggers linked to this record.</p>
      ) : (
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full divide-y divide-app-border text-sm">
            <thead>
              <tr className="text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                <th className="px-3 py-2">Name</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Type</th>
                <th className="px-3 py-2">Action</th>
                <th className="px-3 py-2">Last Run</th>
                <th className="px-3 py-2">Next Run</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-app-border">
              {data?.triggers.map((trigger) => (
                <tr
                  key={trigger.id}
                  className="cursor-pointer text-gray-900 hover:bg-app-muted/30"
                  onClick={() => navigate(`/automation/triggers/${trigger.id}`)}
                >
                  <td className="px-3 py-2 font-medium text-core-blue">{trigger.name}</td>
                  <td className="px-3 py-2">
                    <AutomationStatusBadge status={trigger.status} />
                  </td>
                  <td className="px-3 py-2">{formatTriggerType(trigger.trigger_type)}</td>
                  <td className="px-3 py-2">
                    <AutomationActionTypeBadge actionType={trigger.action_type} />
                  </td>
                  <td className="px-3 py-2">{formatDateTime(trigger.last_run_at)}</td>
                  <td className="px-3 py-2">{formatDateTime(trigger.next_run_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  )
}
