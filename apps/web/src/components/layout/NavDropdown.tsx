import { useEffect, useId, useLayoutEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { NavLink, useLocation } from 'react-router-dom'

import type { PrimaryNavGroup } from '@/lib/navigation'
import { isNavGroupActive, pathMatches } from '@/lib/navigation'
import { cn } from '@/lib/utils'

const navLinkActiveClass = 'bg-auth-surface font-medium text-gray-900'
const navLinkClass = 'text-gray-700 hover:bg-auth-surface/80 hover:text-gray-900'
const navButtonActiveClass = 'bg-auth-surface text-gray-900'
const navButtonClass = 'text-gray-700 hover:bg-auth-surface/80 hover:text-gray-900'
const menuPanelClass =
  'fixed z-[100] min-w-[12rem] overflow-hidden rounded-lg border border-auth-surfaceBorder bg-auth-surface py-1 shadow-lg'

interface NavDropdownProps {
  group: PrimaryNavGroup
}

interface MenuPosition {
  top: number
  left: number
}

function getMenuPosition(button: HTMLButtonElement): MenuPosition {
  const rect = button.getBoundingClientRect()
  return {
    top: rect.bottom + 8,
    left: rect.left,
  }
}

export function NavDropdown({ group }: NavDropdownProps) {
  const location = useLocation()
  const menuId = useId()
  const containerRef = useRef<HTMLDivElement>(null)
  const buttonRef = useRef<HTMLButtonElement>(null)
  const menuRef = useRef<HTMLDivElement>(null)
  const [isOpen, setIsOpen] = useState(false)
  const [menuPosition, setMenuPosition] = useState<MenuPosition>({ top: 0, left: 0 })
  const isActive = isNavGroupActive(location.pathname, group)
  const isSingleItem = group.items.length === 1

  useLayoutEffect(() => {
    if (!isOpen || !buttonRef.current) {
      return
    }

    function updatePosition() {
      if (buttonRef.current) {
        setMenuPosition(getMenuPosition(buttonRef.current))
      }
    }

    updatePosition()
    window.addEventListener('resize', updatePosition)
    window.addEventListener('scroll', updatePosition, true)
    return () => {
      window.removeEventListener('resize', updatePosition)
      window.removeEventListener('scroll', updatePosition, true)
    }
  }, [isOpen])

  useEffect(() => {
    function handlePointerDown(event: MouseEvent) {
      const target = event.target as Node
      if (containerRef.current?.contains(target) || menuRef.current?.contains(target)) {
        return
      }
      setIsOpen(false)
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
              ? navLinkActiveClass
              : navLinkClass,
          )
        }
      >
        {group.label}
      </NavLink>
    )
  }

  const menu = isOpen
    ? createPortal(
        <div
          id={menuId}
          ref={menuRef}
          role="menu"
          style={{ top: menuPosition.top, left: menuPosition.left }}
          className={menuPanelClass}
        >
          {group.items.map((item) => (
            <NavLink
              key={`${item.path}-${item.label}`}
              to={item.path}
              role="menuitem"
              onClick={() => setIsOpen(false)}
              className={({ isActive: linkActive }) =>
                cn(
                  'block px-4 py-2 text-sm transition-colors',
                  linkActive || pathMatches(location.pathname, item.path)
                    ? navLinkActiveClass
                    : navLinkClass,
                )
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>,
        document.body,
      )
    : null

  return (
    <div ref={containerRef} className="relative shrink-0">
      <button
        ref={buttonRef}
        type="button"
        aria-expanded={isOpen}
        aria-haspopup="menu"
        aria-controls={menuId}
        onClick={() => setIsOpen((open) => !open)}
        className={cn(
          'inline-flex items-center gap-1 rounded-md px-3 py-2 text-sm font-medium transition-colors',
          isActive ? navButtonActiveClass : navButtonClass,
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
      {menu}
    </div>
  )
}
