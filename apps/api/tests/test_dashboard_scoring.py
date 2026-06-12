from app.modules.dashboard.scoring import (
    calculate_automation_health_score,
    calculate_compliance_health_score,
    calculate_overall_score,
    calculate_status_from_score,
    calculate_work_health_score,
)


def test_calculate_status_from_score_mapping() -> None:
    assert calculate_status_from_score(90) == "good"
    assert calculate_status_from_score(75) == "warning"
    assert calculate_status_from_score(60) == "critical"
    assert calculate_status_from_score(None) == "unknown"


def test_work_health_score_clamps() -> None:
    score = calculate_work_health_score(
        open_work_items=10,
        overdue_work_items=5,
        critical_items=3,
        risks=2,
    )
    assert score is not None
    assert 0 <= score <= 100


def test_compliance_health_score_zero_open_data() -> None:
    assert (
        calculate_compliance_health_score(
            checks_open=0,
            checks_non_compliant=0,
            checks_overdue=0,
            evidence_missing=0,
        )
        is None
    )


def test_overall_score_averages_available() -> None:
    assert calculate_overall_score(80, 90, None) == 85
