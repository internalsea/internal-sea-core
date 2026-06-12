export type NotificationChannelType =
  | 'email'
  | 'teams'
  | 'slack'
  | 'webhook'
  | 'in_app'
  | 'other'

export type NotificationChannelStatus = 'draft' | 'active' | 'paused' | 'archived'

export type NotificationTemplateStatus = 'draft' | 'active' | 'archived'

export type NotificationMessageStatus =
  | 'draft'
  | 'queued'
  | 'simulated'
  | 'sent'
  | 'failed'
  | 'cancelled'

export type NotificationPriority = 'low' | 'normal' | 'high' | 'urgent'

export type NotificationDeliveryStatus = 'pending' | 'simulated' | 'sent' | 'failed' | 'skipped'

export type NotificationRecipientType = 'user' | 'person' | 'email' | 'channel'

export type NotificationEventType =
  | 'manual'
  | 'automation_run'
  | 'compliance_due'
  | 'work_item_due'
  | 'project_health'
  | 'data_product_review'
  | 'system'

export interface NotificationChannel {
  id: string
  name: string
  channel_type: NotificationChannelType
  status: NotificationChannelStatus
  description: string | null
  endpoint_url: string | null
  default_recipient: string | null
  provider_config: Record<string, unknown> | null
  created_by_id: string | null
  created_at: string
  updated_at: string
}

export interface NotificationChannelListItem {
  id: string
  name: string
  channel_type: NotificationChannelType
  status: NotificationChannelStatus
  default_recipient: string | null
  updated_at: string
}

export interface NotificationTemplateListItem {
  id: string
  name: string
  status: NotificationTemplateStatus
  event_type: NotificationEventType | null
  updated_at: string
}

export type NotificationChannelCreateInput = {
  name: string
  channel_type: NotificationChannelType
  status?: NotificationChannelStatus
  description?: string | null
  endpoint_url?: string | null
  default_recipient?: string | null
  provider_config?: Record<string, unknown> | null
}

export type NotificationChannelUpdateInput = Partial<NotificationChannelCreateInput>

export interface NotificationTemplate {
  id: string
  name: string
  status: NotificationTemplateStatus
  event_type: NotificationEventType | null
  subject_template: string | null
  body_template: string
  description: string | null
  created_by_id: string | null
  created_at: string
  updated_at: string
}

export type NotificationTemplateCreateInput = {
  name: string
  status?: NotificationTemplateStatus
  event_type?: NotificationEventType | null
  subject_template?: string | null
  body_template: string
  description?: string | null
}

export type NotificationTemplateUpdateInput = Partial<NotificationTemplateCreateInput>

export interface NotificationPreference {
  id: string
  user_id: string | null
  person_id: string | null
  channel_type: NotificationChannelType
  event_type: NotificationEventType
  is_enabled: boolean
  created_at: string
  updated_at: string
}

export type NotificationPreferenceCreateInput = {
  user_id?: string | null
  person_id?: string | null
  channel_type: NotificationChannelType
  event_type: NotificationEventType
  is_enabled?: boolean
}

export type NotificationPreferenceUpdateInput = {
  is_enabled?: boolean
}

export interface NotificationMessage {
  id: string
  channel_id: string | null
  template_id: string | null
  status: NotificationMessageStatus
  priority: NotificationPriority
  event_type: NotificationEventType
  subject: string | null
  body: string
  recipient_type: NotificationRecipientType | null
  recipient_value: string | null
  entity_type: string | null
  entity_id: string | null
  automation_run_id: string | null
  created_by_id: string | null
  scheduled_at: string | null
  sent_at: string | null
  simulated_at: string | null
  error_message: string | null
  metadata: Record<string, unknown> | null
  created_at: string
  updated_at: string
}

export interface NotificationMessageListItem {
  id: string
  channel_id: string | null
  template_id: string | null
  status: NotificationMessageStatus
  priority: NotificationPriority
  event_type: NotificationEventType
  subject: string | null
  recipient_type: NotificationRecipientType | null
  recipient_value: string | null
  entity_type: string | null
  entity_id: string | null
  automation_run_id: string | null
  scheduled_at: string | null
  sent_at: string | null
  simulated_at: string | null
  updated_at: string
}

export type NotificationMessageCreateInput = {
  channel_id?: string | null
  template_id?: string | null
  status?: NotificationMessageStatus
  priority?: NotificationPriority
  event_type?: NotificationEventType
  subject?: string | null
  body: string
  recipient_type?: NotificationRecipientType | null
  recipient_value?: string | null
  entity_type?: string | null
  entity_id?: string | null
  automation_run_id?: string | null
  scheduled_at?: string | null
  metadata?: Record<string, unknown> | null
}

export type NotificationMessageUpdateInput = Partial<NotificationMessageCreateInput>

export interface NotificationDeliveryAttempt {
  id: string
  message_id: string
  status: NotificationDeliveryStatus
  attempt_number: number
  provider: string | null
  provider_message_id: string | null
  request_payload: Record<string, unknown> | null
  response_payload: Record<string, unknown> | null
  error_message: string | null
  started_at: string | null
  finished_at: string | null
  created_at: string
  updated_at: string
}

export interface NotificationSendRequest {
  simulate?: boolean
  recipient_override?: string | null
  context?: Record<string, unknown> | null
}

export interface NotificationSendResult {
  message: NotificationMessage
  delivery_attempt: NotificationDeliveryAttempt
  simulated: boolean
  result_summary: string
}

export interface NotificationRenderRequest {
  template_id: string
  context?: Record<string, unknown> | null
}

export interface NotificationRenderResult {
  subject: string | null
  body: string
}

export interface NotificationOverview {
  channels_total: number
  channels_active: number
  templates_total: number
  templates_active: number
  messages_total: number
  messages_sent: number
  messages_simulated: number
  messages_failed: number
  delivery_attempts_total: number
  delivery_attempts_failed: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface ChannelFilters {
  search?: string
  channel_type?: NotificationChannelType
  status?: NotificationChannelStatus
  page?: number
  page_size?: number
}

export interface TemplateFilters {
  search?: string
  status?: NotificationTemplateStatus
  event_type?: NotificationEventType
  page?: number
  page_size?: number
}

export interface MessageFilters {
  search?: string
  status?: NotificationMessageStatus
  priority?: NotificationPriority
  event_type?: NotificationEventType
  channel_id?: string
  template_id?: string
  entity_type?: string
  entity_id?: string
  automation_run_id?: string
  page?: number
  page_size?: number
}

export interface EntityNotificationsResponse {
  entity_type: string
  entity_id: string
  messages: NotificationMessageListItem[]
  total: number
}
