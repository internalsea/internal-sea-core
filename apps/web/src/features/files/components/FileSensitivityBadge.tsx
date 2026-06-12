import { Badge } from '@/components/ui/Badge'
import { fileSensitivityLabels } from '@/features/files/constants'
import type { FileSensitivity } from '@/features/files/types'
import { getSensitivityVariant } from '@/features/files/utils'

interface FileSensitivityBadgeProps {
  sensitivity: FileSensitivity
}

export function FileSensitivityBadge({ sensitivity }: FileSensitivityBadgeProps) {
  return (
    <Badge variant={getSensitivityVariant(sensitivity)}>
      {fileSensitivityLabels[sensitivity]}
    </Badge>
  )
}
