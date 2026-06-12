import type { SeniorityLevel } from '@/features/people/types'

export interface SelectOption<T extends string = string> {
  value: T
  label: string
}

export const SENIORITY_LEVELS: SelectOption<SeniorityLevel>[] = [
  { value: 'intern', label: 'Intern' },
  { value: 'junior', label: 'Junior' },
  { value: 'medior', label: 'Medior' },
  { value: 'senior', label: 'Senior' },
  { value: 'lead', label: 'Lead' },
  { value: 'principal', label: 'Principal' },
  { value: 'director', label: 'Director' },
  { value: 'partner', label: 'Partner' },
]

export const seniorityLevelLabels: Record<SeniorityLevel, string> = Object.fromEntries(
  SENIORITY_LEVELS.map((item) => [item.value, item.label]),
) as Record<SeniorityLevel, string>

export const PERSON_STATUS_OPTIONS = [
  { value: 'true', label: 'Active' },
  { value: 'false', label: 'Inactive' },
] as const

export const DEFAULT_PAGE_SIZE = 20

export const SELECTOR_PAGE_SIZE = 100

export const selectClassName =
  'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue disabled:cursor-not-allowed disabled:bg-app-muted disabled:text-gray-400'
