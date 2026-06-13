import { SETTINGS_SECTIONS, type SettingsSectionDefinition } from '@/features/settings/types'

function canManageCompany(role: string | null | undefined): boolean {
  return role === 'owner' || role === 'admin'
}

export function getVisibleSettingsSections(
  role: string | null | undefined,
): SettingsSectionDefinition[] {
  return SETTINGS_SECTIONS.filter((section) => {
    if (section.id === 'company') {
      return canManageCompany(role)
    }
    return true
  })
}

export function canManageCompanySettings(role: string | null | undefined): boolean {
  return canManageCompany(role)
}
