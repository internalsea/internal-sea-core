import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

interface RunTriggerDialogProps {
  open: boolean
  simulate: boolean
  isRunning?: boolean
  onConfirm: () => void
  onCancel: () => void
}

export function RunTriggerDialog({
  open,
  simulate,
  isRunning = false,
  onConfirm,
  onCancel,
}: RunTriggerDialogProps) {
  if (!open) {
    return null
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <Card className="w-full max-w-md">
        <h3 className="text-lg font-semibold text-gray-900">
          {simulate ? 'Run simulation?' : 'Run this automation now?'}
        </h3>
        <p className="mt-2 text-sm text-gray-600">
          {simulate
            ? 'Simulation records a run and shows what would happen. No business objects are created.'
            : 'This may create a work item, comment or activity event depending on action type.'}
        </p>
        <div className="mt-6 flex justify-end gap-3">
          <Button variant="secondary" onClick={onCancel} disabled={isRunning}>
            Cancel
          </Button>
          <Button onClick={onConfirm} disabled={isRunning}>
            {isRunning ? 'Running…' : simulate ? 'Run Simulation' : 'Run Now'}
          </Button>
        </div>
      </Card>
    </div>
  )
}
