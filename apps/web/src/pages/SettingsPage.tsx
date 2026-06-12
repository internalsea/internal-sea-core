import { ModulePlaceholder } from '@/components/common/ModulePlaceholder'

export function SettingsPage() {
  return (
    <ModulePlaceholder
      title="Settings"
      description="Application preferences and environment configuration."
    >
      <p className="text-sm text-slate-600">
        Authentication, user profile and organization settings will be added later.
      </p>
    </ModulePlaceholder>
  )
}
