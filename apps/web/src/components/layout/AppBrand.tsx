import { Link } from 'react-router-dom'

import { useTenancy } from '@/app/TenancyProvider'
import { BrandLogoMark } from '@/components/layout/BrandLogoMark'
import { APP_NAME } from '@/lib/config'
import { cn } from '@/lib/utils'

export function AppBrand() {
  const { company, isLoading } = useTenancy()

  const organizationSubtitle = isLoading
    ? 'Loading…'
    : company
      ? `of ${company.name}`
      : 'of —'

  return (
    <Link
      to="/dashboard"
      className={cn(
        'group flex shrink-0 items-center gap-2.5 rounded-lg px-1.5 py-1 transition-colors',
        'hover:bg-auth-surface/70',
      )}
      aria-label={`${APP_NAME}, ${organizationSubtitle}`}
    >
      <BrandLogoMark className="transition-transform group-hover:scale-[1.02]" />
      <div className="min-w-0 leading-none">
        <span className="block truncate text-[15px] font-bold tracking-tight text-core-navy sm:text-base">
          {APP_NAME}
        </span>
        <span className="mt-0.5 block max-w-[9rem] truncate text-[13px] font-normal text-gray-600 sm:max-w-[11rem]">
          {organizationSubtitle}
        </span>
      </div>
    </Link>
  )
}
