import { useAuthContext } from '@/app/AuthProvider'
import { roleCanAdmin, roleCanWrite } from '@/features/auth/utils'

export function useAuth() {
  return useAuthContext()
}

export function useCurrentUser() {
  const { user } = useAuthContext()
  return user
}

export function useCanWrite() {
  const { user } = useAuthContext()
  if (!user) return false
  return roleCanWrite(user.role, user.is_superuser)
}

export function useCanAdmin() {
  const { user } = useAuthContext()
  if (!user) return false
  return roleCanAdmin(user.role, user.is_superuser)
}
