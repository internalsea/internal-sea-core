import type { ReactNode } from 'react'

import { AppWaveBackground } from '@/components/layout/AppWaveBackground'
import { cn } from '@/lib/utils'

type AuthLayoutWidth = 'md' | 'lg'

interface AuthLayoutProps {
  children: ReactNode
  width?: AuthLayoutWidth
  className?: string
}

const widthClasses: Record<AuthLayoutWidth, string> = {
  md: 'max-w-md',
  lg: 'max-w-2xl',
}

export function AuthLayout({ children, width = 'md', className }: AuthLayoutProps) {
  return (
    <div
      className={cn(
        'relative flex min-h-screen items-center justify-center bg-auth-background px-4 py-10',
        className,
      )}
    >
      <AppWaveBackground />
      <div className={cn('relative z-10 w-full', widthClasses[width])}>{children}</div>
    </div>
  )
}
