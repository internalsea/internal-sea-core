export function confirmTeamDelete(name: string): boolean {
  return window.confirm(
    `Delete this team?\n\n"${name}"\n\nThis action cannot be undone. Teams with linked people, work items, projects or data products cannot be deleted.`,
  )
}
