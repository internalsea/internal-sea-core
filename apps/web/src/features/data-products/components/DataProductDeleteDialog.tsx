export function confirmDataProductDelete(name: string): boolean {
  return window.confirm(
    `Delete this data product?\n\n"${name}"\n\nThis action cannot be undone.`,
  )
}
