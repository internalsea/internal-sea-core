import { useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { Card } from '@/components/ui/Card'
import { EmptyState } from '@/components/ui/EmptyState'
import { PageHeader } from '@/components/ui/PageHeader'
import { useCapabilities } from '@/features/capabilities/hooks'
import { confirmPersonDeactivate } from '@/features/people/components/PersonDeactivateDialog'
import { PeopleFiltersBar } from '@/features/people/components/PeopleFilters'
import { PeopleTable } from '@/features/people/components/PeopleTable'
import { DEFAULT_PAGE_SIZE, SELECTOR_PAGE_SIZE } from '@/features/people/constants'
import { useDeactivatePerson, usePeople } from '@/features/people/hooks'
import type { PersonFilters, PersonListItem } from '@/features/people/types'
import { getApiErrorMessage } from '@/features/people/utils'
import { useTeams } from '@/features/teams/hooks'

const initialFilters: PersonFilters = {
  page: 1,
  page_size: DEFAULT_PAGE_SIZE,
  is_active: true,
}

export function PeoplePage() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<PersonFilters>(initialFilters)
  const { data, isLoading, isError, error } = usePeople(filters)
  const deactivateMutation = useDeactivatePerson()
  const { data: teamsData } = useTeams({ page: 1, page_size: SELECTOR_PAGE_SIZE })
  const { data: capabilitiesData } = useCapabilities({ page: 1, page_size: SELECTOR_PAGE_SIZE })

  const teamOptions = useMemo(
    () => teamsData?.items.map((team) => ({ id: team.id, name: team.name })) ?? [],
    [teamsData],
  )
  const capabilityOptions = useMemo(
    () => capabilitiesData?.items.map((cap) => ({ id: cap.id, name: cap.name })) ?? [],
    [capabilitiesData],
  )
  const teamNames = useMemo(
    () => Object.fromEntries(teamOptions.map((team) => [team.id, team.name])),
    [teamOptions],
  )
  const capabilityNames = useMemo(
    () => Object.fromEntries(capabilityOptions.map((cap) => [cap.id, cap.name])),
    [capabilityOptions],
  )

  const handleDeactivate = async (item: PersonListItem) => {
    if (!confirmPersonDeactivate(item.full_name)) {
      return
    }
    try {
      await deactivateMutation.mutateAsync(item.id)
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
        title="People"
        description="Manage people, roles, seniority, availability, teams and capabilities."
        actions={
          <PermissionGate require="editor">
            <Link to="/people/new">
              <Button>New Person</Button>
            </Link>
          </PermissionGate>
        }
      />

      <Card>
        <PeopleFiltersBar
          filters={filters}
          teamOptions={teamOptions}
          capabilityOptions={capabilityOptions}
          onChange={setFilters}
          onReset={() => setFilters(initialFilters)}
        />
      </Card>

      {isError ? (
        <ErrorState message={getApiErrorMessage(error)} />
      ) : (
        <>
          <PeopleTable
            items={data?.items ?? []}
            isLoading={isLoading}
            teamNames={teamNames}
            capabilityNames={capabilityNames}
            onOpen={(id) => navigate(`/people/${id}`)}
            onEdit={(id) => navigate(`/people/${id}/edit`)}
            onDeactivate={handleDeactivate}
          />

          {!isLoading && (data?.items.length ?? 0) === 0 ? (
            <EmptyState
              title="No people yet"
              description="Create your first person to track roles, teams and delivery capacity."
              action={
                <PermissionGate require="editor">
                  <Link to="/people/new">
                    <Button>New Person</Button>
                  </Link>
                </PermissionGate>
              }
            />
          ) : null}

          {!isLoading && total > 0 ? (
            <div className="flex items-center justify-between text-sm text-gray-600">
              <p>
                {total} person{total === 1 ? '' : 's'} · Page {page} of {pages}
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
