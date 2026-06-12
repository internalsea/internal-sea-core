export type DataProductType =
  | 'dashboard'
  | 'dataset'
  | 'metric'
  | 'kpi'
  | 'api'
  | 'ai_agent'
  | 'report'
  | 'automation'
  | 'data_contract'
  | 'other'

export type DataProductStatus = 'draft' | 'active' | 'deprecated' | 'archived'

export type QualityStatus = 'unknown' | 'good' | 'warning' | 'critical'

export type WorkItemType =
  | 'epic'
  | 'story'
  | 'task'
  | 'bug'
  | 'risk'
  | 'decision'
  | 'technical_debt'
  | 'improvement'
  | 'support_request'

export type WorkItemStatus =
  | 'backlog'
  | 'ready'
  | 'in_progress'
  | 'review'
  | 'done'
  | 'closed'

export type WorkItemPriority = 'low' | 'medium' | 'high' | 'critical'

export type ProjectType =
  | 'client_project'
  | 'internal_project'
  | 'poc'
  | 'pilot'
  | 'mvp'
  | 'initiative'

export type ProjectStatus =
  | 'idea'
  | 'planned'
  | 'active'
  | 'on_hold'
  | 'completed'
  | 'cancelled'
  | 'archived'

export type ComplianceStatus =
  | 'not_started'
  | 'in_progress'
  | 'compliant'
  | 'non_compliant'
  | 'exception'
  | 'not_applicable'

export type ToolStatus =
  | 'proposed'
  | 'approved'
  | 'active'
  | 'restricted'
  | 'deprecated'
  | 'blocked'

export type DealStatus =
  | 'idea'
  | 'discovery'
  | 'qualified'
  | 'proposal'
  | 'negotiation'
  | 'won'
  | 'lost'
  | 'archived'

export const DATA_PRODUCT_TYPES: DataProductType[] = [
  'dashboard',
  'dataset',
  'metric',
  'kpi',
  'api',
  'ai_agent',
  'report',
  'automation',
  'data_contract',
  'other',
]

export const DATA_PRODUCT_STATUSES: DataProductStatus[] = [
  'draft',
  'active',
  'deprecated',
  'archived',
]

export const QUALITY_STATUSES: QualityStatus[] = ['unknown', 'good', 'warning', 'critical']
