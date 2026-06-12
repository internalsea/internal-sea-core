export function confirmProjectDelete(name: string, variant: 'projects' | 'internal-projects' = 'projects'): boolean {
  const label = variant === 'internal-projects' ? 'internal project' : 'project'
  return window.confirm(
    `Delete this ${label}?\n\n"${name}"\n\nThis action cannot be undone.`,
  )
}
