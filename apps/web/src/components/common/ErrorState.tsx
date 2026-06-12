interface ErrorStateProps {
  title?: string
  message: string
}

export function ErrorState({
  title = 'Something went wrong',
  message,
}: ErrorStateProps) {
  return (
    <div className="rounded-card border border-status-danger/20 bg-status-dangerSoft px-6 py-10 text-center">
      <h3 className="text-base font-semibold text-status-danger">{title}</h3>
      <p className="mx-auto mt-2 max-w-lg text-sm text-red-700">{message}</p>
    </div>
  )
}
