"""Simple search result ranking helpers."""

from __future__ import annotations

from app.modules.search.schemas import SearchResult


def compute_match_rank(query: str, title: str, matched_field: str | None) -> int:
    normalized_query = query.casefold()
    normalized_title = title.casefold()

    if normalized_title == normalized_query:
        return 0
    if normalized_title.startswith(normalized_query):
        return 1
    if normalized_query in normalized_title:
        return 2
    if matched_field in {"name", "title", "full_name"}:
        return 3
    return 4


def sort_search_results(query: str, results: list[SearchResult]) -> list[SearchResult]:
    return sorted(
        results,
        key=lambda result: (
            compute_match_rank(query, result.title, result.matched_field),
            -(result.updated_at.timestamp() if result.updated_at else 0),
            result.title.casefold(),
        ),
    )


def detect_matched_field(
    query: str,
    fields: dict[str, str | None],
) -> str | None:
    normalized_query = query.casefold()
    for field_name, field_value in fields.items():
        if field_value and normalized_query in field_value.casefold():
            return field_name
    return None
