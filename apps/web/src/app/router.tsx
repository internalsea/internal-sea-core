import { Navigate, Outlet, createBrowserRouter } from 'react-router-dom'

import { AuthProvider } from '@/app/AuthProvider'
import { AppProviders } from '@/app/providers'
import { TenancyProvider } from '@/app/TenancyProvider'
import { AppLayout } from '@/components/layout/AppLayout'
import { AutomationPage } from '@/pages/AutomationPage'
import { AutomationScheduleCreatePage } from '@/pages/AutomationScheduleCreatePage'
import { AutomationScheduleEditPage } from '@/pages/AutomationScheduleEditPage'
import { AutomationTriggerCreatePage } from '@/pages/AutomationTriggerCreatePage'
import { AutomationTriggerDetailPage } from '@/pages/AutomationTriggerDetailPage'
import { AutomationTriggerEditPage } from '@/pages/AutomationTriggerEditPage'
import { ProtectedRoute } from '@/features/auth/components/ProtectedRoute'
import { CapabilitiesPage } from '@/pages/CapabilitiesPage'
import { CapabilityCreatePage } from '@/pages/CapabilityCreatePage'
import { CapabilityDetailPage } from '@/pages/CapabilityDetailPage'
import { CapabilityEditPage } from '@/pages/CapabilityEditPage'
import { ComplianceCheckCreatePage } from '@/pages/ComplianceCheckCreatePage'
import { ComplianceCheckDetailPage } from '@/pages/ComplianceCheckDetailPage'
import { ComplianceCheckEditPage } from '@/pages/ComplianceCheckEditPage'
import { CompanySettingsPage } from '@/pages/CompanySettingsPage'
import { CompliancePage } from '@/pages/CompliancePage'
import { PolicyCreatePage } from '@/pages/PolicyCreatePage'
import { PolicyDetailPage } from '@/pages/PolicyDetailPage'
import { PolicyEditPage } from '@/pages/PolicyEditPage'
import { DashboardPage } from '@/pages/DashboardPage'
import { DataProductDetailPage } from '@/pages/DataProductDetailPage'
import { DataProductsPage } from '@/pages/DataProductsPage'
import { DealsPage } from '@/pages/DealsPage'
import { FileCreatePage } from '@/pages/FileCreatePage'
import { FileDetailPage } from '@/pages/FileDetailPage'
import { FileEditPage } from '@/pages/FileEditPage'
import { FilesPage } from '@/pages/FilesPage'
import { FirstUserOnboardingPage } from '@/pages/FirstUserOnboardingPage'
import { InternalProjectCreatePage } from '@/pages/InternalProjectCreatePage'
import { InternalProjectDetailPage } from '@/pages/InternalProjectDetailPage'
import { InternalProjectEditPage } from '@/pages/InternalProjectEditPage'
import { InternalProjectsPage } from '@/pages/InternalProjectsPage'
import { LoginPage } from '@/pages/LoginPage'
import { ProjectCreatePage } from '@/pages/ProjectCreatePage'
import { ProjectDetailPage } from '@/pages/ProjectDetailPage'
import { ProjectEditPage } from '@/pages/ProjectEditPage'
import { NotificationMessageCreatePage } from '@/pages/NotificationMessageCreatePage'
import { NotificationMessageDetailPage } from '@/pages/NotificationMessageDetailPage'
import { NotificationMessageEditPage } from '@/pages/NotificationMessageEditPage'
import { NotificationTemplateCreatePage } from '@/pages/NotificationTemplateCreatePage'
import { NotificationTemplateDetailPage } from '@/pages/NotificationTemplateDetailPage'
import { NotificationTemplateEditPage } from '@/pages/NotificationTemplateEditPage'
import { NotificationsPage } from '@/pages/NotificationsPage'
import { MeetingsPage } from '@/pages/MeetingsPage'
import { NotFoundPage } from '@/pages/NotFoundPage'
import { PeoplePage } from '@/pages/PeoplePage'
import { PersonCreatePage } from '@/pages/PersonCreatePage'
import { PersonDetailPage } from '@/pages/PersonDetailPage'
import { PersonEditPage } from '@/pages/PersonEditPage'
import { MetricDefinitionCreatePage } from '@/pages/MetricDefinitionCreatePage'
import { MetricDefinitionDetailPage } from '@/pages/MetricDefinitionDetailPage'
import { MetricDefinitionEditPage } from '@/pages/MetricDefinitionEditPage'
import { MetricValueCreatePage } from '@/pages/MetricValueCreatePage'
import { MetricValueEditPage } from '@/pages/MetricValueEditPage'
import { PerformancePage } from '@/pages/PerformancePage'
import { PoliciesPage } from '@/pages/PoliciesPage'
import { ProjectsPage } from '@/pages/ProjectsPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { TeamCreatePage } from '@/pages/TeamCreatePage'
import { TeamDetailPage } from '@/pages/TeamDetailPage'
import { TeamEditPage } from '@/pages/TeamEditPage'
import { TeamsPage } from '@/pages/TeamsPage'
import { ToolsPage } from '@/pages/ToolsPage'
import { WorkBoardPage } from '@/pages/WorkBoardPage'
import { WorkItemCreatePage } from '@/pages/WorkItemCreatePage'
import { WorkItemDetailPage } from '@/pages/WorkItemDetailPage'
import { WorkItemEditPage } from '@/pages/WorkItemEditPage'
import { WorkItemsPage } from '@/pages/WorkItemsPage'
import { WorkspaceSettingsPage } from '@/pages/WorkspaceSettingsPage'

