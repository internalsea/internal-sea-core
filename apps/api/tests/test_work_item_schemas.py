import uuid

import pytest
from pydantic import ValidationError

from app.modules.work_items.schemas import WorkItemCreate, WorkItemUpdate


def test_work_item_create_accepts_project_id() -> None:
    project_id = uuid.uuid4()
    payload = WorkItemCreate(title="Link to project", project_id=project_id)
    assert payload.project_id == project_id


def test_work_item_update_accepts_project_id() -> None:
    project_id = uuid.uuid4()
    payload = WorkItemUpdate(project_id=project_id)
    data = payload.model_dump(exclude_unset=True)
    assert data == {"project_id": project_id}


def test_work_item_create_rejects_empty_title() -> None:
    with pytest.raises(ValidationError):
        WorkItemCreate(title="")
