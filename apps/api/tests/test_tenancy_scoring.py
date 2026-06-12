"""Tests for tenancy validators."""

from app.modules.tenancy.validators import ensure_unique_slug, slugify_name


def test_slugify_name() -> None:
    assert slugify_name("Internal Sea Demo") == "internal-sea-demo"
    assert slugify_name("  Hello World!  ") == "hello-world"


def test_ensure_unique_slug() -> None:
    existing = {"acme", "acme-2"}
    assert ensure_unique_slug("acme", existing) == "acme-3"
    assert ensure_unique_slug("new-co", existing) == "new-co"
