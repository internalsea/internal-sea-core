import { Link, useSearchParams } from 'react-router-dom'

import { SETTINGS_SECTIONS, type SettingsSection } from '@/features/settings/types'
import { cn } from '@/lib/utils'

interface SettingsSectionNavProps {
  activeSection: SettingsSection
}

export function SettingsSectionNav({ activeSection }: SettingsSectionNavProps) {
  const [searchParams] = useSearchParams()

  return (
    <nav
      aria-label="Settings sections"
      className="mb-6 flex flex-wrap gap-1 border-b border-app-border"
    >
      {SETTINGS_SECTIONS.map((section) => {
        const params = new URLSearchParams(searchParams)
        params.set('section', section.id)
        const isActive = activeSection === section.id

        return (
          <Link
            key={section.id}
            to={`/settings?${params.toString()}`}
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
