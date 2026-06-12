import { cn } from '@/lib/utils'

interface MiniProgressBarProps {
  value: number | null
  max?: number
  label?: string
}

export function MiniProgressBar({ value, max = 100, label }: MiniProgressBarProps) {
  const percent = value == null ? 0 : Math.min(100, Math.round((value / max) * 100))
  const status = value == null ? 'unknown' : value >= 85 ? 'good' : value >= 70 ? 'warning' : 'critical'
  const barColor =
    status === 'good'
      ? 'bg-status-success'
      : status === 'warning'
        ? 'bg-status-warning'
        : status === 'critical'
          ? 'bg-status-danger'
          : 'bg-gray-300'

  return (
    <div>
      {label ? (
        <div className="mb-1 flex justify-between text-xs text-gray-600">
          <span>{label}</span>
          <span>{value == null ? '—' : `${percent}%`}</span>
        </div>
      ) : null}
      <div className="h-2 w-full overflow-hidden rounded-full bg-app-muted">
        <div className={cn('h-full rounded-full transition-all', barColor)} style={{ width: `${percent}%` }} />
      </div>
    </div>
  )
}
