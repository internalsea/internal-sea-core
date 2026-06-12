import { Badge } from '@/components/ui/Badge'
import { projectStatusVariantMap } from '@/lib/designTokens'
import { projectStatusLabels } from '@/features/projects/constants'
import type { ProjectStatus } from '@/types/enums'

interface ProjectStatusBadgeProps {
  status: ProjectStatus
}

export function ProjectStatusBadge({ status }: ProjectStatusBadgeProps) {
  return (
    <Badge variant={projectStatusVariantMap[status] ?? 'neutral'}>
      {projectStatusLabels[status]}
    </Badge>
  )
}
