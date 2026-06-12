export function confirmCapabilityDelete(name: string): boolean {
  return window.confirm(
    `Delete this capability?\n\n"${name}"\n\nThis action cannot be undone. Capabilities with linked people, work items, projects or data products cannot be deleted.`,
  )
}
