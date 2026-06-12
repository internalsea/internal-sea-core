import { Badge } from '@/components/ui/Badge'
import { seniorityVariantMap } from '@/lib/designTokens'
import { seniorityLevelLabels } from '@/features/people/constants'
import type { SeniorityLevel } from '@/features/people/types'

interface SeniorityBadgeProps {
  seniority: SeniorityLevel | null | undefined
}

export function SeniorityBadge({ seniority }: SeniorityBadgeProps) {
  if (!seniority) {
    return <span className="text-sm text-gray-500">—</span>
  }

  return (
    <Badge variant={seniorityVariantMap[seniority] ?? 'neutral'}>
      {seniorityLevelLabels[seniority]}
    </Badge>
  )
}
