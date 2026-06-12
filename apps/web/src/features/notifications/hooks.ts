import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createNotificationChannel,
  createNotificationMessage,
  createNotificationPreference,
  createNotificationTemplate,
  deleteNotificationChannel,
  deleteNotificationMessage,
  deleteNotificationPreference,
  deleteNotificationTemplate,
  getEntityNotifications,
  getMessageDeliveryAttempts,
  getNotificationChannel,
  getNotificationChannels,
  getNotificationDeliveryAttempts,
  getNotificationMessage,
  getNotificationMessages,
  getNotificationOverview,
  getNotificationPreferences,
  getNotificationTemplate,
  getNotificationTemplates,
  renderNotificationTemplate,
  queueNotificationMessage,
  sendNotificationMessage,
  updateNotificationChannel,
  updateNotificationMessage,
  updateNotificationPreference,
  updateNotificationTemplate,
} from '@/features/notifications/api'
import type {
  ChannelFilters,
  MessageFilters,
  NotificationChannelCreateInput,
  NotificationChannelUpdateInput,
  NotificationMessageCreateInput,
  NotificationMessageUpdateInput,
  NotificationPreferenceCreateInput,
  NotificationPreferenceUpdateInput,
  NotificationRenderRequest,
  NotificationSendRequest,
  NotificationTemplateCreateInput,
  NotificationTemplateUpdateInput,
  TemplateFilters,
} from '@/features/notifications/types'

export const notificationKeys = {
  all: ['notifications'] as const,
  overview: () => [...notificationKeys.all, 'overview'] as const,
  channels: () => [...notificationKeys.all, 'channels'] as const,
  channelLists: () => [...notificationKeys.channels(), 'list'] as const,
  channelList: (filters: ChannelFilters) => [...notificationKeys.channelLists(), filters] as const,
  channelDetails: () => [...notificationKeys.channels(), 'detail'] as const,
  channelDetail: (id: string) => [...notificationKeys.channelDetails(), id] as const,
  templates: () => [...notificationKeys.all, 'templates'] as const,
  templateLists: () => [...notificationKeys.templates(), 'list'] as const,
  templateList: (filters: TemplateFilters) => [...notificationKeys.templateLists(), filters] as const,
  templateDetails: () => [...notificationKeys.templates(), 'detail'] as const,
  templateDetail: (id: string) => [...notificationKeys.templateDetails(), id] as const,
  preferences: () => [...notificationKeys.all, 'preferences'] as const,
  messages: () => [...notificationKeys.all, 'messages'] as const,
  messageLists: () => [...notificationKeys.messages(), 'list'] as const,
  messageList: (filters: MessageFilters) => [...notificationKeys.messageLists(), filters] as const,
  messageDetails: () => [...notificationKeys.messages(), 'detail'] as const,
  messageDetail: (id: string) => [...notificationKeys.messageDetails(), id] as const,
  deliveryAttempts: (messageId?: string) =>
    [...notificationKeys.all, 'delivery-attempts', messageId ?? 'all'] as const,
  entity: (entityType: string, entityId: string) =>
    [...notificationKeys.all, 'entity', entityType, entityId] as const,
}

export function useNotificationOverview() {
  return useQuery({ queryKey: notificationKeys.overview(), queryFn: getNotificationOverview })
}

export function useNotificationChannels(filters: ChannelFilters) {
  return useQuery({
    queryKey: notificationKeys.channelList(filters),
    queryFn: () => getNotificationChannels(filters),
  })
}

export function useNotificationChannel(id: string | undefined) {
  return useQuery({
    queryKey: notificationKeys.channelDetail(id ?? ''),
    queryFn: () => getNotificationChannel(id!),
    enabled: Boolean(id),
  })
}

