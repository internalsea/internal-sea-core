import type { SearchResultType } from '@/features/search/types'
import { formatLabel } from '@/lib/utils'

export function formatSearchResultType(type: SearchResultType): string {
  const labels: Record<SearchResultType, string> = {
    data_product: 'Data Product',
    work_item: 'Work Item',
    project: 'Project',
    internal_project: 'Internal Project',
    person: 'Person',
    team: 'Team',
    capability: 'Capability',
    file: 'File',
    policy: 'Policy',
    compliance_check: 'Compliance Check',
    automation_trigger: 'Automation Trigger',
  }
  return labels[type]
}

export function formatSearchStatus(status: string | null): string | null {
  if (!status) {
    return null
  }
  return formatLabel(status)
}

export function formatSearchDate(value: string | null): string | null {
  if (!value) {
    return null
  }
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return null
  }
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function buildResultMeta(result: {
  description: string | null
  status: string | null
  secondary_status: string | null
}): string {
  const parts: string[] = []
  if (result.description) {
    parts.push(result.description)
  }
  if (result.status) {
    parts.push(formatLabel(result.status))
  }
  if (result.secondary_status) {
    parts.push(formatLabel(result.secondary_status))
  }
  return parts.join(' · ')
}
