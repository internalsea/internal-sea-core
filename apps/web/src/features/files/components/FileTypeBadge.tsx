import { Badge } from '@/components/ui/Badge'
import { fileTypeLabels } from '@/features/files/constants'
import type { FileAssetType } from '@/features/files/types'
import { getFileTypeVariant } from '@/features/files/utils'

interface FileTypeBadgeProps {
  fileType: FileAssetType
}

export function FileTypeBadge({ fileType }: FileTypeBadgeProps) {
  return (
    <Badge variant={getFileTypeVariant(fileType)}>{fileTypeLabels[fileType]}</Badge>
  )
}
