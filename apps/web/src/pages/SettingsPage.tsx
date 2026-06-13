import { useSearchParams } from 'react-router-dom'

import { useTenancy } from '@/app/TenancyProvider'
import { PageHeader } from '@/components/ui/PageHeader'
import { CompanySettingsSection } from '@/features/settings/components/CompanySettingsSection'
import { NotificationsSettingsSection } from '@/features/settings/components/NotificationsSettingsSection'
import { OperationsSettingsSection } from '@/features/settings/components/OperationsSettingsSection'
import { SettingsOverviewSection } from '@/features/settings/components/SettingsOverviewSection'
import { SettingsSectionNav } from '@/features/settings/components/SettingsSectionNav'
import { UserSettingsSection } from '@/features/settings/components/UserSettingsSection'
import { WorkspaceSettingsSection } from '@/features/settings/components/WorkspaceSettingsSection'
import { parseSettingsSection } from '@/features/settings/types'
import { canManageCompanySettings } from '@/features/settings/utils'

export function SettingsPage() {
  const [searchParams] = useSearchParams()
  const section = parseSettingsSection(searchParams.get('section'))
  const { role } = useTenancy()
  const canManageCompany = canManageCompanySettings(role)

  return (
    <div>
      <PageHeader
        title="Settings"
        description="Manage company configuration, workspace defaults, operations, notifications, and account preferences."
      />
      <SettingsSectionNav activeSection={section} />
      {section === 'overview' ? <SettingsOverviewSection /> : null}
      {section === 'company' && canManageCompany ? <CompanySettingsSection /> : null}
      {section === 'workspace' ? <WorkspaceSettingsSection /> : null}
      {section === 'operations' ? <OperationsSettingsSection /> : null}
      {section === 'notifications' ? <NotificationsSettingsSection /> : null}
      {section === 'system' ? <UserSettingsSection /> : null}
    </div>
  )
}
