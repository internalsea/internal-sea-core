import type { ReactNode } from 'react'

import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'

interface ModulePlaceholderProps {
  title: string
  description: string
  children: ReactNode
}

export function ModulePlaceholder({ title, description, children }: ModulePlaceholderProps) {
  return (
    <div>
      <PageHeader title={title} description={description} />
      <Card>{children}</Card>
    </div>
  )
}
