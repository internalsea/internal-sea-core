import { ModulePlaceholder } from '@/components/common/ModulePlaceholder'

export function ComplianceEvidencePage() {
  return (
    <ModulePlaceholder
      title="Compliance Evidence"
      description="Central registry of evidence linked to checks, controls, policies and audits."
    >
      <p className="text-sm text-slate-600">
        Coming next — browse, filter and manage evidence across compliance checks. Evidence is
        currently attached from individual check detail pages.
      </p>
    </ModulePlaceholder>
  )
}
