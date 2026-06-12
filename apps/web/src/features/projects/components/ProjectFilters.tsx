import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import {
  PROJECT_HEALTH_STATUSES,
  PROJECT_STATUSES,
  PROJECT_TYPES,
  selectClassName,
} from '@/features/projects/constants'
import type { ProjectFilters as ProjectFiltersState, ProjectVariant } from '@/features/projects/types'

interface ProjectFiltersProps {
  filters: ProjectFiltersState
  variant?: ProjectVariant
  onChange: (filters: ProjectFiltersState) => void
  onReset: () => void
}

export function ProjectFiltersBar({
  filters,
  variant = 'projects',
  onChange,
  onReset,
}: ProjectFiltersProps) {
  const isInternal = variant === 'internal-projects'

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
      <Input
        label="Search"
        placeholder="Search by name or description"
        value={filters.search ?? ''}
        onChange={(event) =>
          onChange({ ...filters, search: event.target.value || undefined, page: 1 })
        }
      />
      {!isInternal ? (
        <div className="space-y-1.5">
          <label htmlFor="project-type-filter" className="block text-sm font-medium text-gray-700">
            Type
          </label>
          <select
            id="project-type-filter"
            className={selectClassName}
            value={filters.project_type ?? ''}
            onChange={(event) =>
              onChange({
                ...filters,
                project_type: event.target.value
                  ? (event.target.value as ProjectFiltersState['project_type'])
                  : undefined,
                page: 1,
              })
            }
          >
            <option value="">All types</option>
            {PROJECT_TYPES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      ) : null}
      <div className="space-y-1.5">
        <label htmlFor="project-status-filter" className="block text-sm font-medium text-gray-700">
          Status
        </label>
        <select
          id="project-status-filter"
          className={selectClassName}
          value={filters.status ?? ''}
          onChange={(event) =>
            onChange({
              ...filters,
              status: event.target.value
                ? (event.target.value as ProjectFiltersState['status'])
                : undefined,
              page: 1,
            })
          }
        >
          <option value="">All statuses</option>
          {PROJECT_STATUSES.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      <div className="space-y-1.5">
        <label htmlFor="project-health-filter" className="block text-sm font-medium text-gray-700">
          Health
        </label>
        <select
          id="project-health-filter"
          className={selectClassName}
          value={filters.health_status ?? ''}
          onChange={(event) =>
            onChange({
              ...filters,
              health_status: event.target.value || undefined,
              page: 1,
            })
          }
        >
          <option value="">All health statuses</option>
          {PROJECT_HEALTH_STATUSES.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      {!isInternal ? (
        <Input
          label="Client name"
          placeholder="Filter by client"
          value={filters.client_name ?? ''}
          onChange={(event) =>
            onChange({ ...filters, client_name: event.target.value || undefined, page: 1 })
          }
        />
      ) : (
        <div className="flex items-end">
          <Button type="button" variant="secondary" onClick={onReset}>
            Reset filters
          </Button>
        </div>
      )}
      {!isInternal ? (
        <div className="flex items-end md:col-span-2 xl:col-span-5">
          <Button type="button" variant="secondary" onClick={onReset}>
            Reset filters
          </Button>
        </div>
      ) : null}
    </div>
  )
}
