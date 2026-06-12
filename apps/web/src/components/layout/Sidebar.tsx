import { APP_NAME } from '@/lib/config'
import { navigationGroups } from '@/lib/navigation'
import { NavigationItem } from '@/components/layout/NavigationItem'

export function Sidebar() {
  return (
    <aside className="flex h-full w-sidebar shrink-0 flex-col bg-core-navy">
      <div className="border-b border-white/10 px-5 py-4">
        <h1 className="text-base font-semibold text-white">{APP_NAME}</h1>
        <p className="mt-0.5 text-xs text-gray-500">Core</p>
      </div>
      <nav className="flex-1 overflow-y-auto px-3 py-4">
        {navigationGroups.map((group) => (
          <div key={group.title} className="mb-6">
            <p className="mb-2 px-3 text-xs font-medium uppercase tracking-wide text-gray-500">
              {group.title}
            </p>
            <div className="space-y-0.5">
              {group.items.map((item) => (
                <NavigationItem key={item.path} label={item.label} path={item.path} />
              ))}
            </div>
          </div>
        ))}
      </nav>
    </aside>
  )
}
