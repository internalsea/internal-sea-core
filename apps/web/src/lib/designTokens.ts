/**
 * Centralized design tokens and status-to-badge mappings.
 * Use these instead of hardcoding colors in feature components.
 */

export type BadgeVariant = 'neutral' | 'info' | 'success' | 'warning' | 'danger' | 'teal'

export const colors = {
  core: {
    navy: '#111827',
    blue: '#2563EB',
    blueHover: '#1D4ED8',
    blueSoft: '#EFF6FF',
    teal: '#0F766E',
    tealSoft: '#F0FDFA',
  },
  app: {
    background: '#F9FAFB',
    surface: '#FFFFFF',
    muted: '#F3F4F6',
    border: '#E5E7EB',
    borderStrong: '#D1D5DB',
  },
  auth: {
    background: '#E3EBF3',
    surface: '#EDF2F8',
    surfaceBorder: '#D0DAE6',
    input: '#F5F8FB',
    inputBorder: '#BFCBD8',
    wave: '#A8BDD1',
    nav: '#94AFC7',
  },
  text: {
    primary: '#111827',
    secondary: '#374151',
    muted: '#6B7280',
    disabled: '#9CA3AF',
  },
  status: {
    success: '#15803D',
    successSoft: '#F0FDF4',
    warning: '#B45309',
    warningSoft: '#FFFBEB',
    danger: '#B91C1C',
    dangerSoft: '#FEF2F2',
    info: '#1D4ED8',
    infoSoft: '#EFF6FF',
    neutral: '#4B5563',
    neutralSoft: '#F3F4F6',
  },
} as const

export const badgeVariantClasses: Record<BadgeVariant, string> = {
  neutral: 'bg-status-neutralSoft text-status-neutral',
  info: 'bg-status-infoSoft text-status-info',
  success: 'bg-status-successSoft text-status-success',
  warning: 'bg-status-warningSoft text-status-warning',
  danger: 'bg-status-dangerSoft text-status-danger',
  teal: 'bg-core-tealSoft text-core-teal',
}

/** Data product lifecycle status */
export const statusVariantMap: Record<string, BadgeVariant> = {
  draft: 'neutral',
  active: 'success',
  deprecated: 'warning',
  archived: 'neutral',
}

/** Data quality status */
export const qualityVariantMap: Record<string, BadgeVariant> = {
  unknown: 'neutral',
  good: 'success',
  warning: 'warning',
  critical: 'danger',
}

/** Work item status */
export const workStatusVariantMap: Record<string, BadgeVariant> = {
  backlog: 'neutral',
  ready: 'info',
  in_progress: 'teal',
  review: 'warning',
  done: 'success',
  closed: 'neutral',
}

/** Work item / task priority */
export const priorityVariantMap: Record<string, BadgeVariant> = {
  low: 'neutral',
  medium: 'info',
  high: 'warning',
  critical: 'danger',
}

/** Project lifecycle status */
export const projectStatusVariantMap: Record<string, BadgeVariant> = {
  idea: 'neutral',
  planned: 'info',
  active: 'teal',
  on_hold: 'warning',
  completed: 'success',
  cancelled: 'danger',
  archived: 'neutral',
}

/** Project type */
export const projectTypeVariantMap: Record<string, BadgeVariant> = {
  client_project: 'info',
  internal_project: 'teal',
  poc: 'warning',
  pilot: 'warning',
  mvp: 'success',
  initiative: 'neutral',
}

/** Person seniority level */
export const seniorityVariantMap: Record<string, BadgeVariant> = {
  intern: 'neutral',
  junior: 'neutral',
  medior: 'info',
  senior: 'teal',
  lead: 'teal',
  principal: 'warning',
  director: 'warning',
  partner: 'info',
}

/** Project health status */
export const projectHealthVariantMap: Record<string, BadgeVariant> = {
  unknown: 'neutral',
  healthy: 'success',
  warning: 'warning',
  critical: 'danger',
}

/** Compliance tracking status */
export const complianceStatusVariantMap: Record<string, BadgeVariant> = {
  not_started: 'neutral',
  in_progress: 'teal',
  compliant: 'success',
  non_compliant: 'danger',
  exception: 'warning',
  not_applicable: 'neutral',
}

/** Work item type */
export const workItemTypeVariantMap: Record<string, BadgeVariant> = {
  epic: 'info',
  story: 'teal',
  task: 'neutral',
  bug: 'danger',
  risk: 'warning',
  decision: 'info',
  technical_debt: 'warning',
  improvement: 'teal',
  support_request: 'neutral',
}

const allStatusMaps = [
  statusVariantMap,
  qualityVariantMap,
  workStatusVariantMap,
  priorityVariantMap,
  projectStatusVariantMap,
  projectTypeVariantMap,
  projectHealthVariantMap,
  seniorityVariantMap,
  complianceStatusVariantMap,
  workItemTypeVariantMap,
] as const

/** Resolve a status string to a badge variant across all domain maps. */
export function resolveStatusVariant(status: string): BadgeVariant {
  for (const map of allStatusMaps) {
    const variant = map[status]
    if (variant) {
      return variant
    }
  }
  return 'neutral'
}
