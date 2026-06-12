from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.dependencies import get_db
from app.worker.health import get_due_work_summary, get_worker_status
from app.worker.runner import WorkerRunner
from app.worker.schemas import DueWorkSummary, WorkerCycleResult, WorkerStatus

router = APIRouter(prefix="/worker", tags=["Worker"])


@router.get("/status", response_model=WorkerStatus)
async def worker_status(
    _user: ViewerUser,
    db: AsyncSession = Depends(get_db),
) -> WorkerStatus:
    return await get_worker_status(db)


@router.get("/due-work", response_model=DueWorkSummary)
async def worker_due_work(
    _user: ViewerUser,
    db: AsyncSession = Depends(get_db),
) -> DueWorkSummary:
    return await get_due_work_summary(db)


@router.post("/run-once", response_model=WorkerCycleResult)
async def worker_run_once(
    _user: EditorUser,
    db: AsyncSession = Depends(get_db),
) -> WorkerCycleResult:
    runner = WorkerRunner(db)
    return await runner.run_once()
