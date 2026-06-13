import { Outlet } from 'react-router-dom'

import { TopBar } from '@/components/layout/TopBar'

export function AppLayout() {
  return (
    <div className="flex h-screen flex-col bg-app-background">
      <TopBar />
      <main className="flex-1 overflow-y-auto p-6">
        <Outlet />
      </main>
    </div>
  )
}
