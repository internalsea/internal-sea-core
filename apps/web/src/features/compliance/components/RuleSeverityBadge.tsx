import { Badge } from '@/components/ui/Badge'
import { RULE_SEVERITIES } from '@/features/compliance/constants'
import type { RuleSeverity } from '@/features/compliance/types'
import { getRuleSeverityVariant } from '@/features/compliance/utils'

const labels = Object.fromEntries(RULE_SEVERITIES.map((item) => [item.value, item.label]))

interface RuleSeverityBadgeProps {
  severity: RuleSeverity
}

export function RuleSeverityBadge({ severity }: RuleSeverityBadgeProps) {
  return <Badge variant={getRuleSeverityVariant(severity)}>{labels[severity]}</Badge>
}
