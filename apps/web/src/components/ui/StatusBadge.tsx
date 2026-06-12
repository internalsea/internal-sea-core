import { badgeVariantClasses, resolveStatusVariant } from '@/lib/designTokens'
import { cn, formatLabel } from '@/lib/utils'

interface StatusBadgeProps {
  status: string
  className?: string
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const variant = resolveStatusVariant(status)

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium',
        badgeVariantClasses[variant],
        className,
      )}
    >
      {formatLabel(status)}
    </span>
  )
}
