import { ModulePlaceholder } from '@/components/common/ModulePlaceholder'

export function DataProductsPage() {
  return (
    <ModulePlaceholder
      title="Data Products"
      description="Business-facing catalog of dashboards, datasets, metrics, APIs, AI agents, reports and automations."
    >
      <p className="text-sm text-gray-700">
        The backend Data Product API is connected via <code>/api/v1/data-products</code>.
      </p>
      <p className="mt-3 text-sm text-gray-500">
        Prompt 7 will implement the first working catalog table with search, filters, create/edit/delete
        and a detail page.
      </p>
    </ModulePlaceholder>
  )
}
