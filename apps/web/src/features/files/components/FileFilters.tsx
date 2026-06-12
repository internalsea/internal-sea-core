import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import {
  FILE_ASSET_TYPES,
  FILE_SENSITIVITIES,
  FILE_STATUSES,
  selectClassName,
} from '@/features/files/constants'
import type { FileFilters } from '@/features/files/types'

interface FileFiltersBarProps {
  filters: FileFilters
  onChange: (filters: FileFilters) => void
  onReset: () => void
}

export function FileFiltersBar({ filters, onChange, onReset }: FileFiltersBarProps) {
  const update = (patch: Partial<FileFilters>) => {
    onChange({ ...filters, ...patch, page: 1 })
  }

  return (
    <div className="flex flex-wrap items-end gap-4">
      <div className="min-w-[200px] flex-1">
        <label className="mb-1 block text-xs font-medium text-gray-600">Search</label>
        <Input
          value={filters.search ?? ''}
          placeholder="Name, description, URL…"
          onChange={(event) => update({ search: event.target.value || undefined })}
        />
      </div>
      <div className="w-40">
        <label className="mb-1 block text-xs font-medium text-gray-600">Type</label>
        <select
          className={selectClassName}
          value={filters.file_type ?? ''}
          onChange={(event) =>
            update({ file_type: (event.target.value || undefined) as FileFilters['file_type'] })
          }
        >
          <option value="">All types</option>
          {FILE_ASSET_TYPES.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>
      </div>
      <div className="w-36">
        <label className="mb-1 block text-xs font-medium text-gray-600">Status</label>
        <select
          className={selectClassName}
          value={filters.status ?? ''}
          onChange={(event) =>
            update({ status: (event.target.value || undefined) as FileFilters['status'] })
          }
        >
          <option value="">All statuses</option>
          {FILE_STATUSES.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>
      </div>
      <div className="w-40">
        <label className="mb-1 block text-xs font-medium text-gray-600">Sensitivity</label>
        <select
          className={selectClassName}
          value={filters.sensitivity ?? ''}
          onChange={(event) =>
            update({
              sensitivity: (event.target.value || undefined) as FileFilters['sensitivity'],
            })
          }
        >
          <option value="">All</option>
          {FILE_SENSITIVITIES.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>
      </div>
      <div className="w-36">
        <label className="mb-1 block text-xs font-medium text-gray-600">Evidence</label>
        <select
          className={selectClassName}
          value={filters.is_evidence === undefined ? '' : String(filters.is_evidence)}
          onChange={(event) => {
            const value = event.target.value
            update({
              is_evidence: value === '' ? undefined : value === 'true',
            })
          }}
        >
          <option value="">All</option>
          <option value="true">Evidence only</option>
          <option value="false">Non-evidence</option>
        </select>
      </div>
      <Button variant="secondary" onClick={onReset}>
        Reset
      </Button>
    </div>
  )
}
