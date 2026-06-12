import { Badge } from '@/components/ui/Badge'
import { complianceStatusLabels } from '@/features/compliance/constants'
import type { ComplianceStatus } from '@/features/compliance/types'
import { getComplianceStatusVariant } from '@/features/compliance/utils'

interface ComplianceStatusBadgeProps {
  status: ComplianceStatus
}

export function ComplianceStatusBadge({ status }: ComplianceStatusBadgeProps) {
  return (
    <Badge variant={getComplianceStatusVariant(status)}>{complianceStatusLabels[status]}</Badge>
  )
}
