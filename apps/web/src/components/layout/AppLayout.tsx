import { Outlet } from 'react-router-dom'

import { AppWaveBackground } from '@/components/layout/AppWaveBackground'
import { TopBar } from '@/components/layout/TopBar'
import { AiCommandBar } from '@/features/search/components/AiCommandBar'

export function AppLayout() {
  return (
    <div className="relative flex h-screen flex-col bg-auth-background">
      <AppWaveBackground />
      <div className="relative z-10 flex min-h-0 flex-1 flex-col">
        <TopBar />
        <main className="flex-1 overflow-y-auto p-6 pb-28">
          <Outlet />
        </main>
        <AiCommandBar />
      </div>
    </div>
  )
}
