import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  Person,
  PersonCreateInput,
  PersonFilters,
  PersonListResponse,
  PersonSummary,
  PersonUpdateInput,
} from '@/features/people/types'

function toQueryParams(
  filters?: PersonFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) {
    return undefined
  }

  return {
    search: filters.search,
    team_id: filters.team_id,
    capability_id: filters.capability_id,
    seniority_level: filters.seniority_level,
    is_active: filters.is_active,
    location: filters.location,
    min_availability: filters.min_availability,
    max_availability: filters.max_availability,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getPeople(filters?: PersonFilters): Promise<PersonListResponse> {
  return apiGet<PersonListResponse>('/people', toQueryParams(filters))
}

export function getPerson(id: string): Promise<Person> {
  return apiGet<Person>(`/people/${id}`)
}

export function getPersonSummary(id: string): Promise<PersonSummary> {
  return apiGet<PersonSummary>(`/people/${id}/summary`)
}

export function createPerson(payload: PersonCreateInput): Promise<Person> {
  return apiPost<Person>('/people', payload)
}

export function updatePerson(id: string, payload: PersonUpdateInput): Promise<Person> {
  return apiPatch<Person>(`/people/${id}`, payload)
}

export function deactivatePerson(id: string): Promise<void> {
  return apiDelete(`/people/${id}`)
}
