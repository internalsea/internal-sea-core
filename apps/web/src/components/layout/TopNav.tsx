import { AppBrand } from '@/components/layout/AppBrand'
import { NavDropdown } from '@/components/layout/NavDropdown'
import { primaryNavGroups } from '@/lib/navigation'

export function TopNav() {
  return (
    <div className="flex min-w-0 flex-1 items-center gap-6 lg:gap-8">
      <AppBrand />

      <nav
        aria-label="Primary"
        className="flex min-w-0 flex-1 items-center gap-1 overflow-x-auto pb-1 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
      >
        {primaryNavGroups.map((group) => (
          <NavDropdown key={group.id} group={group} />
        ))}
      </nav>
    </div>
  )
}
