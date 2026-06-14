import { cn } from '@/lib/utils'

interface BrandLogoMarkProps {
  className?: string
}

export function BrandLogoMark({ className }: BrandLogoMarkProps) {
  return (
    <div
      className={cn(
        'inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-core-navy shadow-sm',
        'bg-gradient-to-br from-core-navy to-[#1e3a5f]',
        className,
      )}
      aria-hidden="true"
    >
      <span className="text-xs font-bold tracking-tight text-white">IS</span>
    </div>
  )
}
