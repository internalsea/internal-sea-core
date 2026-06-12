from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.modules.activity.repository import ActivityRepository
from app.modules.activity.service import ActivityService


def get_activity_service(db: AsyncSession = Depends(get_db)) -> ActivityService:
    return ActivityService(ActivityRepository(db))


def build_activity_service(session: AsyncSession) -> ActivityService:
    return ActivityService(ActivityRepository(session))
