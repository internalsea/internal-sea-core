import { LoadingState } from '@/components/common/LoadingState'

export function AuthLoadingScreen() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-app-background">
      <LoadingState message="Checking session…" />
    </div>
  )
}
