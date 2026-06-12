from datetime import datetime, timedelta, timezone

from app.worker.locks import is_lock_expired


def test_is_lock_expired_when_none() -> None:
    assert is_lock_expired(None) is True


def test_is_lock_expired_when_past() -> None:
    past = datetime.now(timezone.utc) - timedelta(minutes=5)
    assert is_lock_expired(past) is True


def test_is_lock_expired_when_future() -> None:
    future = datetime.now(timezone.utc) + timedelta(minutes=5)
    assert is_lock_expired(future) is False


def test_lock_update_statement_shape() -> None:
    from sqlalchemy import update

    from app.models.automation import AutomationTrigger

    stmt = update(AutomationTrigger).where(AutomationTrigger.id.is_not(None))
    compiled = str(stmt)
    assert "automation_triggers" in compiled
