import { Link } from 'react-router-dom'

import { DashboardSection } from '@/features/dashboard/components/DashboardSection'
import { MiniProgressBar } from '@/features/dashboard/components/MiniProgressBar'
import { formatCount, sortStatusEntries } from '@/features/dashboard/utils'
import type { WorkDeliverySummary } from '@/features/dashboard/types'

interface WorkDeliveryCardProps {
  data: WorkDeliverySummary | undefined
  isLoading: boolean
  error: string | null
}

export function WorkDeliveryCard({ data, isLoading, error }: WorkDeliveryCardProps) {
  return (
    <DashboardSection
      title="Work delivery"
      description="Open work, overdue items and distribution by status."
      isLoading={isLoading}
      error={error}
      action={
        <div className="flex gap-2 text-sm">
          <Link to="/work-items" className="text-core-blue hover:underline">Work items</Link>
          <Link to="/work-board" className="text-core-blue hover:underline">Board</Link>
        </div>
      }
    >
      {data ? (
        <div className="space-y-4">
          <dl className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-3">
            <div><dt className="text-gray-500">Open</dt><dd className="font-semibold">{formatCount(data.open_work_items)}</dd></div>
            <div><dt className="text-gray-500">Done</dt><dd className="font-semibold">{formatCount(data.done_work_items)}</dd></div>
            <div><dt className="text-gray-500">Overdue</dt><dd className="font-semibold">{formatCount(data.overdue_work_items)}</dd></div>
            <div><dt className="text-gray-500">Critical</dt><dd className="font-semibold">{formatCount(data.critical_items)}</dd></div>
            <div><dt className="text-gray-500">Risks</dt><dd className="font-semibold">{formatCount(data.risks)}</dd></div>
            <div><dt className="text-gray-500">Tech debt</dt><dd className="font-semibold">{formatCount(data.technical_debt)}</dd></div>
          </dl>
          <div>
            <p className="mb-2 text-xs font-medium uppercase text-gray-500">By status</p>
            {sortStatusEntries(data.by_status).map(([status, count]) => (
              <div key={status} className="mb-2">
                <MiniProgressBar value={count} max={data.total_work_items} label={status} />
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </DashboardSection>
  )
}
