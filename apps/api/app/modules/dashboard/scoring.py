"""Transparent health score helpers for the advanced dashboard.

Scores are simple heuristics for operational visibility — not official compliance ratings.
"""

from __future__ import annotations


def calculate_status_from_score(score: int | float | None) -> str:
    if score is None:
        return "unknown"
    if score >= 85:
        return "good"
    if score >= 70:
        return "warning"
    return "critical"


def _clamp_score(value: float) -> int:
    return max(0, min(100, int(round(value))))


def calculate_work_health_score(
    *,
    open_work_items: int,
    overdue_work_items: int,
    critical_items: int,
    risks: int,
) -> int | None:
    if open_work_items == 0 and overdue_work_items == 0 and critical_items == 0 and risks == 0:
        return None
    # Start at 100; subtract weighted penalties for delivery pressure.
    score = 100.0
    score -= min(overdue_work_items * 8, 40)
    score -= min(critical_items * 6, 30)
    score -= min(risks * 5, 20)
    if open_work_items > 0:
        overdue_ratio = overdue_work_items / open_work_items
        score -= min(overdue_ratio * 30, 20)
    return _clamp_score(score)


def calculate_compliance_health_score(
    *,
    checks_open: int,
    checks_non_compliant: int,
    checks_overdue: int,
    evidence_missing: int,
) -> int | None:
    if checks_open == 0 and checks_non_compliant == 0 and checks_overdue == 0:
        return None
    score = 100.0
    score -= min(checks_non_compliant * 15, 45)
    score -= min(checks_overdue * 10, 35)
    score -= min(evidence_missing * 8, 25)
    return _clamp_score(score)


def calculate_project_health_score(
    *,
    active_projects: int,
    warning_or_critical: int,
    overdue_or_at_risk: int,
) -> int | None:
    if active_projects == 0:
        return None
    score = 100.0
    if active_projects > 0:
        score -= min((warning_or_critical / active_projects) * 50, 40)
        score -= min((overdue_or_at_risk / active_projects) * 40, 35)
    return _clamp_score(score)


def calculate_automation_health_score(
    *,
    runs_failed: int,
    due_triggers: int,
    locked_triggers: int,
) -> int | None:
    if runs_failed == 0 and due_triggers == 0 and locked_triggers == 0:
        return None
    score = 100.0
    score -= min(runs_failed * 10, 40)
    score -= min(due_triggers * 5, 30)
    score -= min(locked_triggers * 3, 15)
    return _clamp_score(score)


def calculate_performance_health_score(average_score: float | None) -> int | None:
    if average_score is None:
        return None
    return _clamp_score(average_score)


def calculate_overall_score(*scores: int | None) -> int | None:
    available = [score for score in scores if score is not None]
    if not available:
        return None
    return _clamp_score(sum(available) / len(available))
