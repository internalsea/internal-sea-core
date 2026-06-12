import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import {
  selectClassName,
  WORK_ITEM_PRIORITIES,
  WORK_ITEM_STATUSES,
  WORK_ITEM_TYPES,
} from '@/features/work-items/constants'
import type { WorkItemFilters } from '@/features/work-items/types'

interface WorkItemFiltersProps {
  filters: WorkItemFilters
  onChange: (filters: WorkItemFilters) => void
  onReset: () => void
  showStatus?: boolean
  showDataProductId?: boolean
}

export function WorkItemFiltersBar({
  filters,
  onChange,
  onReset,
  showStatus = true,
  showDataProductId = false,
}: WorkItemFiltersProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
      <Input
        label="Search"
        placeholder="Search by title or description"
        value={filters.search ?? ''}
        onChange={(event) =>
          onChange({ ...filters, search: event.target.value || undefined, page: 1 })
        }
      />
      <div className="space-y-1.5">
        <label htmlFor="work-item-type-filter" className="block text-sm font-medium text-gray-700">
          Type
        </label>
        <select
          id="work-item-type-filter"
          className={selectClassName}
          value={filters.type ?? ''}
          onChange={(event) =>
            onChange({
              ...filters,
              type: event.target.value ? (event.target.value as WorkItemFilters['type']) : undefined,
              page: 1,
            })
          }
        >
          <option value="">All types</option>
          {WORK_ITEM_TYPES.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      {showStatus ? (
        <div className="space-y-1.5">
          <label htmlFor="work-item-status-filter" className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <select
            id="work-item-status-filter"
            className={selectClassName}
            value={filters.status ?? ''}
            onChange={(event) =>
              onChange({
                ...filters,
                status: event.target.value
                  ? (event.target.value as WorkItemFilters['status'])
                  : undefined,
                page: 1,
              })
            }
          >
            <option value="">All statuses</option>
            {WORK_ITEM_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      ) : null}
      <div className="space-y-1.5">
        <label htmlFor="work-item-priority-filter" className="block text-sm font-medium text-gray-700">
          Priority
        </label>
        <select
          id="work-item-priority-filter"
          className={selectClassName}
          value={filters.priority ?? ''}
          onChange={(event) =>
            onChange({
              ...filters,
              priority: event.target.value
                ? (event.target.value as WorkItemFilters['priority'])
                : undefined,
              page: 1,
            })
          }
        >
          <option value="">All priorities</option>
          {WORK_ITEM_PRIORITIES.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      {showDataProductId ? (
        <Input
          label="Data product ID"
          placeholder="Optional UUID filter"
          value={filters.data_product_id ?? ''}
          onChange={(event) =>
            onChange({
              ...filters,
              data_product_id: event.target.value || undefined,
              page: 1,
            })
          }
        />
      ) : (
        <div className="flex items-end">
          <Button type="button" variant="secondary" onClick={onReset}>
            Reset filters
          </Button>
        </div>
      )}
      {showDataProductId ? (
        <div className="flex items-end md:col-span-2 xl:col-span-5">
          <Button type="button" variant="secondary" onClick={onReset}>
            Reset filters
          </Button>
        </div>
      ) : null}
    </div>
  )
}
