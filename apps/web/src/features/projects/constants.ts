import type { ProjectStatus, ProjectType } from '@/types/enums'

export interface SelectOption<T extends string = string> {
  value: T
  label: string
}

export const PROJECT_TYPES: SelectOption<ProjectType>[] = [
  { value: 'client_project', label: 'Client Project' },
  { value: 'internal_project', label: 'Internal Project' },
  { value: 'poc', label: 'POC' },
  { value: 'pilot', label: 'Pilot' },
  { value: 'mvp', label: 'MVP' },
  { value: 'initiative', label: 'Initiative' },
]

export const PROJECT_STATUSES: SelectOption<ProjectStatus>[] = [
  { value: 'idea', label: 'Idea' },
  { value: 'planned', label: 'Planned' },
  { value: 'active', label: 'Active' },
  { value: 'on_hold', label: 'On Hold' },
  { value: 'completed', label: 'Completed' },
  { value: 'cancelled', label: 'Cancelled' },
  { value: 'archived', label: 'Archived' },
]

export const PROJECT_HEALTH_STATUSES: SelectOption[] = [
  { value: 'unknown', label: 'Unknown' },
  { value: 'healthy', label: 'Healthy' },
  { value: 'warning', label: 'Warning' },
  { value: 'critical', label: 'Critical' },
]

export const PROJECT_PRIORITIES: SelectOption[] = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
  { value: 'critical', label: 'Critical' },
]

export const projectTypeLabels: Record<ProjectType, string> = Object.fromEntries(
  PROJECT_TYPES.map((item) => [item.value, item.label]),
) as Record<ProjectType, string>

export const projectStatusLabels: Record<ProjectStatus, string> = Object.fromEntries(
  PROJECT_STATUSES.map((item) => [item.value, item.label]),
) as Record<ProjectStatus, string>

export const projectHealthStatusLabels: Record<string, string> = Object.fromEntries(
  PROJECT_HEALTH_STATUSES.map((item) => [item.value, item.label]),
)

export const DEFAULT_PAGE_SIZE = 20

export const selectClassName =
  'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue disabled:cursor-not-allowed disabled:bg-app-muted disabled:text-gray-400'
