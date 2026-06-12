import { useEffect, useId, useRef, useState } from 'react'

import { EntityPickerDropdown } from '@/features/entity-picker/components/EntityPickerDropdown'
import { SelectedEntityPill } from '@/features/entity-picker/components/SelectedEntityPill'
import { useEntitySearch } from '@/features/entity-picker/hooks'
import type { EntityPickerProps, EntityPickerResult } from '@/features/entity-picker/types'
import { buildPickerPlaceholder, normalizePickerResultToValue } from '@/features/entity-picker/utils'
import { cn } from '@/lib/utils'

const DEBOUNCE_MS = 300

export function EntityPicker({
  value,
  onChange,
  allowedTypes,
  label,
  placeholder,
  helperText,
  disabled = false,
  required = false,
  error,
  allowClear = true,
}: EntityPickerProps) {
  const inputId = useId()
  const containerRef = useRef<HTMLDivElement>(null)
  const [inputValue, setInputValue] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(0)

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedQuery(inputValue)
    }, DEBOUNCE_MS)
    return () => window.clearTimeout(timer)
  }, [inputValue])

  const { data: results = [], isLoading, isError } = useEntitySearch(
    debouncedQuery,
    allowedTypes,
    isOpen && !value,
  )

  useEffect(() => {
    setActiveIndex(0)
  }, [results])

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const resolvedPlaceholder = placeholder ?? buildPickerPlaceholder(allowedTypes)

  function handleSelect(result: EntityPickerResult) {
    onChange(normalizePickerResultToValue(result))
    setInputValue('')
    setDebouncedQuery('')
    setIsOpen(false)
  }

  function handleClear() {
    onChange(null)
    setInputValue('')
    setDebouncedQuery('')
    setIsOpen(false)
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {
    if (event.key === 'Escape') {
      setIsOpen(false)
      return
    }
    if (event.key === 'Enter' && isOpen && results.length > 0) {
      event.preventDefault()
      handleSelect(results[activeIndex] ?? results[0])
      return
    }
    if (event.key === 'ArrowDown' && isOpen && results.length > 0) {
      event.preventDefault()
      setActiveIndex((current) => Math.min(current + 1, results.length - 1))
    }
    if (event.key === 'ArrowUp' && isOpen && results.length > 0) {
      event.preventDefault()
      setActiveIndex((current) => Math.max(current - 1, 0))
    }
  }

  return (
    <div ref={containerRef} className="space-y-1.5">
      {label ? (
        <label htmlFor={inputId} className="block text-sm font-medium text-gray-700">
          {label}
          {required ? <span className="text-status-danger"> *</span> : null}
        </label>
      ) : null}

      {value ? (
        <SelectedEntityPill
          value={value}
          onClear={allowClear && !disabled ? handleClear : undefined}
          disabled={disabled}
        />
      ) : (
        <div className="relative">
          <input
            id={inputId}
            type="text"
            value={inputValue}
            disabled={disabled}
            placeholder={resolvedPlaceholder}
            onChange={(event) => {
              setInputValue(event.target.value)
              setIsOpen(true)
            }}
            onFocus={() => setIsOpen(true)}
            onKeyDown={handleKeyDown}
            className={cn(
              'block h-10 w-full rounded-md border border-app-borderStrong bg-app-surface px-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue',
              error && 'border-status-danger focus:border-status-danger focus:ring-status-danger',
            )}
            autoComplete="off"
            role="combobox"
            aria-expanded={isOpen}
            aria-controls={`${inputId}-listbox`}
          />
          {isOpen ? (
            <EntityPickerDropdown
              results={results}
              isLoading={isLoading}
              isError={isError}
              query={debouncedQuery}
              activeIndex={activeIndex}
              onSelect={handleSelect}
            />
          ) : null}
        </div>
      )}

      {helperText && !error ? <p className="text-xs text-gray-500">{helperText}</p> : null}
      {error ? <p className="text-xs text-status-danger">{error}</p> : null}
    </div>
  )
}
