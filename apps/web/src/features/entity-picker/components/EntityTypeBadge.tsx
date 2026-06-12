import { Badge } from '@/components/ui/Badge'
import { entityPickerBadgeVariants, entityPickerTypeLabels } from '@/features/entity-picker/constants'
import type { EntityPickerType } from '@/features/entity-picker/types'

interface EntityTypeBadgeProps {
  type: EntityPickerType
  className?: string
}

export function EntityTypeBadge({ type, className }: EntityTypeBadgeProps) {
  return (
    <Badge variant={entityPickerBadgeVariants[type]} className={className}>
      {entityPickerTypeLabels[type]}
    </Badge>
  )
}
