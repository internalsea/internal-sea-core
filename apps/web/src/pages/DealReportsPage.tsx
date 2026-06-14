import { ModulePlaceholder } from '@/components/common/ModulePlaceholder'

export function DealReportsPage() {
  return (
    <ModulePlaceholder
      title="Deal Reports"
      description="Review deal pipeline, ownership, status, value, and conversion insights."
    >
      <p className="text-sm text-gray-600">
        This report is not configured yet. Pipeline, value, and conversion insights will appear here
        once deal reporting is available.
      </p>
    </ModulePlaceholder>
  )
}
