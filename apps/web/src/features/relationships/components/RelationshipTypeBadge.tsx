import { Badge } from '@/components/ui/Badge'
import type { BadgeVariant } from '@/lib/designTokens'
import { entityLinkTypeLabels } from '@/features/relationships/constants'
import type { EntityLinkType } from '@/features/relationships/types'

const linkTypeVariants: Record<EntityLinkType, BadgeVariant> = {
  relates_to: 'neutral',
  depends_on: 'warning',
  blocks: 'danger',
  duplicates: 'neutral',
  replaces: 'warning',
  owns: 'info',
  supports: 'teal',
  improves: 'success',
  affects: 'warning',
  created_from: 'neutral',
  evidence_for: 'info',
  decision_for: 'info',
  risk_for: 'warning',
}

interface RelationshipTypeBadgeProps {
  linkType: EntityLinkType
}

export function RelationshipTypeBadge({ linkType }: RelationshipTypeBadgeProps) {
  return (
    <Badge variant={linkTypeVariants[linkType]}>
      {entityLinkTypeLabels[linkType] ?? linkType}
    </Badge>
  )
}
