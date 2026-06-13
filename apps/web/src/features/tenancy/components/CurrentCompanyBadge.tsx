import type { Company } from '@/features/tenancy/types'

interface CurrentCompanyBadgeProps {
  company: Company | null
  isLoading?: boolean
}

export function CurrentCompanyBadge({ company, isLoading = false }: CurrentCompanyBadgeProps) {
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
    <span className="hidden rounded-md border border-app-border bg-app-muted/40 px-3 py-1.5 text-sm font-medium text-gray-900 sm:inline">
      {company.name}
    </span>
  )
}
