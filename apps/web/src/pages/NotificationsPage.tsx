import { useState } from 'react'
import { Link } from 'react-router-dom'

import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { DEFAULT_PAGE_SIZE } from '@/features/notifications/constants'
import { NotificationChannelForm } from '@/features/notifications/components/NotificationChannelForm'
import { NotificationChannelsTable } from '@/features/notifications/components/NotificationChannelsTable'
import { NotificationDeliveryAttemptsTable } from '@/features/notifications/components/NotificationDeliveryAttemptsTable'
import { NotificationMessagesTable } from '@/features/notifications/components/NotificationMessagesTable'
import { NotificationOverviewCards } from '@/features/notifications/components/NotificationOverviewCards'
import { NotificationPreferenceForm } from '@/features/notifications/components/NotificationPreferenceForm'
import { NotificationPreferencesTable } from '@/features/notifications/components/NotificationPreferencesTable'
import { NotificationTemplatesTable } from '@/features/notifications/components/NotificationTemplatesTable'
import {
  useCreateNotificationChannel,
  useCreateNotificationPreference,
  useDeleteNotificationChannel,
  useDeleteNotificationMessage,
  useDeleteNotificationTemplate,
  useNotificationChannels,
  useNotificationDeliveryAttempts,
  useNotificationMessages,
  useNotificationOverview,
  useNotificationPreferences,
  useNotificationTemplates,
  useQueueNotificationMessage,
  useUpdateNotificationChannel,
  useUpdateNotificationPreference,
} from '@/features/notifications/hooks'
import type { NotificationChannelListItem } from '@/features/notifications/types'
import { getApiErrorMessage } from '@/features/notifications/utils'

