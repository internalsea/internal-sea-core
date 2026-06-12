import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { Card } from '@/components/ui/Card'
import { EmptyState } from '@/components/ui/EmptyState'
import { PageHeader } from '@/components/ui/PageHeader'
import { confirmProjectDelete } from '@/features/projects/components/ProjectDeleteDialog'
import { ProjectFiltersBar } from '@/features/projects/components/ProjectFilters'
import { ProjectTable } from '@/features/projects/components/ProjectTable'
import { DEFAULT_PAGE_SIZE } from '@/features/projects/constants'
import { useDeleteProject, useProjects } from '@/features/projects/hooks'
import type { ProjectFilters, ProjectListItem } from '@/features/projects/types'
import { getApiErrorMessage } from '@/features/projects/utils'

const initialFilters: ProjectFilters = {
  page: 1,
  page_size: DEFAULT_PAGE_SIZE,
}

export function ProjectsPage() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<ProjectFilters>(initialFilters)
  const { data, isLoading, isError, error } = useProjects(filters)
  const deleteMutation = useDeleteProject()

  const handleDelete = async (item: ProjectListItem) => {
    if (!confirmProjectDelete(item.name, 'projects')) {
      return
    }
    try {
      await deleteMutation.mutateAsync(item.id)
    } catch {
      // Error surfaced via mutation state if needed
    }
  }

  const total = data?.total ?? 0
  const page = data?.page ?? 1
  const pages = data?.pages ?? 1

  return (
    <div className="space-y-6">
      <PageHeader
        title="Projects"
        description="Manage client projects, POCs, pilots, MVPs and initiatives."
        actions={
          <PermissionGate require="editor">
            <Link to="/projects/new">
              <Button>New Project</Button>
            </Link>
          </PermissionGate>
        }
      />

      <Card>
        <ProjectFiltersBar
          filters={filters}
          variant="projects"
          onChange={setFilters}
          onReset={() => setFilters(initialFilters)}
        />
      </Card>

      {isError ? (
        <ErrorState message={getApiErrorMessage(error)} />
      ) : (
        <>
          <ProjectTable
            items={data?.items ?? []}
            variant="projects"
            isLoading={isLoading}
            onOpen={(id) => navigate(`/projects/${id}`)}
            onEdit={(id) => navigate(`/projects/${id}/edit`)}
            onDelete={handleDelete}
          />

          {!isLoading && (data?.items.length ?? 0) === 0 ? (
            <EmptyState
              title="No projects yet"
              description="Create your first project to track client delivery, POCs, pilots and initiatives."
              action={
                <PermissionGate require="editor">
                  <Link to="/projects/new">
                    <Button>New Project</Button>
                  </Link>
                </PermissionGate>
              }
            />
          ) : null}

          {!isLoading && total > 0 ? (
            <div className="flex items-center justify-between text-sm text-gray-600">
              <p>
                {total} project{total === 1 ? '' : 's'} · Page {page} of {pages}
              </p>
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  disabled={page <= 1}
                  onClick={() => setFilters((current) => ({ ...current, page: page - 1 }))}
                >
                  Previous
                </Button>
                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  disabled={page >= pages}
                  onClick={() => setFilters((current) => ({ ...current, page: page + 1 }))}
                >
                  Next
                </Button>
              </div>
            </div>
          ) : null}
        </>
      )}
    </div>
  )
}
