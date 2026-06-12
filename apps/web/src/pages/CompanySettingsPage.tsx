import { useState } from 'react'

import { getApiErrorMessage } from '@/app/AuthProvider'
import { useTenancy } from '@/app/TenancyProvider'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { CompanySettingsForm } from '@/features/tenancy/components/CompanySettingsForm'
import { MembersTable } from '@/features/tenancy/components/MembersTable'
import { useCompanyMembers, useUpdateCompany, useUpdateMember } from '@/features/tenancy/hooks'
import { companyToFormValues } from '@/features/tenancy/utils'

export function CompanySettingsPage() {
  const { company, companyId, role, isLoading, refetch } = useTenancy()
  const updateCompany = useUpdateCompany()
  const updateMember = useUpdateMember()
  const membersQuery = useCompanyMembers(companyId ?? undefined)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [updatingMemberId, setUpdatingMemberId] = useState<string | null>(null)

  const canManage = role === 'owner' || role === 'admin'

  if (isLoading || !company) {
    return <p className="text-sm text-gray-500">Loading company settings…</p>
  }

  return (
    <div>
      <PageHeader
        title="Company settings"
        description="Manage your organization profile and members."
      />

      <div className="space-y-6">
        <Card title="Company profile">
          <CompanySettingsForm
            key={company.updated_at}
            initialValues={companyToFormValues(company)}
            isSubmitting={updateCompany.isPending}
            submitError={submitError}
            onSubmit={async (payload) => {
              setSubmitError(null)
              try {
                await updateCompany.mutateAsync({ id: company.id, payload })
                await refetch()
              } catch (error) {
                setSubmitError(getApiErrorMessage(error))
              }
            }}
          />
        </Card>

        <Card>
          <SectionHeader
            title="Members"
            description="People with access to this company."
          />
          <MembersTable
            items={membersQuery.data?.items ?? []}
            isLoading={membersQuery.isLoading}
            canManage={canManage}
            isUpdatingId={updatingMemberId}
            onRoleChange={async (memberId, nextRole) => {
              setUpdatingMemberId(memberId)
              try {
                await updateMember.mutateAsync({
                  memberId,
                  payload: { role: nextRole },
                })
                await membersQuery.refetch()
              } finally {
                setUpdatingMemberId(null)
              }
            }}
          />
        </Card>
      </div>
    </div>
  )
}
