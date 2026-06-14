import { cn } from '@/lib/utils'

interface SparklesIconProps {
  className?: string
}

export function SparklesIcon({ className }: SparklesIconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={cn('h-4 w-4', className)}
      aria-hidden="true"
    >
      <path d="M9.94 15.5 12 21l2.06-5.5L19.5 13l-5.44-2.5L12 5 9.94 10.5 4.5 13z" />
      <path d="M5 3v4" />
      <path d="M3 5h4" />
      <path d="M19 17v4" />
      <path d="M17 19h4" />
    </svg>
  )
}
