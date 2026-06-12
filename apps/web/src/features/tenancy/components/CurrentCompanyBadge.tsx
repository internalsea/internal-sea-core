import type { Company, Workspace } from '@/features/tenancy/types'

interface CurrentCompanyBadgeProps {
  company: Company | null
  workspace: Workspace | null
  isLoading?: boolean
}

export function CurrentCompanyBadge({ company, workspace, isLoading = false }: CurrentCompanyBadgeProps) {
  if (isLoading) {
    return (
      <span className="hidden text-sm text-gray-500 sm:inline">
        Loading tenant…
      </span>
    )
  }

  if (!company) {
    return null
  }

  return (
    <div className="hidden items-center gap-2 rounded-md border border-app-border bg-app-muted/40 px-3 py-1.5 text-sm sm:flex">
      <span className="font-medium text-gray-900">{company.name}</span>
      {workspace ? (
        <>
          <span className="text-gray-400">/</span>
          <span className="text-gray-600">{workspace.name}</span>
        </>
      ) : null}
    </div>
  )
}
