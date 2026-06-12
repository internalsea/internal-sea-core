import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  Project,
  ProjectCreateInput,
  ProjectFilters,
  ProjectListResponse,
  ProjectSummary,
  ProjectUpdateInput,
} from '@/features/projects/types'

function toQueryParams(
  filters?: ProjectFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) {
    return undefined
  }

  return {
    search: filters.search,
    project_type: filters.project_type,
    status: filters.status,
    client_name: filters.client_name,
    account_name: filters.account_name,
    owner_id: filters.owner_id,
    team_id: filters.team_id,
    capability_id: filters.capability_id,
    health_status: filters.health_status,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getProjects(filters?: ProjectFilters): Promise<ProjectListResponse> {
  return apiGet<ProjectListResponse>('/projects', toQueryParams(filters))
}

export function getProject(id: string): Promise<Project> {
  return apiGet<Project>(`/projects/${id}`)
}

export function getProjectSummary(id: string): Promise<ProjectSummary> {
  return apiGet<ProjectSummary>(`/projects/${id}/summary`)
}

export function createProject(payload: ProjectCreateInput): Promise<Project> {
  return apiPost<Project>('/projects', payload)
}

export function updateProject(id: string, payload: ProjectUpdateInput): Promise<Project> {
  return apiPatch<Project>(`/projects/${id}`, payload)
}

export function deleteProject(id: string): Promise<void> {
  return apiDelete(`/projects/${id}`)
}

export function getInternalProjects(filters?: ProjectFilters): Promise<ProjectListResponse> {
  return apiGet<ProjectListResponse>('/internal-projects', toQueryParams(filters))
}

export function getInternalProject(id: string): Promise<Project> {
  return apiGet<Project>(`/internal-projects/${id}`)
}

export function createInternalProject(payload: ProjectCreateInput): Promise<Project> {
  return apiPost<Project>('/internal-projects', {
    ...payload,
    project_type: 'internal_project',
  })
}

export function updateInternalProject(id: string, payload: ProjectUpdateInput): Promise<Project> {
  const rest = { ...payload }
  delete rest.project_type
  return apiPatch<Project>(`/internal-projects/${id}`, rest)
}

export function deleteInternalProject(id: string): Promise<void> {
  return apiDelete(`/internal-projects/${id}`)
}
