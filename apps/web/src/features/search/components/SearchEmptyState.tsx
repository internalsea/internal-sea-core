type SearchEmptyVariant = 'no-query' | 'short-query' | 'no-results'

interface SearchEmptyStateProps {
  variant: SearchEmptyVariant
}

const messages: Record<SearchEmptyVariant, string> = {
  'no-query': 'Start typing to search.',
  'short-query': 'Type at least 2 characters.',
  'no-results': 'No results found.',
}

export function SearchEmptyState({ variant }: SearchEmptyStateProps) {
  return <p className="px-4 py-6 text-center text-sm text-gray-500">{messages[variant]}</p>
}
