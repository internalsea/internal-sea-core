import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { ScorecardCard } from '@/features/performance/components/ScorecardCard'
import { ScorecardMetricList } from '@/features/performance/components/ScorecardMetricList'
import { useEntityPerformanceScorecard } from '@/features/performance/hooks'
import type { PerformanceSubjectType } from '@/features/performance/types'
import { getApiErrorMessage } from '@/features/performance/utils'

interface PerformanceSectionProps {
  subjectType: PerformanceSubjectType
  subjectId: string
  title?: string
}

export function PerformanceSection({
  subjectType,
  subjectId,
  title = 'Performance',
}: PerformanceSectionProps) {
  const { data, isLoading, isError, error } = useEntityPerformanceScorecard(subjectType, subjectId)

  const newValueUrl = `/performance/values/new?subject_type=${subjectType}&subject_id=${subjectId}`

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title={title}
          description="Current scorecard metrics, targets and trends for this record."
        />
        <div className="flex flex-wrap gap-2">
          <Link to="/performance">
            <Button variant="secondary" size="sm">View performance</Button>
          </Link>
          <PermissionGate require="editor">
            <Link to={newValueUrl}>
              <Button variant="secondary" size="sm">Add metric value</Button>
            </Link>
          </PermissionGate>
        </div>
      </div>

      {isLoading ? (
        <p className="mt-4 text-sm text-gray-500">Loading performance scorecard…</p>
      ) : isError ? (
        <p className="mt-4 text-sm text-status-danger">{getApiErrorMessage(error)}</p>
      ) : !data ? (
        <p className="mt-4 text-sm text-gray-500">No performance data available.</p>
      ) : (
        <div className="mt-4 space-y-4">
          <ScorecardCard scorecard={data} />
          <ScorecardMetricList metrics={data.metrics} />
        </div>
      )}
    </Card>
  )
}
