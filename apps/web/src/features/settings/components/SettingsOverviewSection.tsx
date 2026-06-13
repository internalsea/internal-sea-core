import { Link } from 'react-router-dom'

import { useTenancy } from '@/app/TenancyProvider'
import { Card } from '@/components/ui/Card'
import { getVisibleSettingsSections } from '@/features/settings/utils'
import type { SettingsSectionDefinition } from '@/features/settings/types'

function SettingsSectionCard({ section }: { section: SettingsSectionDefinition }) {
  return (
    <Card className="flex h-full flex-col">
      <h3 className="text-base font-semibold text-gray-900">{section.title}</h3>
      <p className="mt-2 flex-1 text-sm text-gray-600">{section.description}</p>
      <Link
        to={`/settings?section=${section.id}`}
        className="mt-4 inline-flex text-sm font-medium text-core-blue hover:text-core-blueHover"
      >
        Open {section.label.toLowerCase()} settings
      </Link>
    </Card>
  )
}

export function SettingsOverviewSection() {
  const { role } = useTenancy()
  const sections = getVisibleSettingsSections(role)

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {sections.map((section) => (
        <SettingsSectionCard key={section.id} section={section} />
      ))}
    </div>
  )
}
