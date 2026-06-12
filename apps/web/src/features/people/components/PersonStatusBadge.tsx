import { Badge } from '@/components/ui/Badge'

interface PersonStatusBadgeProps {
  isActive: boolean
}

export function PersonStatusBadge({ isActive }: PersonStatusBadgeProps) {
  return (
    <Badge variant={isActive ? 'success' : 'neutral'}>
      {isActive ? 'Active' : 'Inactive'}
    </Badge>
  )
}
