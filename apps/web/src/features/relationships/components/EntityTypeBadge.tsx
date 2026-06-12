import { Badge } from '@/components/ui/Badge'
import type { BadgeVariant } from '@/lib/designTokens'
import { entityTypeLabels } from '@/features/relationships/constants'
import type { EntityType } from '@/features/relationships/types'

const entityTypeVariants: Record<EntityType, BadgeVariant> = {
  data_product: 'info',
  work_item: 'teal',
  project: 'warning',
  internal_project: 'teal',
  person: 'neutral',
  team: 'neutral',
  capability: 'info',
  policy: 'neutral',
  rule: 'neutral',
  compliance_check: 'warning',
  file: 'neutral',
  meeting: 'neutral',
  deal: 'neutral',
  tool: 'neutral',
}

interface EntityTypeBadgeProps {
  entityType: EntityType
}

export function EntityTypeBadge({ entityType }: EntityTypeBadgeProps) {
  return (
    <Badge variant={entityTypeVariants[entityType]}>
      {entityTypeLabels[entityType] ?? entityType}
    </Badge>
  )
}
