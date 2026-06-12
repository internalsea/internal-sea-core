import type { BadgeVariant } from '@/lib/designTokens'
import { Badge } from '@/components/ui/Badge'
import type { SearchResultType } from '@/features/search/types'
import { formatSearchResultType } from '@/features/search/utils'

const typeVariants: Record<SearchResultType, BadgeVariant> = {
  data_product: 'info',
  work_item: 'teal',
  project: 'warning',
  internal_project: 'teal',
  person: 'neutral',
  team: 'neutral',
  capability: 'info',
  file: 'neutral',
  policy: 'warning',
  compliance_check: 'danger',
  automation_trigger: 'teal',
}

interface SearchResultTypeBadgeProps {
  type: SearchResultType
}

export function SearchResultTypeBadge({ type }: SearchResultTypeBadgeProps) {
  return <Badge variant={typeVariants[type]}>{formatSearchResultType(type)}</Badge>
}
