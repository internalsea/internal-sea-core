import { Link } from 'react-router-dom'

import { Card } from '@/components/ui/Card'
import { operationsSettingsLinks } from '@/lib/navigation'

export function OperationsSettingsSection() {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {operationsSettingsLinks.map((item) => (
        <Card key={item.path} className="flex h-full flex-col">
          <h3 className="text-base font-semibold text-gray-900">{item.label}</h3>
          <p className="mt-2 flex-1 text-sm text-gray-600">{item.description}</p>
          <Link
            to={item.path}
            className="mt-4 inline-flex text-sm font-medium text-core-blue hover:text-core-blueHover"
          >
            Open {item.label.toLowerCase()}
          </Link>
        </Card>
      ))}
    </div>
  )
}
