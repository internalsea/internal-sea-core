import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import type { DueWorkSummary } from '@/features/worker/types'

interface DueWorkCardProps {
  summary: DueWorkSummary | undefined
  isLoading: boolean
}

export function DueWorkCard({ summary, isLoading }: DueWorkCardProps) {
  return (
    <Card>
      <SectionHeader
        title="Due work queue"
        description="Items eligible for the next worker cycle."
      />
      {isLoading ? (
        <p className="mt-3 text-sm text-gray-500">Loading due work…</p>
      ) : (
        <dl className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <Item label="Due triggers" value={summary?.due_automation_triggers ?? 0} />
          <Item label="Queued notifications" value={summary?.due_notifications ?? 0} />
          <Item label="Locked triggers" value={summary?.locked_automation_triggers ?? 0} />
          <Item label="Locked notifications" value={summary?.locked_notifications ?? 0} />
        </dl>
      )}
    </Card>
  )
}

function Item({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-2xl font-semibold text-gray-900">{value}</dd>
    </div>
  )
}
