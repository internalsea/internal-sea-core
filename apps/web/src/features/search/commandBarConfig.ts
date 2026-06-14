export type CommandActionPermission = 'viewer' | 'editor'

export interface CommandHintChip {
  label: string
  query: string
}

export interface CommandQuickAction {
  label: string
  path: string
  description?: string
  require?: CommandActionPermission
}

export const COMMAND_HINT_CHIPS: CommandHintChip[] = [
  { label: 'Projects', query: 'project' },
  { label: 'People', query: 'people' },
  { label: 'Reports', query: 'report' },
  { label: 'Deals', query: 'deal' },
]

export const COMMAND_QUICK_ACTIONS: CommandQuickAction[] = [
  {
    label: 'Search projects',
    path: '/projects',
    description: 'Open the projects directory',
  },
  {
    label: 'Search people',
    path: '/people',
    description: 'Browse people and ownership',
  },
  {
    label: 'Open reports',
    path: '/reports/capabilities',
    description: 'Capability, project, and deal reports',
  },
  {
    label: 'Open compliance dashboard',
    path: '/compliance',
    description: 'Policies, checks, and evidence',
  },
  {
    label: 'Create work item',
    path: '/work-items/new',
    description: 'Add a new work item',
    require: 'editor',
  },
  {
    label: 'Create project',
    path: '/projects/new',
    description: 'Start a new project',
    require: 'editor',
  },
]

export const COMMAND_SUGGESTED_PROMPTS: string[] = [
  'Show delayed projects',
  'Find people in Data Engineering',
  'Open capability reports',
  'Show deals without next meeting',
  'Create a project',
  'Summarize team performance',
]

export function isMacPlatform(): boolean {
  if (typeof navigator === 'undefined') {
    return false
  }
  return /Mac|iPhone|iPod|iPad/i.test(navigator.platform)
}
