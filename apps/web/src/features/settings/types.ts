export type SettingsSection =
  | 'overview'
  | 'company'
  | 'workspace'
  | 'operations'
  | 'notifications'
  | 'system'

export interface SettingsSectionDefinition {
  id: SettingsSection
  label: string
  title: string
  description: string
}

export const SETTINGS_SECTIONS: SettingsSectionDefinition[] = [
  {
    id: 'company',
    label: 'Company',
    title: 'Company',
    description: 'Organization-level configuration, company profile, structure, and default rules.',
  },
  {
    id: 'workspace',
    label: 'Workspace',
    title: 'Workspace',
    description: 'Workspace preferences and team or workspace-level defaults.',
  },
  {
    id: 'operations',
    label: 'Operations',
    title: 'Operations',
    description: 'Operational configuration and supporting workflows.',
  },
  {
    id: 'notifications',
    label: 'Notifications',
    title: 'Notifications',
    description: 'Notification preferences, rules, and delivery or channel settings.',
  },
  {
    id: 'system',
    label: 'System',
    title: 'System',
    description: 'General settings and access or configuration options for your account.',
  },
]

export function parseSettingsSection(value: string | null): SettingsSection {
  if (
    value === 'company' ||
    value === 'workspace' ||
    value === 'operations' ||
    value === 'notifications' ||
    value === 'system'
  ) {
    return value
  }
  if (value === 'user') {
    return 'system'
  }
  return 'overview'
}
