export function confirmWorkItemDelete(title: string): boolean {
  return window.confirm(
    `Delete this work item?\n\n"${title}"\n\nThis action cannot be undone.`,
  )
}
