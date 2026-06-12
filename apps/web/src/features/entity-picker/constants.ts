import type { BadgeVariant } from '@/lib/designTokens'

import type { EntityPickerType } from '@/features/entity-picker/types'

export const ENTITY_PICKER_TYPES: EntityPickerType[] = [
  'data_product',
  'work_item',
  'project',
  'internal_project',
  'person',
  'team',
  'capability',
  'file',
  'policy',
  'compliance_check',
]

export const entityPickerTypeLabels: Record<EntityPickerType, string> = {
  data_product: 'Data Product',
  work_item: 'Work Item',
  project: 'Project',
  internal_project: 'Internal Project',
  person: 'Person',
  team: 'Team',
  capability: 'Capability',
  file: 'File',
  policy: 'Policy',
  compliance_check: 'Compliance Check',
}

export const entityPickerBadgeVariants: Record<EntityPickerType, BadgeVariant> = {
  data_product: 'info',
  work_item: 'teal',
  project: 'warning',
  internal_project: 'teal',
  person: 'neutral',
  team: 'neutral',
  capability: 'info',
  file: 'neutral',
  policy: 'warning',
  compliance_check: 'danger',
}

export const entityPickerPlaceholders: Partial<Record<EntityPickerType, string>> = {
  person: 'Search people…',
  team: 'Search teams…',
  capability: 'Search capabilities…',
  data_product: 'Search data products…',
  work_item: 'Search work items…',
  project: 'Search projects…',
  internal_project: 'Search internal projects…',
  file: 'Search files…',
  policy: 'Search policies…',
  compliance_check: 'Search checks…',
}
