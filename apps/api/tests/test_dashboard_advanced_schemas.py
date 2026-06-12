from datetime import datetime, timezone

from app.modules.dashboard.schemas import ActionableInsight, ExecutiveSummary


def test_executive_summary_schema() -> None:
    summary = ExecutiveSummary(
        overall_status="good",
        overall_score=88,
        active_projects=2,
        active_internal_projects=1,
        active_data_products=5,
        open_work_items=10,
        overdue_work_items=1,
        compliance_open_checks=2,
        compliance_overdue_checks=0,
        average_performance_score=82.5,
        ownership_gaps=1,
        automation_due_triggers=0,
        notification_failed_messages=0,
        generated_at=datetime.now(timezone.utc),
    )
    assert summary.overall_score == 88


def test_actionable_insight_schema() -> None:
    insight = ActionableInsight(
        id="abc123",
        category="ownership",
        severity="critical",
        title="Missing owner",
        description="Test",
        entity_type="data_product",
        entity_id=None,
        recommended_action="Assign owner",
        url="/data-products/1",
    )
    assert insight.severity == "critical"
