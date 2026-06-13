import { ModulePlaceholder } from '@/components/common/ModulePlaceholder'

export function ComplianceFrameworksPage() {
  return (
    <ModulePlaceholder
      title="Compliance Frameworks"
      description="Frameworks, standards and control mappings for organizational compliance programs."
    >
      <p className="text-sm text-slate-600">
        Coming next — define frameworks such as SOC 2, ISO 27001 or internal standards and map
        controls to policies and checks.
      </p>
    </ModulePlaceholder>
  )
}
