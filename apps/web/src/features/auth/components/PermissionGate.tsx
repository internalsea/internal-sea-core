import type { ReactNode } from 'react'

import { useAuth } from '@/features/auth/hooks'
import { roleCanAdmin, roleCanWrite } from '@/features/auth/utils'

type PermissionLevel = 'viewer' | 'editor' | 'admin'

interface PermissionGateProps {
  require: PermissionLevel
  children: ReactNode
  fallback?: ReactNode
}

function hasPermission(
  require: PermissionLevel,
  role: 'admin' | 'editor' | 'viewer',
  isSuperuser: boolean,
): boolean {
  if (isSuperuser) return true
  switch (require) {
    case 'viewer':
      return true
    case 'editor':
      return roleCanWrite(role, isSuperuser)
    case 'admin':
      return roleCanAdmin(role, isSuperuser)
    default:
      return false
  }
}

export function PermissionGate({ require, children, fallback = null }: PermissionGateProps) {
  const { user } = useAuth()
  if (!user) return <>{fallback}</>
  if (!hasPermission(require, user.role, user.is_superuser)) {
    return <>{fallback}</>
  }
  return <>{children}</>
}
