export function LoadingState({ message = 'Loading…' }: { message?: string }) {
  return (
    <div className="rounded-card border border-app-border bg-app-surface px-6 py-10 text-center text-sm text-gray-500">
      {message}
    </div>
  )
}
