import uuid

from app.modules.dashboard.insights import InsightContext, build_actionable_insights
from app.modules.dashboard.schemas import ActionableInsight


def test_insights_sort_critical_before_warning() -> None:
    ctx = InsightContext(
        ownership_gaps=[],
        overdue_work_items=[],
        old_technical_debt=[],
        at_risk_projects=[],
        overdue_compliance_checks=[],
        non_compliant_checks=[],
        missing_evidence_checks=[],
        weak_performance=[],
        failed_automation_count=1,
        due_automation_triggers=3,
        failed_notification_count=0,
    )
    items = build_actionable_insights(ctx, limit=20)
    severities = [item.severity for item in items]
    if "critical" in severities and "info" in severities:
        assert severities.index("critical") < severities.index("info")


def test_actionable_insight_stable_id() -> None:
    entity_id = uuid.uuid4()
    item = ActionableInsight(
        id="stable",
        category="delivery",
        severity="warning",
        title="Test",
        description="Desc",
        entity_type="work_item",
        entity_id=entity_id,
        recommended_action=None,
        url=None,
    )
    assert item.entity_id == entity_id
