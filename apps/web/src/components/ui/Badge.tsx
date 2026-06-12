import type { BadgeVariant } from '@/lib/designTokens'
import { badgeVariantClasses } from '@/lib/designTokens'
import { cn } from '@/lib/utils'

interface BadgeProps {
  children: string
  variant?: BadgeVariant
  className?: string
}

export function Badge({ children, variant = 'neutral', className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium',
        badgeVariantClasses[variant],
        className,
      )}
    >
      {children}
    </span>
  )
}
