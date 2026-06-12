export type EntityPickerType =
  | 'data_product'
  | 'work_item'
  | 'project'
  | 'internal_project'
  | 'person'
  | 'team'
  | 'capability'
  | 'file'
  | 'policy'
  | 'compliance_check'

export interface EntityPickerResult {
  id: string
  type: EntityPickerType
  title: string
  description: string | null
  status: string | null
  secondary_status: string | null
  url: string
  matched_field: string | null
  updated_at: string | null
}

export interface EntityPickerValue {
  entity_type: EntityPickerType
  entity_id: string
  title?: string
  description?: string | null
  url?: string
}

export interface EntityPickerProps {
  value: EntityPickerValue | null
  onChange: (value: EntityPickerValue | null) => void
  allowedTypes: EntityPickerType[]
  label?: string
  placeholder?: string
  helperText?: string
  disabled?: boolean
  required?: boolean
  error?: string
  allowClear?: boolean
}

export interface EntityReferenceProps {
  entityType: EntityPickerType
  entityId: string
  showType?: boolean
  link?: boolean
  fallbackLabel?: string
}
