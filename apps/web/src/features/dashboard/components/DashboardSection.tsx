import type { ReactNode } from 'react'

import { LoadingState } from '@/components/common/LoadingState'
import { Card } from '@/components/ui/Card'
import { cn } from '@/lib/utils'

interface DashboardSectionProps {
  title: string
  description?: string
  action?: ReactNode
  children: ReactNode
  isLoading?: boolean
  error?: string | null
  className?: string
}

export function DashboardSection({
  title,
  description,
  action,
  children,
  isLoading = false,
  error = null,
  className,
}: DashboardSectionProps) {
  return (
    <Card className={cn('h-full', className)} padding="lg">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <h3 className="text-base font-semibold text-gray-900">{title}</h3>
          {description ? <p className="mt-1 text-sm text-gray-500">{description}</p> : null}
        </div>
        {action ? <div className="shrink-0">{action}</div> : null}
      </div>

      {isLoading ? <LoadingState message="Loading…" /> : null}
      {!isLoading && error ? (
        <p className="rounded-md border border-status-danger/20 bg-status-dangerSoft px-3 py-2 text-sm text-red-700">
          {error}
        </p>
      ) : null}
      {!isLoading && !error ? children : null}
    </Card>
  )
}
