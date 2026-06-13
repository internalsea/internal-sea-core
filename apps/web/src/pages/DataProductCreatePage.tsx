import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { DataProductForm } from '@/features/data-products/components/DataProductForm'
import { useCreateDataProduct } from '@/features/data-products/hooks'
import { getApiErrorMessage } from '@/features/data-products/utils'

export function DataProductCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateDataProduct()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Data Product"
        description="Add a dashboard, dataset, metric, API, report or other catalog entry."
        actions={
          <Link to="/data-products">
            <Button variant="secondary">Back to Data Products</Button>
          </Link>
        }
      />

      <Card>
        <DataProductForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/data-products')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/data-products/${created.id}`)
            } catch (err) {
              setSubmitError(getApiErrorMessage(err))
            }
          }}
        />
      </Card>
    </div>
  )
}
