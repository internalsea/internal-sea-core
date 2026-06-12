import { Badge } from '@/components/ui/Badge'
import { projectHealthVariantMap } from '@/lib/designTokens'
import { projectHealthStatusLabels } from '@/features/projects/constants'

interface ProjectHealthBadgeProps {
  healthStatus: string | null | undefined
}

export function ProjectHealthBadge({ healthStatus }: ProjectHealthBadgeProps) {
  const status = healthStatus?.trim() || 'unknown'
  const label = projectHealthStatusLabels[status] ?? status

  return (
    <Badge variant={projectHealthVariantMap[status] ?? 'neutral'}>
      {label}
    </Badge>
  )
}
