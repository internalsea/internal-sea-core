export interface NavigationItem {
  label: string
  path: string
}

export interface PrimaryNavGroup {
  id: string
  label: string
  items: NavigationItem[]
}

export const primaryNavGroups: PrimaryNavGroup[] = [
  {
    id: 'home',
    label: 'Home',
    items: [{ label: 'Dashboard', path: '/dashboard' }],
  },
  {
    id: 'work',
    label: 'Work',
    items: [
      { label: 'Work Board', path: '/work-board' },
      { label: 'Work Items', path: '/work-items' },
      { label: 'Projects', path: '/projects' },
      { label: 'Internal Projects', path: '/internal-projects' },
      { label: 'Activities', path: '/activities' },
      { label: 'Deals', path: '/deals' },
    ],
  },
  {
    id: 'organization',
    label: 'Organization',
    items: [
      { label: 'People', path: '/people' },
      { label: 'Teams', path: '/teams' },
      { label: 'Capabilities', path: '/capabilities' },
      { label: 'Performance', path: '/performance' },
    ],
  },
  {
    id: 'data',
    label: 'Data',
    items: [
      { label: 'Data Products', path: '/data-products' },
      { label: 'Governance', path: '/compliance' },
      { label: 'Compliance', path: '/compliance' },
      { label: 'Policies', path: '/policies' },
    ],
  },
]

export interface SettingsLinkItem {
  label: string
  path: string
  description: string
}

export const operationsSettingsLinks: SettingsLinkItem[] = [
  {
    label: 'Automation',
    path: '/automation',
    description: 'Schedules, triggers, and operational workflows.',
  },
  {
    label: 'Meetings',
    path: '/meetings',
    description: 'Governance, delivery, and planning meetings.',
  },
  {
    label: 'Files',
    path: '/files',
    description: 'File metadata, attachments, and document management.',
  },
  {
    label: 'Tools',
    path: '/tools',
    description: 'Operational tools and supporting integrations.',
  },
]

export const notificationsSettingsLinks: SettingsLinkItem[] = [
  {
    label: 'Notifications',
    path: '/notifications',
    description: 'Channels, templates, messages, and delivery preferences.',
  },
]

export const createActionLinks: NavigationItem[] = [
  { label: 'Work item', path: '/work-items/new' },
  { label: 'Project', path: '/projects/new' },
  { label: 'Internal project', path: '/internal-projects/new' },
  { label: 'Person', path: '/people/new' },
  { label: 'Data product', path: '/data-products/new' },
]

export function pathMatches(pathname: string, path: string): boolean {
  if (path === '/dashboard') {
    return pathname === '/' || pathname === '/dashboard'
  }
  return pathname === path || pathname.startsWith(`${path}/`)
}

export function isNavGroupActive(pathname: string, group: PrimaryNavGroup): boolean {
  return group.items.some((item) => pathMatches(pathname, item.path))
}

export function isSettingsPageActive(pathname: string): boolean {
  return pathname === '/settings' || pathname.startsWith('/settings/')
}

export function isNotificationsPageActive(pathname: string): boolean {
  return pathname === '/notifications' || pathname.startsWith('/notifications/')
}
