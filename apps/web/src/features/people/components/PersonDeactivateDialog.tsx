export function confirmPersonDeactivate(fullName: string): boolean {
  return window.confirm(
    `Deactivate this person?\n\n"${fullName}"\n\nThis keeps historical links to work, projects and data products.`,
  )
}
