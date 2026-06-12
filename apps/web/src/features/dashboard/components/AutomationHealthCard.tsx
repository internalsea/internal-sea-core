import { Link } from 'react-router-dom'

import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { formatCount, formatDateTime } from '@/features/dashboard/utils'
import type { AutomationHealth } from '@/features/dashboard/types'

interface AutomationHealthCardProps {
  data: AutomationHealth | undefined
  isLoading: boolean
  error: string | null
}

export function AutomationHealthCard({ data, isLoading, error }: AutomationHealthCardProps) {
  return (
    <DashboardSection
      title="Automation health"
      description="Schedules, due triggers and failed runs."
      isLoading={isLoading}
      error={error}
      action={<Link to="/automation" className="text-sm text-core-blue hover:underline">Automation</Link>}
    >
      {data ? (
        <div className="space-y-4">
          <dl className="grid grid-cols-2 gap-3 text-sm">
            <div><dt className="text-gray-500">Due triggers</dt><dd className="font-semibold">{formatCount(data.due_triggers)}</dd></div>
            <div><dt className="text-gray-500">Failed runs</dt><dd className="font-semibold">{formatCount(data.runs_failed)}</dd></div>
            <div><dt className="text-gray-500">Active triggers</dt><dd className="font-semibold">{formatCount(data.triggers_active)}</dd></div>
            <div><dt className="text-gray-500">Locked</dt><dd className="font-semibold">{formatCount(data.locked_triggers)}</dd></div>
          </dl>
          {data.recent_failed_runs.length > 0 ? (
            <ul className="divide-y divide-app-border text-sm">
              {data.recent_failed_runs.map((run) => (
                <li key={run.id} className="py-2 first:pt-0">
                  <Link to={`/automation/triggers/${run.trigger_id}`} className="text-core-blue hover:underline">
                    {run.action_type ?? 'automation run'}
                  </Link>
                  <p className="text-gray-600">{run.error_message ?? 'Failed'} · {formatDateTime(run.created_at)}</p>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      ) : null}
    </DashboardSection>
  )
}
