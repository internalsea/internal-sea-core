import type {
  NotificationChannelCreateInput,
  NotificationChannelType,
  NotificationMessageCreateInput,
  NotificationPreferenceCreateInput,
  NotificationTemplateCreateInput,
} from '@/features/notifications/types'

const SECRET_KEY_PATTERN = /(token|secret|password|api[_-]?key)/i

export function formatDateTime(value: string | null | undefined): string {
  if (!value) return '—'
  return new Date(value).toLocaleString()
}

export function formatChannelType(value: string): string {
  return value.replace(/_/g, ' ')
}

export function formatMessageStatus(value: string): string {
  return value.replace(/_/g, ' ')
}

export function formatPriority(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1)
}

export function parseJsonField(value: string): Record<string, unknown> | null {
  const trimmed = value.trim()
  if (!trimmed) return null
  return JSON.parse(trimmed) as Record<string, unknown>
}

export function stringifyJsonField(value: Record<string, unknown> | null | undefined): string {
  if (!value) return ''
  return JSON.stringify(value, null, 2)
}

export function rejectSecretKeys(config: Record<string, unknown> | null | undefined): void {
  if (!config) return
  for (const key of Object.keys(config)) {
    if (SECRET_KEY_PATTERN.test(key)) {
      throw new Error(
        `provider_config must not contain secret-like keys (found: ${key}). Use environment variables instead.`,
      )
    }
  }
}

export function cleanChannelPayload(
  values: NotificationChannelCreateInput,
): NotificationChannelCreateInput {
  rejectSecretKeys(values.provider_config ?? null)
  return {
    ...values,
    name: values.name.trim(),
    description: values.description?.trim() || null,
    endpoint_url: values.endpoint_url?.trim() || null,
    default_recipient: values.default_recipient?.trim() || null,
  }
}

export function cleanTemplatePayload(
  values: NotificationTemplateCreateInput,
): NotificationTemplateCreateInput {
  return {
    ...values,
    name: values.name.trim(),
    body_template: values.body_template.trim(),
    description: values.description?.trim() || null,
    subject_template: values.subject_template?.trim() || null,
  }
}

export function cleanMessagePayload(
  values: NotificationMessageCreateInput,
): NotificationMessageCreateInput {
  return {
    ...values,
    body: values.body.trim(),
    subject: values.subject?.trim() || null,
    recipient_value: values.recipient_value?.trim() || null,
  }
}

export function cleanPreferencePayload(
  values: NotificationPreferenceCreateInput,
): NotificationPreferenceCreateInput {
  return values
}

export function getNotificationEntityHref(
  entityType: string | null | undefined,
  entityId: string | null | undefined,
): string | null {
  if (!entityType || !entityId) return null
  const routes: Record<string, string> = {
    data_product: `/data-products/${entityId}`,
    work_item: `/work-items/${entityId}`,
    project: `/projects/${entityId}`,
    internal_project: `/internal-projects/${entityId}`,
    person: `/people/${entityId}`,
    team: `/teams/${entityId}`,
    capability: `/capabilities/${entityId}`,
    compliance_check: `/compliance/checks/${entityId}`,
  }
  return routes[entityType] ?? null
}

export function isExternalChannelType(channelType: NotificationChannelType | string): boolean {
  return channelType !== 'in_app'
}

export function canSendRealInMvp(channelType: NotificationChannelType | string | null): boolean {
  return channelType === 'in_app'
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message
  return 'An unexpected error occurred'
}
