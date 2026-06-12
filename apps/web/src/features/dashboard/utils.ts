import type { BadgeVariant } from '@/lib/designTokens'
import type { HealthStatus, InsightSeverity } from '@/features/dashboard/types'
import {
  priorityVariantMap,
  projectHealthVariantMap,
  qualityVariantMap,
  statusVariantMap,
} from '@/lib/designTokens'
import type { OwnershipGapItem, ProjectHealthItem } from '@/features/dashboard/types'

export function formatDate(value: string | null | undefined): string {
  if (!value) {
    return '—'
  }
  const date = new Date(value.includes('T') ? value : `${value}T00:00:00`)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return '—'
  }
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatEntityType(value: string): string {
  return value
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}

export function formatCount(value: number): string {
  return new Intl.NumberFormat().format(value)
}

export function getProjectHref(project: Pick<ProjectHealthItem, 'id' | 'project_type'>): string {
  if (project.project_type === 'internal_project') {
    return `/internal-projects/${project.id}`
  }
  return `/projects/${project.id}`
}

export function getOwnershipGapHref(gap: OwnershipGapItem): string | null {
  switch (gap.entity_type) {
    case 'data_product':
      return `/data-products/${gap.entity_id}`
    case 'project':
      return `/projects/${gap.entity_id}`
    case 'work_item':
      return `/work-items/${gap.entity_id}`
    default:
      return null
  }
}

export function getHealthVariant(health: HealthStatus | string | null | undefined): BadgeVariant {
  switch (health) {
    case 'good':
    case 'healthy':
      return 'success'
    case 'warning':
      return 'warning'
    case 'critical':
      return 'danger'
    default:
      if (!health) {
        return 'neutral'
      }
      return projectHealthVariantMap[health] ?? 'neutral'
  }
}

export function getSeverityVariant(severity: InsightSeverity | string): BadgeVariant {
  switch (severity) {
    case 'critical':
    case 'high':
      return 'danger'
    case 'warning':
    case 'medium':
      return 'warning'
    case 'info':
      return 'info'
    case 'low':
      return 'neutral'
    default:
      return 'neutral'
  }
}

export function getStatusVariant(status: string): BadgeVariant {
  return statusVariantMap[status] ?? 'neutral'
}

export function getQualityVariant(quality: string): BadgeVariant {
  return qualityVariantMap[quality] ?? 'neutral'
}

export function getPriorityVariant(priority: string): BadgeVariant {
  return priorityVariantMap[priority] ?? 'neutral'
}

export function formatScore(value: number | null | undefined): string {
  if (value == null) {
    return '—'
  }
  return `${Math.round(value)}`
}

export function formatPercent(value: number | null | undefined): string {
  if (value == null) {
    return '—'
  }
  return `${value.toFixed(0)}%`
}

export function formatInsightCategory(category: string): string {
  return category
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}

export function getDashboardEntityHref(
  entityType: string | null | undefined,
  entityId: string | null | undefined,
): string | null {
  if (!entityType || !entityId) {
    return null
  }
  const routes: Record<string, string> = {
    data_product: `/data-products/${entityId}`,
    work_item: `/work-items/${entityId}`,
    project: `/projects/${entityId}`,
    internal_project: `/internal-projects/${entityId}`,
    compliance_check: `/compliance/checks/${entityId}`,
  }
  return routes[entityType] ?? null
}

export function sortStatusEntries(entries: Record<string, number>): [string, number][] {
  return Object.entries(entries).sort((a, b) => b[1] - a[1])
}

export function calculateMiniBarPercent(value: number, total: number): number {
  if (total <= 0) {
    return 0
  }
  return Math.min(100, Math.round((value / total) * 100))
}

export function isOverdue(dueDate: string | null | undefined): boolean {
  if (!dueDate) {
    return false
  }
  const date = new Date(`${dueDate}T00:00:00`)
  if (Number.isNaN(date.getTime())) {
    return false
  }
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return date < today
}
