import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import type { WorkerStatus } from '@/features/worker/types'
import { formatDateTime } from '@/features/automation/utils'

interface WorkerStatusCardProps {
  status: WorkerStatus | undefined
  isLoading: boolean
  error: Error | null
}

export function WorkerStatusCard({ status, isLoading, error }: WorkerStatusCardProps) {
  if (isLoading) {
    return (
      <Card>
        <SectionHeader title="Worker status" description="Background execution health." />
        <p className="mt-3 text-sm text-gray-500">Loading worker status…</p>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <SectionHeader title="Worker status" description="Background execution health." />
        <p className="mt-3 text-sm text-red-600">Unable to load worker status.</p>
      </Card>
    )
  }

  if (!status) {
    return null
  }

  return (
    <Card>
      <SectionHeader
        title="Worker status"
        description="Optional background process for scheduled automation and queued notifications."
      />
      <dl className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <Item label="Enabled" value={status.worker_enabled ? 'Yes' : 'No (optional locally)'} />
        <Item label="Instance" value={status.worker_instance_id} />
        <Item label="Poll interval" value={`${status.poll_interval_seconds}s`} />
        <Item label="Batch size" value={String(status.batch_size)} />
        <Item label="Due automation triggers" value={String(status.automation_due_count)} />
        <Item label="Due notifications" value={String(status.notification_due_count)} />
        <Item label="Last checked" value={formatDateTime(status.last_checked_at)} />
      </dl>
    </Card>
  )
}

function Item({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-900">{value}</dd>
    </div>
  )
}
