import { Badge } from '@/components/ui/Badge'
import { POLICY_STATUSES } from '@/features/compliance/constants'
import type { PolicyStatus } from '@/features/compliance/types'
import type { BadgeVariant } from '@/lib/designTokens'

const labels = Object.fromEntries(POLICY_STATUSES.map((item) => [item.value, item.label]))

const variants: Record<PolicyStatus, BadgeVariant> = {
  draft: 'neutral',
  active: 'success',
  deprecated: 'warning',
  archived: 'neutral',
}

interface PolicyStatusBadgeProps {
  status: PolicyStatus
}

export function PolicyStatusBadge({ status }: PolicyStatusBadgeProps) {
  return <Badge variant={variants[status]}>{labels[status]}</Badge>
}
