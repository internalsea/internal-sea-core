import { ModulePlaceholder } from '@/components/common/ModulePlaceholder'

export function CapabilityReportsPage() {
  return (
    <ModulePlaceholder
      title="Capability Reports"
      description="Track capability coverage, skills, capacity, and performance across the organization."
    >
      <p className="text-sm text-gray-600">
        This report is not configured yet. Capability coverage, skills, and capacity insights will
        appear here once reporting is enabled for your workspace.
      </p>
    </ModulePlaceholder>
  )
}
