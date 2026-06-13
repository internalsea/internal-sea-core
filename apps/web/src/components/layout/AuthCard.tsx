import type { ReactNode } from 'react'

import { Card } from '@/components/ui/Card'
import { cn } from '@/lib/utils'

interface AuthCardProps {
  title?: string
  children: ReactNode
  className?: string
  padding?: 'md' | 'lg'
}

export function AuthCard({ title, children, className, padding = 'md' }: AuthCardProps) {
  return (
    <Card
      title={title}
      padding={padding}
      className={cn(
        'auth-card border-auth-surfaceBorder bg-auth-surface shadow-authCard',
        className,
      )}
    >
      {children}
    </Card>
  )
}
