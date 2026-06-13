export interface NavigationItem {
  label: string
  path: string
}

export interface NavigationGroup {
  title: string
  items: NavigationItem[]
}

export const navigationGroups: NavigationGroup[] = [
  {
    title: 'Today',
    items: [
      { label: 'Dashboard', path: '/dashboard' },
      { label: 'Data Products', path: '/data-products' },
    ],
  },
  {
    title: 'Activities',
    items: [
      { label: 'Work Items', path: '/work-items' },
      { label: 'Work Board', path: '/work-board' },
      { label: 'Projects', path: '/projects' },
      { label: 'Internal Projects', path: '/internal-projects' },
    ],
  },
  {
    title: 'Organization',
    items: [
      { label: 'People', path: '/people' },
      { label: 'Teams', path: '/teams' },
      { label: 'Capabilities', path: '/capabilities' },
      { label: 'Performance', path: '/performance' },
    ],
  },
  {
    title: 'Governance',
    items: [
      { label: 'Compliance', path: '/compliance' },
      { label: 'Policies', path: '/policies' },
      { label: 'Tools', path: '/tools' },
    ],
  },
  {
    title: 'Operations',
    items: [
      { label: 'Automation', path: '/automation' },
      { label: 'Notifications', path: '/notifications' },
      { label: 'Meetings', path: '/meetings' },
      { label: 'Deals', path: '/deals' },
      { label: 'Files', path: '/files' },
      { label: 'Settings', path: '/settings' },
    ],
  },
  {
    title: 'Settings',
    items: [
      { label: 'Company Settings', path: '/settings/company' },
      { label: 'Workspace Settings', path: '/settings/workspace' },
    ],
  },
]
