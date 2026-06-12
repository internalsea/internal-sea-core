import { Badge } from '@/components/ui/Badge'
import { fileStatusLabels } from '@/features/files/constants'
import type { FileStatus } from '@/features/files/types'
import { getFileStatusVariant } from '@/features/files/utils'

interface FileStatusBadgeProps {
  status: FileStatus
}

export function FileStatusBadge({ status }: FileStatusBadgeProps) {
  return (
    <Badge variant={getFileStatusVariant(status)}>{fileStatusLabels[status]}</Badge>
  )
}
