import { Link } from 'react-router-dom'

import { cn } from '@/lib/utils'

type MetricCardVariant = 'neutral' | 'info' | 'success' | 'warning' | 'danger'

interface MetricCardProps {
  title: string
  value: number | string
  description?: string
  variant?: MetricCardVariant
  href?: string
}

const variantClasses: Record<MetricCardVariant, string> = {
  neutral: 'border-app-border',
  info: 'border-status-info/20 bg-status-infoSoft/40',
  success: 'border-status-success/20 bg-status-successSoft/40',
  warning: 'border-status-warning/20 bg-status-warningSoft/50',
  danger: 'border-status-danger/20 bg-status-dangerSoft/50',
}

const valueClasses: Record<MetricCardVariant, string> = {
  neutral: 'text-gray-900',
  info: 'text-status-info',
  success: 'text-status-success',
  warning: 'text-status-warning',
  danger: 'text-status-danger',
}

export function MetricCard({
  title,
  value,
  description,
  variant = 'neutral',
  href,
}: MetricCardProps) {
  const content = (
    <div
      className={cn(
        'rounded-card border bg-app-surface p-5 transition-colors',
        variantClasses[variant],
        href && 'hover:border-app-borderStrong',
      )}
    >
      <p className="text-xs font-medium uppercase tracking-wide text-gray-500">{title}</p>
      <p className={cn('mt-2 text-2xl font-semibold', valueClasses[variant])}>{value}</p>
      {description ? <p className="mt-1 text-xs text-gray-500">{description}</p> : null}
    </div>
  )

  if (href) {
    return (
      <Link to={href} className="block">
        {content}
      </Link>
    )
  }

  return content
}
