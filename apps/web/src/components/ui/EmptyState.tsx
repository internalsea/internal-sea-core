import type { ReactNode } from 'react'

import { Button } from '@/components/ui/Button'

interface EmptyStateProps {
  title: string
  description: string
  action?: ReactNode
}

export function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="rounded-card border border-dashed border-app-border bg-app-surface px-6 py-10 text-center">
      <h3 className="text-base font-semibold text-gray-900">{title}</h3>
      <p className="mx-auto mt-2 max-w-lg text-sm text-gray-500">{description}</p>
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  )
}

export function EmptyStateButton(props: React.ComponentProps<typeof Button>) {
  return <Button variant="secondary" {...props} />
}
