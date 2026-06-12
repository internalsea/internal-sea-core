import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  ChannelFilters,
  EntityNotificationsResponse,
  MessageFilters,
  NotificationChannel,
  NotificationChannelCreateInput,
  NotificationChannelUpdateInput,
  NotificationDeliveryAttempt,
  NotificationMessage,
  NotificationMessageCreateInput,
  NotificationMessageUpdateInput,
  NotificationOverview,
  NotificationPreference,
  NotificationPreferenceCreateInput,
  NotificationPreferenceUpdateInput,
  NotificationRenderRequest,
  NotificationRenderResult,
  NotificationSendRequest,
  NotificationSendResult,
  NotificationTemplate,
  NotificationTemplateCreateInput,
  NotificationTemplateUpdateInput,
  PaginatedResponse,
  TemplateFilters,
} from '@/features/notifications/types'

function toParams(
  filters?: object,
): Record<string, string | number | undefined> | undefined {
  if (!filters) return undefined
  const params: Record<string, string | number | undefined> = {}
  for (const [key, value] of Object.entries(filters as Record<string, unknown>)) {
    if (typeof value !== 'string' && typeof value !== 'number') continue
    if (value !== undefined && value !== null && value !== '') {
      params[key] = value
    }
  }
  return Object.keys(params).length ? params : undefined
}

export function getNotificationOverview(): Promise<NotificationOverview> {
  return apiGet<NotificationOverview>('/notifications/overview')
}

export function getNotificationChannels(
  filters?: ChannelFilters,
): Promise<PaginatedResponse<NotificationChannel>> {
  return apiGet('/notifications/channels', toParams(filters))
}

export function getNotificationChannel(id: string): Promise<NotificationChannel> {
  return apiGet(`/notifications/channels/${id}`)
}

export function createNotificationChannel(
  payload: NotificationChannelCreateInput,
): Promise<NotificationChannel> {
  return apiPost('/notifications/channels', payload)
}

export function updateNotificationChannel(
  id: string,
  payload: NotificationChannelUpdateInput,
): Promise<NotificationChannel> {
  return apiPatch(`/notifications/channels/${id}`, payload)
}

export function deleteNotificationChannel(id: string): Promise<void> {
  return apiDelete(`/notifications/channels/${id}`)
}

export function getNotificationTemplates(
  filters?: TemplateFilters,
): Promise<PaginatedResponse<NotificationTemplate>> {
  return apiGet('/notifications/templates', toParams(filters))
}

export function getNotificationTemplate(id: string): Promise<NotificationTemplate> {
  return apiGet(`/notifications/templates/${id}`)
}

export function createNotificationTemplate(
  payload: NotificationTemplateCreateInput,
): Promise<NotificationTemplate> {
  return apiPost('/notifications/templates', payload)
}

export function updateNotificationTemplate(
  id: string,
  payload: NotificationTemplateUpdateInput,
): Promise<NotificationTemplate> {
  return apiPatch(`/notifications/templates/${id}`, payload)
}

export function deleteNotificationTemplate(id: string): Promise<void> {
  return apiDelete(`/notifications/templates/${id}`)
}

export function renderNotificationTemplate(
  payload: NotificationRenderRequest,
): Promise<NotificationRenderResult> {
  return apiPost('/notifications/templates/render', payload)
}

export function getNotificationPreferences(params?: {
  user_id?: string
  person_id?: string
  page?: number
  page_size?: number
}): Promise<NotificationPreference[]> {
  return apiGet('/notifications/preferences', toParams(params))
}

export function createNotificationPreference(
  payload: NotificationPreferenceCreateInput,
): Promise<NotificationPreference> {
  return apiPost('/notifications/preferences', payload)
}

export function updateNotificationPreference(
  id: string,
  payload: NotificationPreferenceUpdateInput,
): Promise<NotificationPreference> {
  return apiPatch(`/notifications/preferences/${id}`, payload)
}

export function deleteNotificationPreference(id: string): Promise<void> {
  return apiDelete(`/notifications/preferences/${id}`)
}

export function getNotificationMessages(
  filters?: MessageFilters,
): Promise<PaginatedResponse<NotificationMessage>> {
  return apiGet('/notifications/messages', toParams(filters))
}

export function getNotificationMessage(id: string): Promise<NotificationMessage> {
  return apiGet(`/notifications/messages/${id}`)
}

export function createNotificationMessage(
  payload: NotificationMessageCreateInput,
): Promise<NotificationMessage> {
  return apiPost('/notifications/messages', payload)
}

export function updateNotificationMessage(
  id: string,
  payload: NotificationMessageUpdateInput,
): Promise<NotificationMessage> {
  return apiPatch(`/notifications/messages/${id}`, payload)
}

export function deleteNotificationMessage(id: string): Promise<void> {
  return apiDelete(`/notifications/messages/${id}`)
}

export function sendNotificationMessage(
  id: string,
  payload: NotificationSendRequest,
): Promise<NotificationSendResult> {
  return apiPost(`/notifications/messages/${id}/send`, payload)
}

export function queueNotificationMessage(id: string): Promise<NotificationMessage> {
  return apiPost(`/notifications/messages/${id}/queue`)
}

export function getMessageDeliveryAttempts(
  messageId: string,
  params?: { page?: number; page_size?: number },
): Promise<PaginatedResponse<NotificationDeliveryAttempt>> {
  return apiGet(`/notifications/messages/${messageId}/delivery-attempts`, toParams(params))
}

export function getNotificationDeliveryAttempts(params?: {
  page?: number
  page_size?: number
}): Promise<PaginatedResponse<NotificationDeliveryAttempt>> {
  return apiGet('/notifications/delivery-attempts', toParams(params))
}

export function getEntityNotifications(
  entityType: string,
  entityId: string,
): Promise<EntityNotificationsResponse> {
  return apiGet(`/notifications/entity/${entityType}/${entityId}`)
}
