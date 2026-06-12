import { useState } from 'react'

import { getApiErrorMessage } from '@/app/AuthProvider'
import { useTenancy } from '@/app/TenancyProvider'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { WorkspaceSettingsForm } from '@/features/tenancy/components/WorkspaceSettingsForm'
import { useUpdateWorkspace } from '@/features/tenancy/hooks'
import { workspaceToFormValues } from '@/features/tenancy/utils'

export function WorkspaceSettingsPage() {
  const { workspace, workspaceId, isLoading, refetch } = useTenancy()
  const updateWorkspace = useUpdateWorkspace()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading || !workspace || !workspaceId) {
    return <p className="text-sm text-gray-500">Loading workspace settings…</p>
  }

  return (
    <div>
      <PageHeader
        title="Workspace settings"
        description="Configure defaults and metadata for the active workspace."
      />

      <Card title="Workspace profile">
        <WorkspaceSettingsForm
          key={workspace.updated_at}
          initialValues={workspaceToFormValues(workspace)}
          isSubmitting={updateWorkspace.isPending}
          submitError={submitError}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateWorkspace.mutateAsync({ id: workspaceId, payload })
              await refetch()
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
