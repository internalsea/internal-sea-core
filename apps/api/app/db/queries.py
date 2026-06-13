"""Small SQLAlchemy query helpers for clearer static typing."""

from __future__ import annotations

from typing import Any, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


async def get_model(
    session: AsyncSession,
    model: type[ModelT],
    primary_key: Any,
) -> ModelT | None:
    return cast(ModelT | None, await session.get(model, primary_key))
