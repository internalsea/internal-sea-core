"""Slug and validation helpers for tenancy."""

import re
import unicodedata

_SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


def slugify_name(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name.strip().lower())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = _SLUG_PATTERN.sub("-", ascii_text).strip("-")
    return slug or "company"


def ensure_unique_slug(base_slug: str, existing_slugs: set[str]) -> str:
    if base_slug not in existing_slugs:
        return base_slug
    counter = 2
    while f"{base_slug}-{counter}" in existing_slugs:
        counter += 1
    return f"{base_slug}-{counter}"
