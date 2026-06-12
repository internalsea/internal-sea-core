from app.db.base import Base
from app.domain.enums import (
    CommentEntityType,
    DataProductStatus,
    DataProductType,
    QualityStatus,
    SeniorityLevel,
    UserRole,
    WorkItemPriority,
    WorkItemStatus,
    WorkItemType,
)
from app.models import (
    ActivityEvent,
    BusinessDomain,
    Capability,
    Comment,
    DataProduct,
    EntityLink,
    Person,
    Project,
    SystemInfo,
    Team,
    User,
    WorkItem,
)


def test_all_models_can_be_imported() -> None:
    models = [
        SystemInfo,
        User,
        Person,
        Team,
        Capability,
        BusinessDomain,
        DataProduct,
        WorkItem,
        Comment,
        Project,
        ActivityEvent,
        EntityLink,
    ]
    assert len(models) == 12
    for model in models:
        assert hasattr(model, "__tablename__")


def test_base_metadata_contains_expected_tables() -> None:
    table_names = set(Base.metadata.tables.keys())
    expected = {
        "system_info",
        "users",
        "people",
        "teams",
        "capabilities",
        "business_domains",
        "data_products",
        "work_items",
        "comments",
        "projects",
        "activity_events",
        "entity_links",
    }
    assert expected.issubset(table_names)


def test_user_role_enum_values() -> None:
    assert UserRole.ADMIN.value == "admin"
    assert UserRole.EDITOR.value == "editor"
    assert UserRole.VIEWER.value == "viewer"


def test_seniority_level_enum_values() -> None:
    assert SeniorityLevel.SENIOR.value == "senior"
    assert SeniorityLevel.LEAD.value == "lead"


def test_data_product_enums() -> None:
    assert DataProductType.DATASET.value == "dataset"
    assert DataProductStatus.DRAFT.value == "draft"
    assert QualityStatus.UNKNOWN.value == "unknown"


def test_work_item_enums() -> None:
    assert WorkItemType.TASK.value == "task"
    assert WorkItemStatus.BACKLOG.value == "backlog"
    assert WorkItemPriority.MEDIUM.value == "medium"


def test_comment_entity_type_enum_values() -> None:
    assert CommentEntityType.DATA_PRODUCT.value == "data_product"
    assert CommentEntityType.WORK_ITEM.value == "work_item"


def test_migration_revision_chain_is_present() -> None:
    from pathlib import Path

    versions_dir = Path(__file__).resolve().parents[1] / "alembic" / "versions"
    migration_files = sorted(versions_dir.glob("0*.py"))
    assert any(path.name.startswith("0001") for path in migration_files)
    assert any(path.name.startswith("0002") for path in migration_files)
    assert any(path.name.startswith("0003") for path in migration_files)
    assert any(path.name.startswith("0004") for path in migration_files)
    assert any(path.name.startswith("0005") for path in migration_files)
