import { ModulePlaceholder } from '@/components/common/ModulePlaceholder'

export function ProjectReportsPage() {
  return (
    <ModulePlaceholder
      title="Project Reports"
      description="Monitor project delivery, ownership, progress, risks, and business outcomes."
    >
      <p className="text-sm text-gray-600">
        This report is not configured yet. Delivery, ownership, and outcome metrics will appear
        here once project reporting is available.
      </p>
    </ModulePlaceholder>
  )
}
