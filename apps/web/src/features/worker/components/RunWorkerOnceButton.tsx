import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { useRunWorkerOnce } from '@/features/worker/hooks'

export function RunWorkerOnceButton() {
  const [message, setMessage] = useState<string | null>(null)
  const mutation = useRunWorkerOnce()

  const handleClick = () => {
    if (!window.confirm('Run one worker cycle now?')) {
      return
    }
    setMessage(null)
    mutation.mutate(undefined, {
      onSuccess: (result) => setMessage(result.summary),
      onError: () => setMessage('Worker cycle failed.'),
    })
  }

  return (
    <div className="flex flex-col gap-2">
      <Button onClick={handleClick} disabled={mutation.isPending}>
        {mutation.isPending ? 'Running…' : 'Run Worker Once'}
      </Button>
      {message ? <p className="text-sm text-gray-700">{message}</p> : null}
    </div>
  )
}
