from app.core.pagination import calculate_pages, normalize_pagination


def test_normalize_pagination_clamps_page_size() -> None:
    page, page_size = normalize_pagination(0, 500)
    assert page == 1
    assert page_size == 100


def test_calculate_pages() -> None:
    assert calculate_pages(0, 20) == 0
    assert calculate_pages(1, 20) == 1
    assert calculate_pages(21, 20) == 2
