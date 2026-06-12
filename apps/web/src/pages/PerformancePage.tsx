import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { DEFAULT_PAGE_SIZE } from '@/features/performance/constants'
import { MetricDefinitionsTable } from '@/features/performance/components/MetricDefinitionsTable'
import { MetricValuesTable } from '@/features/performance/components/MetricValuesTable'
import { PerformanceOverviewCards } from '@/features/performance/components/PerformanceOverviewCards'
import {
  useDeleteMetricDefinition,
  useDeleteMetricValue,
  useMetricDefinitions,
  useMetricValues,
  usePerformanceOverview,
} from '@/features/performance/hooks'
import type {
  MetricDefinitionFilters,
  MetricValueFilters,
  PerformanceMetricDefinitionListItem,
} from '@/features/performance/types'
import { getApiErrorMessage } from '@/features/performance/utils'

export function PerformancePage() {
  const definitionFilters: MetricDefinitionFilters = { page: 1, page_size: DEFAULT_PAGE_SIZE }
  const valueFilters: MetricValueFilters = { page: 1, page_size: DEFAULT_PAGE_SIZE }

  const overviewQuery = usePerformanceOverview()
  const definitionsQuery = useMetricDefinitions(definitionFilters)
  const valuesQuery = useMetricValues(valueFilters)
  const deleteDefinitionMutation = useDeleteMetricDefinition()
  const deleteValueMutation = useDeleteMetricValue()
  const [actionError, setActionError] = useState<string | null>(null)

  const definitionsById = useMemo(() => {
    const map: Record<string, PerformanceMetricDefinitionListItem> = {}
    for (const item of definitionsQuery.data?.items ?? []) {
      map[item.id] = item
    }
    return map
  }, [definitionsQuery.data?.items])

  const handleDeleteDefinition = async (item: { id: string; name: string }) => {
    if (!window.confirm(`Delete metric definition "${item.name}"?`)) return
    setActionError(null)
    try {
      await deleteDefinitionMutation.mutateAsync(item.id)
    } catch (error) {
      setActionError(getApiErrorMessage(error))
    }
  }

  const handleDeleteValue = async (item: { id: string }) => {
    if (!window.confirm('Delete this metric value?')) return
    setActionError(null)
    try {
      await deleteValueMutation.mutateAsync(item.id)
    } catch (error) {
      setActionError(getApiErrorMessage(error))
    }
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Performance"
        description="Track metrics and scorecards for people, teams, capabilities, projects and data products."
        actions={
          <PermissionGate require="editor">
            <div className="flex gap-2">
              <Link to="/performance/metrics/new">
                <Button>New Metric</Button>
              </Link>
              <Link to="/performance/values/new">
                <Button variant="secondary">New Value</Button>
              </Link>
            </div>
          </PermissionGate>
        }
      />

      <PerformanceOverviewCards
        overview={overviewQuery.data}
        isLoading={overviewQuery.isLoading}
      />

      {actionError ? <ErrorState message={actionError} /> : null}

      <Card title="Metric definitions">
        {definitionsQuery.isError ? (
          <ErrorState message={getApiErrorMessage(definitionsQuery.error)} />
        ) : (
          <MetricDefinitionsTable
            items={definitionsQuery.data?.items ?? []}
            onDelete={handleDeleteDefinition}
          />
        )}
      </Card>

      <Card title="Recent metric values">
        {valuesQuery.isError ? (
          <ErrorState message={getApiErrorMessage(valuesQuery.error)} />
        ) : (
          <MetricValuesTable
            items={valuesQuery.data?.items ?? []}
            definitionsById={definitionsById}
            onDelete={handleDeleteValue}
          />
        )}
      </Card>

      <Card title="Future capabilities">
        <ul className="list-disc space-y-1 pl-5 text-sm text-gray-600">
          <li>Automatic metric calculations</li>
          <li>Advanced trend analytics</li>
          <li>External BI integration</li>
          <li>AI-assisted performance insights</li>
        </ul>
      </Card>
    </div>
  )
}
