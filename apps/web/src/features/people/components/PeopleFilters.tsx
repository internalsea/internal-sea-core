import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import {
  PERSON_STATUS_OPTIONS,
  SENIORITY_LEVELS,
  selectClassName,
} from '@/features/people/constants'
import type { PersonFilters } from '@/features/people/types'
import type { SeniorityLevel } from '@/features/people/types'

interface PeopleFiltersProps {
  filters: PersonFilters
  teamOptions?: Array<{ id: string; name: string }>
  capabilityOptions?: Array<{ id: string; name: string }>
  onChange: (filters: PersonFilters) => void
  onReset: () => void
}

export function PeopleFiltersBar({
  filters,
  teamOptions = [],
  capabilityOptions = [],
  onChange,
  onReset,
}: PeopleFiltersProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      <Input
        label="Search"
        placeholder="Search by name, email or role"
        value={filters.search ?? ''}
        onChange={(event) =>
          onChange({ ...filters, search: event.target.value || undefined, page: 1 })
        }
      />
      <div className="space-y-1.5">
        <label htmlFor="seniority-filter" className="block text-sm font-medium text-gray-700">
          Seniority
        </label>
        <select
          id="seniority-filter"
          className={selectClassName}
          value={filters.seniority_level ?? ''}
          onChange={(event) =>
            onChange({
              ...filters,
              seniority_level: event.target.value
                ? (event.target.value as SeniorityLevel)
                : undefined,
              page: 1,
            })
          }
        >
          <option value="">All levels</option>
          {SENIORITY_LEVELS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      <div className="space-y-1.5">
        <label htmlFor="active-filter" className="block text-sm font-medium text-gray-700">
          Status
        </label>
        <select
          id="active-filter"
          className={selectClassName}
          value={
            filters.is_active === undefined ? '' : filters.is_active ? 'true' : 'false'
          }
          onChange={(event) =>
            onChange({
              ...filters,
              is_active:
                event.target.value === '' ? undefined : event.target.value === 'true',
              page: 1,
            })
          }
        >
          <option value="">All statuses</option>
          {PERSON_STATUS_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      <Input
        label="Location"
        placeholder="Filter by location"
        value={filters.location ?? ''}
        onChange={(event) =>
          onChange({ ...filters, location: event.target.value || undefined, page: 1 })
        }
      />
      <div className="space-y-1.5">
        <label htmlFor="team-filter" className="block text-sm font-medium text-gray-700">
          Team
        </label>
        <select
          id="team-filter"
          className={selectClassName}
          value={filters.team_id ?? ''}
          onChange={(event) =>
            onChange({
              ...filters,
              team_id: event.target.value || undefined,
              page: 1,
            })
          }
        >
          <option value="">All teams</option>
          {teamOptions.map((team) => (
            <option key={team.id} value={team.id}>
              {team.name}
            </option>
          ))}
        </select>
      </div>
      <div className="space-y-1.5">
        <label htmlFor="capability-filter" className="block text-sm font-medium text-gray-700">
          Capability
        </label>
        <select
          id="capability-filter"
          className={selectClassName}
          value={filters.capability_id ?? ''}
          onChange={(event) =>
            onChange({
              ...filters,
              capability_id: event.target.value || undefined,
              page: 1,
            })
          }
        >
          <option value="">All capabilities</option>
          {capabilityOptions.map((capability) => (
            <option key={capability.id} value={capability.id}>
              {capability.name}
            </option>
          ))}
        </select>
      </div>
      <div className="flex items-end md:col-span-2 xl:col-span-4">
        <Button type="button" variant="secondary" onClick={onReset}>
          Reset filters
        </Button>
      </div>
    </div>
  )
}