function RootProviders() {
  return (
    <AppProviders>
      <AuthProvider>
        <TenancyProvider>
          <Outlet />
        </TenancyProvider>
      </AuthProvider>
    </AppProviders>
  )
}

export const router = createBrowserRouter([
  {
    element: <RootProviders />,
    children: [
      { path: 'login', element: <LoginPage /> },
      { path: 'onboarding/first-user', element: <FirstUserOnboardingPage /> },
      {
        path: '/',
        element: (
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        ),
        children: [
          { index: true, element: <Navigate to="/dashboard" replace /> },
          { path: 'dashboard', element: <DashboardPage /> },
          { path: 'data-products/:id', element: <DataProductDetailPage /> },
          { path: 'data-products', element: <DataProductsPage /> },
          { path: 'work-items/new', element: <WorkItemCreatePage /> },
          { path: 'work-items/:id/edit', element: <WorkItemEditPage /> },
          { path: 'work-items/:id', element: <WorkItemDetailPage /> },
          { path: 'work-items', element: <WorkItemsPage /> },
          { path: 'work-board', element: <WorkBoardPage /> },
          { path: 'projects/new', element: <ProjectCreatePage /> },
          { path: 'projects/:id/edit', element: <ProjectEditPage /> },
          { path: 'projects/:id', element: <ProjectDetailPage /> },
          { path: 'projects', element: <ProjectsPage /> },
          { path: 'internal-projects/new', element: <InternalProjectCreatePage /> },
          { path: 'internal-projects/:id/edit', element: <InternalProjectEditPage /> },
          { path: 'internal-projects/:id', element: <InternalProjectDetailPage /> },
          { path: 'internal-projects', element: <InternalProjectsPage /> },
          { path: 'people/new', element: <PersonCreatePage /> },
          { path: 'people/:id/edit', element: <PersonEditPage /> },
          { path: 'people/:id', element: <PersonDetailPage /> },
          { path: 'people', element: <PeoplePage /> },
          { path: 'teams/new', element: <TeamCreatePage /> },
          { path: 'teams/:id/edit', element: <TeamEditPage /> },
          { path: 'teams/:id', element: <TeamDetailPage /> },
          { path: 'teams', element: <TeamsPage /> },
          { path: 'capabilities/new', element: <CapabilityCreatePage /> },
          { path: 'capabilities/:id/edit', element: <CapabilityEditPage /> },
          { path: 'capabilities/:id', element: <CapabilityDetailPage /> },
          { path: 'capabilities', element: <CapabilitiesPage /> },
          { path: 'performance/metrics/new', element: <MetricDefinitionCreatePage /> },
          { path: 'performance/metrics/:id/edit', element: <MetricDefinitionEditPage /> },
          { path: 'performance/metrics/:id', element: <MetricDefinitionDetailPage /> },
          { path: 'performance/values/new', element: <MetricValueCreatePage /> },
          { path: 'performance/values/:id/edit', element: <MetricValueEditPage /> },
          { path: 'performance', element: <PerformancePage /> },
          { path: 'compliance/policies/new', element: <PolicyCreatePage /> },
          { path: 'compliance/policies/:id/edit', element: <PolicyEditPage /> },
          { path: 'compliance/policies/:id', element: <PolicyDetailPage /> },
          { path: 'compliance/checks/new', element: <ComplianceCheckCreatePage /> },
          { path: 'compliance/checks/:id/edit', element: <ComplianceCheckEditPage /> },
          { path: 'compliance/checks/:id', element: <ComplianceCheckDetailPage /> },
          { path: 'compliance', element: <CompliancePage /> },
          { path: 'policies', element: <PoliciesPage /> },
          { path: 'tools', element: <ToolsPage /> },
          { path: 'automation/triggers/new', element: <AutomationTriggerCreatePage /> },
          { path: 'automation/triggers/:id/edit', element: <AutomationTriggerEditPage /> },
          { path: 'automation/triggers/:id', element: <AutomationTriggerDetailPage /> },
          { path: 'automation/schedules/new', element: <AutomationScheduleCreatePage /> },
          { path: 'automation/schedules/:id/edit', element: <AutomationScheduleEditPage /> },
          { path: 'automation', element: <AutomationPage /> },
          { path: 'notifications/templates/new', element: <NotificationTemplateCreatePage /> },
          { path: 'notifications/templates/:id/edit', element: <NotificationTemplateEditPage /> },
          { path: 'notifications/templates/:id', element: <NotificationTemplateDetailPage /> },
          { path: 'notifications/messages/new', element: <NotificationMessageCreatePage /> },
          { path: 'notifications/messages/:id/edit', element: <NotificationMessageEditPage /> },
          { path: 'notifications/messages/:id', element: <NotificationMessageDetailPage /> },
          { path: 'notifications', element: <NotificationsPage /> },
          { path: 'meetings', element: <MeetingsPage /> },
          { path: 'deals', element: <DealsPage /> },
          { path: 'files/new', element: <FileCreatePage /> },
          { path: 'files/:id/edit', element: <FileEditPage /> },
          { path: 'files/:id', element: <FileDetailPage /> },
          { path: 'files', element: <FilesPage /> },
          { path: 'settings', element: <SettingsPage /> },
          { path: 'settings/company', element: <CompanySettingsPage /> },
          { path: 'settings/workspace', element: <WorkspaceSettingsPage /> },
          { path: '*', element: <NotFoundPage /> },
        ],
      },
    ],
  },
])
