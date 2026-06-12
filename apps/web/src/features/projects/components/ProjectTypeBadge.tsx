import { Badge } from '@/components/ui/Badge'
import { projectTypeVariantMap } from '@/lib/designTokens'
import { projectTypeLabels } from '@/features/projects/constants'
import type { ProjectType } from '@/types/enums'

interface ProjectTypeBadgeProps {
  type: ProjectType
}

export function ProjectTypeBadge({ type }: ProjectTypeBadgeProps) {
  return (
    <Badge variant={projectTypeVariantMap[type] ?? 'neutral'}>
      {projectTypeLabels[type]}
    </Badge>
  )
}
