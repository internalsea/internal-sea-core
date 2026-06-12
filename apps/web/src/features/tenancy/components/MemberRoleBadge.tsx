import { Badge } from '@/components/ui/Badge'
import type { BadgeVariant } from '@/lib/designTokens'
import { formatMemberRole } from '@/features/tenancy/utils'

interface MemberRoleBadgeProps {
  role: string
}

function roleVariant(role: string): BadgeVariant {
  switch (role) {
    case 'owner':
      return 'teal'
    case 'admin':
      return 'info'
    case 'editor':
      return 'success'
    case 'viewer':
    default:
      return 'neutral'
  }
}

export function MemberRoleBadge({ role }: MemberRoleBadgeProps) {
  return <Badge variant={roleVariant(role)}>{formatMemberRole(role)}</Badge>
}
