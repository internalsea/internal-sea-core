import type { ReactNode } from 'react'

import { cn } from '@/lib/utils'

interface CardProps {
  title?: string
  children: ReactNode
  className?: string
  padding?: 'md' | 'lg'
}

export function Card({ title, children, className, padding = 'md' }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-card border border-app-border bg-app-surface',
        padding === 'lg' ? 'p-6' : 'p-5',
        className,
      )}
    >
      {title ? (
        <h3 className="mb-3 text-base font-semibold text-gray-900">{title}</h3>
      ) : null}
      {children}
    </div>
  )
}
