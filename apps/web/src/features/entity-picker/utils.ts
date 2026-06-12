import {
  entityPickerPlaceholders,
  entityPickerTypeLabels,
} from '@/features/entity-picker/constants'
import type { EntityPickerResult, EntityPickerType, EntityPickerValue } from '@/features/entity-picker/types'

export function shortId(id: string): string {
  if (id.length <= 12) {
    return id
  }
  return `${id.slice(0, 8)}…`
}

export function getEntityTypeLabel(type: EntityPickerType): string {
  return entityPickerTypeLabels[type]
}

export function getEntityHref(type: EntityPickerType, id: string): string {
  switch (type) {
    case 'data_product':
      return `/data-products/${id}`
    case 'work_item':
      return `/work-items/${id}`
    case 'project':
      return `/projects/${id}`
    case 'internal_project':
      return `/internal-projects/${id}`
    case 'person':
      return `/people/${id}`
    case 'team':
      return `/teams/${id}`
    case 'capability':
      return `/capabilities/${id}`
    case 'file':
      return `/files/${id}`
    case 'policy':
      return `/compliance/policies/${id}`
    case 'compliance_check':
      return `/compliance/checks/${id}`
    default:
      return '#'
  }
}

export function normalizePickerResultToValue(result: EntityPickerResult): EntityPickerValue {
  return {
    entity_type: result.type,
    entity_id: result.id,
    title: result.title,
    description: result.description,
    url: result.url,
  }
}

export function buildPickerPlaceholder(allowedTypes: EntityPickerType[]): string {
  if (allowedTypes.length === 1) {
    return entityPickerPlaceholders[allowedTypes[0]] ?? `Search ${getEntityTypeLabel(allowedTypes[0]).toLowerCase()}…`
  }
  const labels = sortAllowedTypes(allowedTypes).map((type) => getEntityTypeLabel(type).toLowerCase())
  if (labels.length <= 2) {
    return `Search ${labels.join(' or ')}…`
  }
  return 'Search entities…'
}

export function sortAllowedTypes(types: EntityPickerType[]): EntityPickerType[] {
  const order = new Map(ENTITY_PICKER_TYPE_ORDER.map((type, index) => [type, index]))
  return [...types].sort((left, right) => (order.get(left) ?? 99) - (order.get(right) ?? 99))
}

const ENTITY_PICKER_TYPE_ORDER: EntityPickerType[] = [
  'person',
  'team',
  'capability',
  'data_product',
  'work_item',
  'project',
  'internal_project',
  'file',
  'policy',
  'compliance_check',
]

export function isValidUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value)
}