export function NotificationsPage() {
  const overviewQuery = useNotificationOverview()
  const channelsQuery = useNotificationChannels({ page: 1, page_size: DEFAULT_PAGE_SIZE })
  const templatesQuery = useNotificationTemplates({ page: 1, page_size: DEFAULT_PAGE_SIZE })
  const messagesQuery = useNotificationMessages({ page: 1, page_size: DEFAULT_PAGE_SIZE })
  const attemptsQuery = useNotificationDeliveryAttempts({ page: 1, page_size: 10 })
  const preferencesQuery = useNotificationPreferences({ page: 1, page_size: DEFAULT_PAGE_SIZE })

  const createChannelMutation = useCreateNotificationChannel()
  const updateChannelMutation = useUpdateNotificationChannel()
  const deleteChannelMutation = useDeleteNotificationChannel()
  const deleteTemplateMutation = useDeleteNotificationTemplate()
  const deleteMessageMutation = useDeleteNotificationMessage()
  const queueMessageMutation = useQueueNotificationMessage()
  const createPreferenceMutation = useCreateNotificationPreference()
  const updatePreferenceMutation = useUpdateNotificationPreference()

  const [showChannelForm, setShowChannelForm] = useState(false)
  const [editingChannel, setEditingChannel] = useState<NotificationChannelListItem | null>(null)
  const [showPreferenceForm, setShowPreferenceForm] = useState(false)
  const [actionError, setActionError] = useState<string | null>(null)

  const channelItems = (channelsQuery.data?.items ?? []) as NotificationChannelListItem[]

  return (
    <div className="space-y-8">
      <PageHeader
        title="Notifications"
        description="Manage notification channels, templates, messages and delivery history."
        actions={
          <PermissionGate require="editor">
            <div className="flex gap-2">
              <Link to="/notifications/templates/new">
                <Button>New Template</Button>
              </Link>
              <Link to="/notifications/messages/new">
                <Button variant="secondary">New Message</Button>
              </Link>
            </div>
          </PermissionGate>
        }
      />

      <NotificationOverviewCards
        overview={overviewQuery.data}
        isLoading={overviewQuery.isLoading}
        error={overviewQuery.error}
      />

      <Card>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <SectionHeader title="Channels" description="Outbound channel configuration (simulation-first MVP)." />
          <PermissionGate require="editor">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => {
                setEditingChannel(null)
                setShowChannelForm((current) => !current)
              }}
            >
              {showChannelForm ? 'Cancel' : 'New channel'}
            </Button>
          </PermissionGate>
        </div>
        {showChannelForm ? (
          <div className="mt-4">
            <NotificationChannelForm
              initial={editingChannel as never}
              isSubmitting={createChannelMutation.isPending || updateChannelMutation.isPending}
              submitError={actionError}
              onCancel={() => {
                setShowChannelForm(false)
                setEditingChannel(null)
              }}
              onSubmit={async (payload) => {
                setActionError(null)
                try {
                  if (editingChannel) {
                    await updateChannelMutation.mutateAsync({ id: editingChannel.id, payload })
                  } else {
                    await createChannelMutation.mutateAsync(payload)
                  }
                  setShowChannelForm(false)
                  setEditingChannel(null)
                } catch (error) {
                  setActionError(getApiErrorMessage(error))
                }
              }}
            />
          </div>
        ) : null}
        <div className="mt-4">
          <NotificationChannelsTable
            items={channelItems}
            onEdit={(item) => {
              setEditingChannel(item)
              setShowChannelForm(true)
            }}
            onDelete={async (item) => {
              if (!window.confirm(`Delete channel "${item.name}"?`)) return
              try {
                await deleteChannelMutation.mutateAsync(item.id)
              } catch (error) {
                setActionError(getApiErrorMessage(error))
              }
            }}
          />
        </div>
      </Card>

      <Card>
        <SectionHeader title="Templates" description="Reusable notification content with simple placeholders." />
        <div className="mt-4">
          <NotificationTemplatesTable
            items={templatesQuery.data?.items ?? []}
            onDelete={async (item) => {
              if (!window.confirm(`Delete template "${item.name}"?`)) return
              try {
                await deleteTemplateMutation.mutateAsync(item.id)
              } catch (error) {
                setActionError(getApiErrorMessage(error))
              }
            }}
          />
        </div>
      </Card>

      <Card>
        <SectionHeader title="Messages" description="Notification records and delivery state." />
        <div className="mt-4">
          <NotificationMessagesTable
            items={messagesQuery.data?.items ?? []}
            onQueue={async (item) => {
              try {
                await queueMessageMutation.mutateAsync(item.id)
              } catch (error) {
                setActionError(getApiErrorMessage(error))
              }
            }}
            onDelete={async (item) => {
              if (!window.confirm('Delete this notification message?')) return
              try {
                await deleteMessageMutation.mutateAsync(item.id)
              } catch (error) {
                setActionError(getApiErrorMessage(error))
              }
            }}
          />
        </div>
      </Card>

      <Card>
        <SectionHeader title="Recent delivery attempts" description="Latest simulation and delivery history." />
        <div className="mt-4">
          <NotificationDeliveryAttemptsTable items={attemptsQuery.data?.items ?? []} />
        </div>
      </Card>

      <Card>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <SectionHeader title="Preferences" description="Per-user notification preferences (basic MVP)." />
          <PermissionGate require="editor">
            <Button variant="secondary" size="sm" onClick={() => setShowPreferenceForm((c) => !c)}>
              {showPreferenceForm ? 'Cancel' : 'Add preference'}
            </Button>
          </PermissionGate>
        </div>
        {showPreferenceForm ? (
          <div className="mt-4">
            <NotificationPreferenceForm
              isSubmitting={createPreferenceMutation.isPending}
              submitError={actionError}
              onSubmit={async (payload) => {
                setActionError(null)
                try {
                  await createPreferenceMutation.mutateAsync(payload)
                  setShowPreferenceForm(false)
                } catch (error) {
                  setActionError(getApiErrorMessage(error))
                }
              }}
            />
          </div>
        ) : null}
        <div className="mt-4">
          <NotificationPreferencesTable
            items={preferencesQuery.data ?? []}
            onToggle={async (item) => {
              try {
                await updatePreferenceMutation.mutateAsync({
                  id: item.id,
                  payload: { is_enabled: !item.is_enabled },
                })
              } catch (error) {
                setActionError(getApiErrorMessage(error))
              }
            }}
          />
        </div>
      </Card>

      <Card>
        <SectionHeader
          title="Future capabilities"
          description="Planned notification features not yet available in MVP."
        />
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-gray-600">
          <li>Real email delivery</li>
          <li>Teams and Slack providers</li>
          <li>Notification preferences engine</li>
          <li>Background delivery worker</li>
        </ul>
      </Card>

      {actionError ? <p className="text-sm text-status-danger">{actionError}</p> : null}
    </div>
  )
}
