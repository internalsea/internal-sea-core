import type { BadgeVariant } from '@/lib/designTokens'
import type {
  NotificationChannelStatus,
  NotificationChannelType,
  NotificationDeliveryStatus,
  NotificationEventType,
  NotificationMessageStatus,
  NotificationPriority,
  NotificationRecipientType,
  NotificationTemplateStatus,
} from '@/features/notifications/types'

export const DEFAULT_PAGE_SIZE = 20

export const NOTIFICATION_CHANNEL_TYPES: NotificationChannelType[] = [
  'email',
  'teams',
  'slack',
  'webhook',
  'in_app',
  'other',
]

export const NOTIFICATION_CHANNEL_STATUSES: NotificationChannelStatus[] = [
  'draft',
  'active',
  'paused',
  'archived',
]

export const NOTIFICATION_TEMPLATE_STATUSES: NotificationTemplateStatus[] = [
  'draft',
  'active',
  'archived',
]

export const NOTIFICATION_MESSAGE_STATUSES: NotificationMessageStatus[] = [
  'draft',
  'queued',
  'simulated',
  'sent',
  'failed',
  'cancelled',
]

export const NOTIFICATION_PRIORITIES: NotificationPriority[] = [
  'low',
  'normal',
  'high',
  'urgent',
]

export const NOTIFICATION_DELIVERY_STATUSES: NotificationDeliveryStatus[] = [
  'pending',
  'simulated',
  'sent',
  'failed',
  'skipped',
]

export const NOTIFICATION_RECIPIENT_TYPES: NotificationRecipientType[] = [
  'user',
  'person',
  'email',
  'channel',
]

export const NOTIFICATION_EVENT_TYPES: NotificationEventType[] = [
  'manual',
  'automation_run',
  'compliance_due',
  'work_item_due',
  'project_health',
  'data_product_review',
  'system',
]

export const channelTypeBadgeVariants: Record<NotificationChannelType, BadgeVariant> = {
  email: 'info',
  teams: 'teal',
  slack: 'teal',
  webhook: 'warning',
  in_app: 'success',
  other: 'neutral',
}

export const messageStatusBadgeVariants: Record<NotificationMessageStatus, BadgeVariant> = {
  draft: 'neutral',
  queued: 'info',
  simulated: 'teal',
  sent: 'success',
  failed: 'danger',
  cancelled: 'neutral',
}

export const priorityBadgeVariants: Record<NotificationPriority, BadgeVariant> = {
  low: 'neutral',
  normal: 'info',
  high: 'warning',
  urgent: 'danger',
}

export const deliveryStatusBadgeVariants: Record<NotificationDeliveryStatus, BadgeVariant> = {
  pending: 'neutral',
  simulated: 'teal',
  sent: 'success',
  failed: 'danger',
  skipped: 'warning',
}

export const NOTIFICATION_ENTITY_PICKER_TYPES = [
  'data_product',
  'work_item',
  'project',
  'internal_project',
  'person',
  'team',
  'capability',
  'compliance_check',
] as const

export const TEMPLATE_PLACEHOLDER_HELP =
  'Supported placeholders: {{app_name}}, {{entity_type}}, {{entity_id}}, {{title}}, {{status}}, {{event_type}}'
