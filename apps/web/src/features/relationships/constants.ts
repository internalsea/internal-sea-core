import type { EntityLinkType, EntityType } from '@/features/relationships/types'

export const ACTIVE_ENTITY_TYPES: EntityType[] = [
  'data_product',
  'work_item',
  'project',
  'internal_project',
  'person',
  'team',
  'capability',
]

export const ENTITY_LINK_TYPES: EntityLinkType[] = [
  'relates_to',
  'depends_on',
  'blocks',
  'duplicates',
  'replaces',
  'owns',
  'supports',
  'improves',
  'affects',
  'created_from',
  'evidence_for',
  'decision_for',
  'risk_for',
]

export const entityTypeLabels: Record<EntityType, string> = {
  data_product: 'Data Product',
  work_item: 'Work Item',
  project: 'Project',
  internal_project: 'Internal Project',
  person: 'Person',
  team: 'Team',
  capability: 'Capability',
  policy: 'Policy',
  rule: 'Rule',
  compliance_check: 'Compliance Check',
  file: 'File',
  meeting: 'Meeting',
  deal: 'Deal',
  tool: 'Tool',
}

export const entityLinkTypeLabels: Record<EntityLinkType, string> = {
  relates_to: 'Relates to',
  depends_on: 'Depends on',
  blocks: 'Blocks',
  duplicates: 'Duplicates',
  replaces: 'Replaces',
  owns: 'Owns',
  supports: 'Supports',
  improves: 'Improves',
  affects: 'Affects',
  created_from: 'Created from',
  evidence_for: 'Evidence for',
  decision_for: 'Decision for',
  risk_for: 'Risk for',
}
