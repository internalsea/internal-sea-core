export type SettingsSection = 'user' | 'workspace' | 'company'

export const SETTINGS_SECTIONS: { id: SettingsSection; label: string }[] = [
  { id: 'user', label: 'User' },
  { id: 'workspace', label: 'Workspace' },
  { id: 'company', label: 'Company' },
]

export function parseSettingsSection(value: string | null): SettingsSection {
  if (value === 'workspace' || value === 'company') {
    return value
  }
  return 'user'
}