export function useCreateNotificationChannel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: NotificationChannelCreateInput) => createNotificationChannel(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.channelLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useUpdateNotificationChannel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: NotificationChannelUpdateInput }) =>
      updateNotificationChannel(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.channelLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.channelDetail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useDeleteNotificationChannel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: deleteNotificationChannel,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.channelLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useNotificationTemplates(filters: TemplateFilters) {
  return useQuery({
    queryKey: notificationKeys.templateList(filters),
    queryFn: () => getNotificationTemplates(filters),
  })
}

export function useNotificationTemplate(id: string | undefined) {
  return useQuery({
    queryKey: notificationKeys.templateDetail(id ?? ''),
    queryFn: () => getNotificationTemplate(id!),
    enabled: Boolean(id),
  })
}

export function useCreateNotificationTemplate() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: NotificationTemplateCreateInput) => createNotificationTemplate(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.templateLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useUpdateNotificationTemplate() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: NotificationTemplateUpdateInput }) =>
      updateNotificationTemplate(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.templateLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.templateDetail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useDeleteNotificationTemplate() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: deleteNotificationTemplate,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.templateLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useRenderNotificationTemplate() {
  return useMutation({
    mutationFn: (payload: NotificationRenderRequest) => renderNotificationTemplate(payload),
  })
}

export function useNotificationPreferences(params?: {
  user_id?: string
  person_id?: string
  page?: number
  page_size?: number
}) {
  return useQuery({
    queryKey: [...notificationKeys.preferences(), params],
    queryFn: () => getNotificationPreferences(params),
  })
}

export function useCreateNotificationPreference() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: NotificationPreferenceCreateInput) => createNotificationPreference(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.preferences() })
    },
  })
}

export function useUpdateNotificationPreference() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: NotificationPreferenceUpdateInput }) =>
      updateNotificationPreference(id, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.preferences() })
    },
  })
}

export function useDeleteNotificationPreference() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: deleteNotificationPreference,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.preferences() })
    },
  })
}

export function useNotificationMessages(filters: MessageFilters) {
  return useQuery({
    queryKey: notificationKeys.messageList(filters),
    queryFn: () => getNotificationMessages(filters),
  })
}

export function useNotificationMessage(id: string | undefined) {
  return useQuery({
    queryKey: notificationKeys.messageDetail(id ?? ''),
    queryFn: () => getNotificationMessage(id!),
    enabled: Boolean(id),
  })
}

export function useCreateNotificationMessage() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: NotificationMessageCreateInput) => createNotificationMessage(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.messageLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useUpdateNotificationMessage() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: NotificationMessageUpdateInput }) =>
      updateNotificationMessage(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.messageLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.messageDetail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useDeleteNotificationMessage() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: deleteNotificationMessage,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.messageLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useQueueNotificationMessage() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (messageId: string) => queueNotificationMessage(messageId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.messageLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
    },
  })
}

export function useSendNotificationMessage(messageId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: NotificationSendRequest) => sendNotificationMessage(messageId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: notificationKeys.messageDetail(messageId) })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.messageLists() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.deliveryAttempts(messageId) })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.deliveryAttempts() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.overview() })
      void queryClient.invalidateQueries({ queryKey: notificationKeys.all })
    },
  })
}

export function useMessageDeliveryAttempts(messageId: string | undefined) {
  return useQuery({
    queryKey: notificationKeys.deliveryAttempts(messageId),
    queryFn: () => getMessageDeliveryAttempts(messageId!),
    enabled: Boolean(messageId),
  })
}

export function useNotificationDeliveryAttempts(params?: { page?: number; page_size?: number }) {
  return useQuery({
    queryKey: notificationKeys.deliveryAttempts(),
    queryFn: () => getNotificationDeliveryAttempts(params),
  })
}

export function useEntityNotifications(entityType: string, entityId: string) {
  return useQuery({
    queryKey: notificationKeys.entity(entityType, entityId),
    queryFn: () => getEntityNotifications(entityType, entityId),
    enabled: Boolean(entityType && entityId),
  })
}
