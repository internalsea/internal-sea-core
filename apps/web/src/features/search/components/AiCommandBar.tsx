import {
  useCallback,
  useEffect,
  useId,
  useRef,
  useState,
  type FormEvent,
  type KeyboardEvent as ReactKeyboardEvent,
} from 'react'
import { createPortal } from 'react-dom'
import { useNavigate } from 'react-router-dom'

import { ArrowUpIcon } from '@/components/icons/ArrowUpIcon'
import { SparklesIcon } from '@/components/icons/SparklesIcon'
import { useCanWrite } from '@/features/auth/hooks'
import {
  COMMAND_HINT_CHIPS,
  COMMAND_QUICK_ACTIONS,
  COMMAND_SUGGESTED_PROMPTS,
  isMacPlatform,
  type CommandQuickAction,
} from '@/features/search/commandBarConfig'
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

function canAccessAction(action: CommandQuickAction, canWrite: boolean): boolean {
  if (action.require === 'editor') {
    return canWrite
  }
  return true
}

export function AiCommandBar() {
  const navigate = useNavigate()
  const canWrite = useCanWrite()
  const panelId = useId()
  const inputRef = useRef<HTMLInputElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [isExpanded, setIsExpanded] = useState(false)
  const [query, setQuery] = useState('')
  const [showAiPlaceholder, setShowAiPlaceholder] = useState(false)
  const debouncedQuery = useDebouncedValue(query, 280)
  const keyboardShortcut = isMacPlatform() ? '⌘ K' : 'Ctrl K'

  const searchQuery = useGlobalSearch(debouncedQuery, {
    enabled: isExpanded,
    limit: 20,
  })

  const openPanel = useCallback(() => {
    setIsExpanded(true)
  }, [])

  const closePanel = useCallback(() => {
    setIsExpanded(false)
    setShowAiPlaceholder(false)
    inputRef.current?.blur()
  }, [])

  useEffect(() => {
    if (!isExpanded) {
      return
    }

    const frame = window.requestAnimationFrame(() => {
      inputRef.current?.focus()
    })

    return () => window.cancelAnimationFrame(frame)
  }, [isExpanded])

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      const modifierPressed = isMacPlatform() ? event.metaKey : event.ctrlKey
      if (modifierPressed && event.key.toLowerCase() === 'k') {
        event.preventDefault()
        setIsExpanded((open) => {
          if (open) {
            inputRef.current?.focus()
          }
          return true
        })
        return
      }

      if (event.key === 'Escape' && isExpanded) {
        event.preventDefault()
        closePanel()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [closePanel, isExpanded])

  useEffect(() => {
    if (!isExpanded) {
      return
    }

    function handlePointerDown(event: MouseEvent) {
      const target = event.target as Node
      if (containerRef.current?.contains(target)) {
        return
      }
      closePanel()
    }

    document.addEventListener('mousedown', handlePointerDown)
    return () => document.removeEventListener('mousedown', handlePointerDown)
  }, [closePanel, isExpanded])

  function handleSelect(result: SearchResult) {
    closePanel()
    setQuery('')
    navigate(result.url)
  }

  function handleSubmit(event?: FormEvent | ReactKeyboardEvent<HTMLInputElement>) {
    event?.preventDefault()
    const trimmedQuery = query.trim()

    if (searchQuery.data?.items[0]) {
      handleSelect(searchQuery.data.items[0])
      return
    }

    if (trimmedQuery.length >= 2) {
      setShowAiPlaceholder(true)
    }
  }

  function handleInputKeyDown(event: ReactKeyboardEvent<HTMLInputElement>) {
    if (event.key === 'Enter') {
      handleSubmit(event)
    }
  }

  function handlePromptSelect(prompt: string) {
    setQuery(prompt)
    setShowAiPlaceholder(true)
    openPanel()
  }

  function handleChipSelect(chipQuery: string) {
    setQuery(chipQuery)
    setShowAiPlaceholder(false)
    openPanel()
  }

  const trimmedQuery = query.trim()
  const showSearchResults = trimmedQuery.length > 0
  const visibleActions = COMMAND_QUICK_ACTIONS.filter((action) => canAccessAction(action, canWrite))

  return createPortal(
    <>
      {isExpanded ? (
        <div
          className="fixed inset-0 z-40 bg-core-navy/10 backdrop-blur-[1px]"
          aria-hidden="true"
        />
      ) : null}

      <div
        ref={containerRef}
        className={cn(
          'pointer-events-none fixed left-1/2 z-50 w-[calc(100vw-24px)] max-w-[880px] -translate-x-1/2',
          'bottom-3 sm:bottom-6',
        )}
      >
        {isExpanded ? (
          <div
            id={panelId}
            role="dialog"
            aria-modal="true"
            aria-label="Internal Sea AI command palette"
            className="pointer-events-auto mb-3 overflow-hidden rounded-[22px] border border-auth-surfaceBorder bg-app-surface shadow-[0_20px_50px_-12px_rgb(17_24_39_/_0.22)]"
          >
            <div className="border-b border-app-border px-4 py-3 sm:px-5">
              <p className="text-sm font-semibold text-gray-900">Ask Internal Sea</p>
              <p className="mt-0.5 text-xs text-gray-500">
                Search your workspace or use suggested prompts. AI responses are coming soon.
              </p>
            </div>

            <div className="max-h-[min(52vh,420px)] overflow-y-auto">
              <div className="border-b border-app-border px-4 py-3 sm:px-5">
                <p className="mb-2 text-xs font-medium uppercase tracking-wide text-gray-500">
                  Quick actions
                </p>
                <div className="grid gap-2 sm:grid-cols-2">
                  {visibleActions.map((action) => (
                    <button
                      key={action.path + action.label}
                      type="button"
                      onClick={() => {
                        closePanel()
                        setQuery('')
                        navigate(action.path)
                      }}
                      className="rounded-xl border border-app-border bg-auth-input/60 px-3 py-2.5 text-left transition-colors hover:border-auth-inputBorder hover:bg-auth-surface"
                    >
                      <span className="block text-sm font-medium text-gray-900">{action.label}</span>
                      {action.description ? (
                        <span className="mt-0.5 block text-xs text-gray-500">{action.description}</span>
                      ) : null}
                    </button>
                  ))}
                </div>
              </div>

              <div className="border-b border-app-border px-4 py-3 sm:px-5">
                <p className="mb-2 text-xs font-medium uppercase tracking-wide text-gray-500">
                  Suggested prompts
                </p>
                <div className="flex flex-wrap gap-2">
                  {COMMAND_SUGGESTED_PROMPTS.map((prompt) => (
                    <button
                      key={prompt}
                      type="button"
                      onClick={() => handlePromptSelect(prompt)}
                      className="rounded-full border border-app-border bg-app-surface px-3 py-1.5 text-xs text-gray-700 transition-colors hover:border-auth-inputBorder hover:bg-auth-input"
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>

              {showAiPlaceholder &&
              trimmedQuery.length >= 2 &&
              !searchQuery.isLoading &&
              (searchQuery.data?.items.length ?? 0) === 0 ? (
                <div className="border-b border-app-border px-4 py-4 sm:px-5">
                  <p className="text-sm text-gray-700">
                    Internal Sea AI is not connected yet. Use global search results below or open a
                    quick action.
                  </p>
                </div>
              ) : null}

              {showSearchResults ? (
                <SearchResultsDropdown
                  query={query}
                  results={searchQuery.data?.items ?? []}
                  isLoading={searchQuery.isLoading}
                  error={searchQuery.isError ? getErrorMessage(searchQuery.error) : null}
                  onSelect={handleSelect}
                />
              ) : (
                <p className="px-4 py-6 text-center text-sm text-gray-500 sm:px-5">
                  Type to search projects, people, teams, capabilities, and more.
                </p>
              )}
            </div>
          </div>
        ) : null}

        <form
          onSubmit={handleSubmit}
          className={cn(
            'pointer-events-auto flex h-[60px] items-center gap-3 rounded-[22px] border border-auth-surfaceBorder',
            'bg-app-surface px-3 shadow-[0_12px_40px_-10px_rgb(17_24_39_/_0.2)] sm:px-4',
            isExpanded ? 'ring-2 ring-core-blue/20' : 'transition-shadow hover:shadow-[0_16px_44px_-10px_rgb(17_24_39_/_0.24)]',
          )}
        >
          <button
            type="button"
            onClick={() => {
              if (!isExpanded) {
                openPanel()
              }
            }}
            className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-core-blueSoft text-core-blue"
            aria-label="Open command palette"
          >
            <SparklesIcon />
          </button>

          {isExpanded ? (
            <input
              ref={inputRef}
              type="search"
              value={query}
              onChange={(event) => {
                setQuery(event.target.value)
                setShowAiPlaceholder(false)
              }}
              onKeyDown={handleInputKeyDown}
              placeholder="Ask Internal Sea AI or search anything…"
              aria-label="Ask Internal Sea AI or search anything"
              aria-controls={isExpanded ? panelId : undefined}
              aria-expanded={isExpanded}
              className="min-w-0 flex-1 bg-transparent text-sm text-gray-900 placeholder:text-gray-500 focus:outline-none"
            />
          ) : (
            <button
              type="button"
              onClick={openPanel}
              className="min-w-0 flex-1 truncate text-left text-sm text-gray-500"
            >
              Ask Internal Sea AI or search anything…
            </button>
          )}

          {!isExpanded ? (
            <div className="hidden items-center gap-1.5 sm:flex">
              {COMMAND_HINT_CHIPS.map((chip) => (
                <button
                  key={chip.label}
                  type="button"
                  onClick={() => handleChipSelect(chip.query)}
                  className="rounded-full border border-app-border bg-auth-input/50 px-2.5 py-1 text-xs text-gray-600 transition-colors hover:border-auth-inputBorder hover:bg-auth-surface"
                >
                  {chip.label}
                </button>
              ))}
            </div>
          ) : null}

          <kbd className="hidden shrink-0 rounded-md border border-app-border bg-auth-input/70 px-2 py-1 text-[11px] font-medium text-gray-500 lg:inline-block">
            {keyboardShortcut}
          </kbd>

          <button
            type="submit"
            disabled={!isExpanded || trimmedQuery.length === 0}
            aria-label="Submit search"
            className={cn(
              'inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl transition-colors',
              isExpanded && trimmedQuery.length > 0
                ? 'bg-core-blue text-white hover:bg-core-blueHover'
                : 'bg-app-muted text-gray-400',
            )}
          >
            <ArrowUpIcon />
          </button>
        </form>
      </div>
    </>,
    document.body,
  )
}
