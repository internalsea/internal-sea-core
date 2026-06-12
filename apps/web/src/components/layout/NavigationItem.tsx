import { NavLink } from 'react-router-dom'

import { cn } from '@/lib/utils'

interface NavigationItemProps {
  label: string
  path: string
}

export function NavigationItem({ label, path }: NavigationItemProps) {
  return (
    <NavLink
      to={path}
      className={({ isActive }) =>
        cn(
          'block rounded-md px-3 py-2 text-sm text-gray-300 transition-colors',
          isActive
            ? 'bg-white/10 font-medium text-white'
            : 'hover:bg-gray-800 hover:text-white',
        )
      }
    >
      {label}
    </NavLink>
  )
}
