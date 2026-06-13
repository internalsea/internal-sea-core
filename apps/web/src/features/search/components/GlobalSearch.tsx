import { useEffect, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from 'react'
import { useNavigate } from 'react-router-dom'

import { SearchResultsDropdown } from '@/features/search/components/SearchResultsDropdown'
import { useGlobalSearch } from '@/features/search/hooks'
import type { SearchResult } from '@/features/search/types'
import { useDebouncedValue } from '@/lib/hooks'
import { cn } from '@/lib/utils'

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }
  return 'Search is unavailable.'
}

interface GlobalSearchProps {
  variant?: 'light' | 'dark'
}

export function GlobalSearch({ variant = 'light' }: GlobalSearchProps) {
  const navigate = useNavigate()
  const containerRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const [query, setQuery] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const debouncedQuery = useDebouncedValue(query, 280)

  const searchQuery = useGlobalSearch(debouncedQuery, {
    enabled: isOpen,
    limit: 20,
  })

  useEffect(() => {
    function handlePointerDown(event: MouseEvent) {
      if (!containerRef.current?.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    function handleEscape(event: globalThis.KeyboardEvent) {
      if (event.key === 'Escape') {
        setIsOpen(false)
        inputRef.current?.blur()
      }
    }

    document.addEventListener('mousedown', handlePointerDown)
    document.addEventListener('keydown', handleEscape)
    return () => {
      document.removeEventListener('mousedown', handlePointerDown)
      document.removeEventListener('keydown', handleEscape)
    }
  }, [])

  function handleSelect(result: SearchResult) {
    setIsOpen(false)
    setQuery('')
    navigate(result.url)
  }

  function handleKeyDown(event: ReactKeyboardEvent<HTMLInputElement>) {
    if (event.key === 'Enter' && searchQuery.data?.items[0]) {
      event.preventDefault()
      handleSelect(searchQuery.data.items[0])
    }
  }

  const showDropdown = isOpen && query.trim().length > 0

  return (
    <div ref={containerRef} className="relative w-full max-w-xl">
      <input
        ref={inputRef}
        type="search"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onFocus={() => setIsOpen(true)}
        onKeyDown={handleKeyDown}
        placeholder="Search products, work, people..."
        aria-label="Global search"
        aria-expanded={showDropdown}
        aria-controls="global-search-results"
        className={cn(
          'block h-9 w-full rounded-md border px-3 text-sm focus:outline-none focus:ring-1 focus:ring-core-blue',
          variant === 'dark'
            ? 'border-white/15 bg-white/10 text-white placeholder:text-gray-400 focus:border-white/30'
            : 'border-app-borderStrong bg-app-surface text-gray-900 placeholder:text-gray-400 focus:border-core-blue',
        )}
      />

      {showDropdown ? (
        <div
          id="global-search-results"
          className="absolute left-0 right-0 top-[calc(100%+0.5rem)] z-50 overflow-hidden rounded-xl border border-app-border bg-app-surface shadow-sm"
        >
          <SearchResultsDropdown
            query={query}
            results={searchQuery.data?.items ?? []}
            isLoading={searchQuery.isLoading}
            error={searchQuery.isError ? getErrorMessage(searchQuery.error) : null}
            onSelect={handleSelect}
          />
        </div>
      ) : null}
    </div>
  )
}
