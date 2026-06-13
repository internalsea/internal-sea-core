import { useEffect, useId, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import { PlusIcon } from '@/components/icons/PlusIcon'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { createActionLinks } from '@/lib/navigation'
import { cn } from '@/lib/utils'

export function CreateActionMenu() {
  const menuId = useId()
  const containerRef = useRef<HTMLDivElement>(null)
  const [isOpen, setIsOpen] = useState(false)

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

  return (
    <PermissionGate require="editor">
      <div ref={containerRef} className="relative">
        <Button
          type="button"
          size="sm"
          aria-expanded={isOpen}
          aria-haspopup="menu"
          aria-controls={menuId}
          onClick={() => setIsOpen((open) => !open)}
          className="gap-1.5"
        >
          <PlusIcon />
          Create
        </Button>

        {isOpen ? (
          <div
            id={menuId}
            role="menu"
            className="absolute right-0 top-[calc(100%+0.5rem)] z-50 min-w-[12rem] overflow-hidden rounded-lg border border-app-border bg-app-surface py-1 shadow-lg"
          >
            {createActionLinks.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                role="menuitem"
                onClick={() => setIsOpen(false)}
                className={cn(
                  'block px-4 py-2 text-sm text-gray-700 transition-colors hover:bg-app-muted',
                )}
              >
                {item.label}
              </Link>
            ))}
          </div>
        ) : null}
      </div>
    </PermissionGate>
  )
}
