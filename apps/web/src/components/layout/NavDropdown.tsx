import { useEffect, useId, useRef, useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'

import type { PrimaryNavGroup } from '@/lib/navigation'
import { isNavGroupActive, pathMatches } from '@/lib/navigation'
import { cn } from '@/lib/utils'

interface NavDropdownProps {
  group: PrimaryNavGroup
}

export function NavDropdown({ group }: NavDropdownProps) {
  const location = useLocation()
  const menuId = useId()
  const containerRef = useRef<HTMLDivElement>(null)
  const [isOpen, setIsOpen] = useState(false)
  const isActive = isNavGroupActive(location.pathname, group)
  const isSingleItem = group.items.length === 1

  useEffect(() => {
    function handlePointerDown(event: MouseEvent) {
      if (!containerRef.current?.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    function handleEscape(event: globalThis.KeyboardEvent) {
      if (event.key === 'Escape') {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handlePointerDown)
    document.addEventListener('keydown', handleEscape)
    return () => {
      document.removeEventListener('mousedown', handlePointerDown)
      document.removeEventListener('keydown', handleEscape)
    }
  }, [])

  useEffect(() => {
    setIsOpen(false)
  }, [location.pathname])

  if (isSingleItem) {
    const item = group.items[0]
    return (
      <NavLink
        to={item.path}
        className={({ isActive: linkActive }) =>
          cn(
            'rounded-md px-3 py-2 text-sm font-medium transition-colors',
            linkActive || pathMatches(location.pathname, item.path)
              ? 'bg-white/10 text-white'
              : 'text-gray-300 hover:bg-white/5 hover:text-white',
          )
        }
      >
        {group.label}
      </NavLink>
    )
  }

  return (
    <div ref={containerRef} className="relative">
      <button
        type="button"
        aria-expanded={isOpen}
        aria-haspopup="menu"
        aria-controls={menuId}
        onClick={() => setIsOpen((open) => !open)}
        className={cn(
          'inline-flex items-center gap-1 rounded-md px-3 py-2 text-sm font-medium transition-colors',
          isActive
            ? 'bg-white/10 text-white'
            : 'text-gray-300 hover:bg-white/5 hover:text-white',
        )}
      >
        {group.label}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          aria-hidden="true"
          className={cn('h-4 w-4 transition-transform', isOpen ? 'rotate-180' : '')}
        >
          <path
            fillRule="evenodd"
            d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.94a.75.75 0 111.08 1.04l-4.24 4.5a.75.75 0 01-1.08 0l-4.24-4.5a.75.75 0 01.02-1.06z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {isOpen ? (
        <div
          id={menuId}
          role="menu"
          className="absolute left-0 top-[calc(100%+0.5rem)] z-50 min-w-[12rem] overflow-hidden rounded-lg border border-white/10 bg-core-navy py-1 shadow-lg"
        >
          {group.items.map((item) => (
            <NavLink
              key={`${item.path}-${item.label}`}
              to={item.path}
              role="menuitem"
              className={({ isActive: linkActive }) =>
                cn(
                  'block px-4 py-2 text-sm transition-colors',
                  linkActive || pathMatches(location.pathname, item.path)
                    ? 'bg-white/10 font-medium text-white'
                    : 'text-gray-300 hover:bg-white/5 hover:text-white',
                )
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      ) : null}
    </div>
  )
}
