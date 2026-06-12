import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  Team,
  TeamCreateInput,
  TeamFilters,
  TeamListResponse,
  TeamSummary,
  TeamUpdateInput,
} from '@/features/teams/types'

function toQueryParams(
  filters?: TeamFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) {
    return undefined
  }

  return {
    search: filters.search,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getTeams(filters?: TeamFilters): Promise<TeamListResponse> {
  return apiGet<TeamListResponse>('/teams', toQueryParams(filters))
}

export function getTeam(id: string): Promise<Team> {
  return apiGet<Team>(`/teams/${id}`)
}

export function getTeamSummary(id: string): Promise<TeamSummary> {
  return apiGet<TeamSummary>(`/teams/${id}/summary`)
}

export function createTeam(payload: TeamCreateInput): Promise<Team> {
  return apiPost<Team>('/teams', payload)
}

export function updateTeam(id: string, payload: TeamUpdateInput): Promise<Team> {
  return apiPatch<Team>(`/teams/${id}`, payload)
}

export function deleteTeam(id: string): Promise<void> {
  return apiDelete(`/teams/${id}`)
}
