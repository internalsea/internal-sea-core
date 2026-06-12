from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.enums import NotificationChannelType, NotificationEventType
from app.modules.notifications.schemas import (
    NotificationChannelCreate,
    NotificationMessageCreate,
    NotificationPreferenceCreate,
    NotificationTemplateCreate,
)


def test_channel_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        NotificationChannelCreate(name="", channel_type=NotificationChannelType.IN_APP)


def test_channel_provider_config_rejects_secret_keys() -> None:
    with pytest.raises(ValidationError):
        NotificationChannelCreate(
            name="Test",
            channel_type=NotificationChannelType.EMAIL,
            provider_config={"api_key": "secret"},
        )


def test_template_create_rejects_empty_body() -> None:
    with pytest.raises(ValidationError):
        NotificationTemplateCreate(name="Test", body_template="")


def test_message_create_requires_body() -> None:
    with pytest.raises(ValidationError):
        NotificationMessageCreate(body="")


def test_preference_requires_user_or_person() -> None:
    with pytest.raises(ValidationError):
        NotificationPreferenceCreate(
            channel_type=NotificationChannelType.IN_APP,
            event_type=NotificationEventType.MANUAL,
        )


def test_message_entity_pair_validation() -> None:
    with pytest.raises(ValidationError):
        NotificationMessageCreate(body="Hello", entity_type="data_product")

    with pytest.raises(ValidationError):
        NotificationMessageCreate(body="Hello", entity_id=uuid4())
