import { useSearchParams } from 'react-router-dom'

import { PageHeader } from '@/components/ui/PageHeader'
import { CompanySettingsSection } from '@/features/settings/components/CompanySettingsSection'
import { SettingsSectionNav } from '@/features/settings/components/SettingsSectionNav'
import { UserSettingsSection } from '@/features/settings/components/UserSettingsSection'
import { WorkspaceSettingsSection } from '@/features/settings/components/WorkspaceSettingsSection'
import { parseSettingsSection } from '@/features/settings/types'

export function SettingsPage() {
  const [searchParams] = useSearchParams()
  const section = parseSettingsSection(searchParams.get('section'))

  return (
    <div>
      <PageHeader
        title="Settings"
        description="Manage your user profile, workspace defaults, and company configuration."
      />
      <SettingsSectionNav activeSection={section} />
      {section === 'user' ? <UserSettingsSection /> : null}
      {section === 'workspace' ? <WorkspaceSettingsSection /> : null}
      {section === 'company' ? <CompanySettingsSection /> : null}
    </div>
  )
}
