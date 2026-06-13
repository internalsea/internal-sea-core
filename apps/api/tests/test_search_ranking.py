import uuid
from datetime import UTC, datetime

from app.modules.search.ranking import compute_match_rank, sort_search_results
from app.modules.search.schemas import SearchResult, SearchResultType


def _result(title: str, *, matched_field: str | None = None) -> SearchResult:
    now = datetime.now(UTC)
    return SearchResult(
        id=uuid.uuid4(),
        type=SearchResultType.TEAM,
        title=title,
        url="/teams/example",
        matched_field=matched_field,
        updated_at=now,
    )


def test_compute_match_rank_exact_before_contains() -> None:
    assert compute_match_rank("sales", "Sales", "name") < compute_match_rank(
        "sales",
        "Executive Sales Dashboard",
        "name",
    )


def test_sort_search_results_prioritizes_exact_match() -> None:
    results = sort_search_results(
        "data",
        [
            _result("Platform Data Team", matched_field="name"),
            _result("Data Engineering", matched_field="name"),
        ],
    )

    assert results[0].title == "Data Engineering"
