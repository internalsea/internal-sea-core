import type { InputHTMLAttributes } from 'react'

import { cn } from '@/lib/utils'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  helpText?: string
  error?: string
}

export function Input({ label, helpText, error, className, id, ...props }: InputProps) {
  const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-')

  return (
    <div className="space-y-1.5">
      {label ? (
        <label htmlFor={inputId} className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      ) : null}
      <input
        id={inputId}
        className={cn(
          'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue',
          error && 'border-status-danger focus:border-status-danger focus:ring-status-danger',
          className,
        )}
        {...props}
      />
      {helpText && !error ? (
        <p className="text-xs text-gray-500">{helpText}</p>
      ) : null}
      {error ? <p className="text-xs text-red-700">{error}</p> : null}
    </div>
  )
}
