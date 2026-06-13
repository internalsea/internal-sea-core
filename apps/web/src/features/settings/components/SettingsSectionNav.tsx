import { Link, useSearchParams } from 'react-router-dom'

import { useTenancy } from '@/app/TenancyProvider'
import { type SettingsSection } from '@/features/settings/types'
import { getVisibleSettingsSections } from '@/features/settings/utils'
import { cn } from '@/lib/utils'

interface SettingsSectionNavProps {
  activeSection: SettingsSection
}

export function SettingsSectionNav({ activeSection }: SettingsSectionNavProps) {
  const [searchParams] = useSearchParams()
  const { role } = useTenancy()

  const visibleSections = getVisibleSettingsSections(role)

  const sections: Array<{ id: SettingsSection; label: string }> = [
    { id: 'overview', label: 'Overview' },
    ...visibleSections.map((section) => ({ id: section.id, label: section.label })),
  ]

  return (
    <nav
      aria-label="Settings sections"
      className="mb-6 flex flex-wrap gap-1 border-b border-app-border"
    >
      {sections.map((section) => {
        const params = new URLSearchParams(searchParams)
        if (section.id === 'overview') {
          params.delete('section')
        } else {
          params.set('section', section.id)
        }
        const isActive = activeSection === section.id

        return (
          <Link
            key={section.id}
            to={section.id === 'overview' ? '/settings' : `/settings?${params.toString()}`}
            className={cn(
              '-mb-px border-b-2 px-4 py-2.5 text-sm font-medium transition-colors',
              isActive
                ? 'border-core-blue text-core-blue'
                : 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-900',
            )}
          >
            {section.label}
          </Link>
        )
      })}
    </nav>
  )
}
