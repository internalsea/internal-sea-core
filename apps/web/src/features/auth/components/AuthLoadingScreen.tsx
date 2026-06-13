import { LoadingState } from '@/components/common/LoadingState'
import { AuthLayout } from '@/components/layout/AuthLayout'

export function AuthLoadingScreen() {
  return (
    <AuthLayout>
      <LoadingState message="Checking session…" />
    </AuthLayout>
  )
}
