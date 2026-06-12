from decimal import Decimal

from app.domain.enums import MetricDirection, PerformanceTrend
from app.models.performance import PerformanceMetricDefinition, PerformanceMetricValue

STABLE_THRESHOLD = Decimal("0.01")
MAX_SCORE = Decimal("120")


def calculate_metric_score(
    definition: PerformanceMetricDefinition,
    value: PerformanceMetricValue | None,
) -> Decimal | None:
    if value is None or value.value_numeric is None:
        return None
    if definition.target_value is None or definition.target_value == 0:
        return None

    numeric_value = Decimal(str(value.value_numeric))
    target = Decimal(str(definition.target_value))
    direction = MetricDirection(definition.direction)

    if direction == MetricDirection.HIGHER_IS_BETTER:
        return min(numeric_value / target * Decimal("100"), MAX_SCORE).quantize(Decimal("0.01"))

    if direction == MetricDirection.LOWER_IS_BETTER:
        if numeric_value == 0:
            return MAX_SCORE
        return min(target / numeric_value * Decimal("100"), MAX_SCORE).quantize(Decimal("0.01"))

    if direction == MetricDirection.TARGET_IS_BEST:
        distance = abs(numeric_value - target)
        ratio = distance / target if target != 0 else distance
        score = max(Decimal("0"), Decimal("100") - ratio * Decimal("100"))
        return min(score, MAX_SCORE).quantize(Decimal("0.01"))

    return None


def calculate_trend(
    current_value: Decimal | None,
    previous_value: Decimal | None,
    direction: MetricDirection | None = None,
) -> PerformanceTrend:
    del direction
    if current_value is None or previous_value is None:
        return PerformanceTrend.UNKNOWN

    difference = current_value - previous_value
    if abs(difference) <= STABLE_THRESHOLD:
        return PerformanceTrend.STABLE
    if difference > 0:
        return PerformanceTrend.UP
    return PerformanceTrend.DOWN


def interpret_metric(
    definition: PerformanceMetricDefinition,
    value: PerformanceMetricValue | None,
    score: Decimal | None,
) -> str | None:
    if definition.target_value is None:
        return "No target defined"
    if value is None or value.value_numeric is None:
        return None

    numeric_value = Decimal(str(value.value_numeric))
    target = Decimal(str(definition.target_value))
    direction = MetricDirection(definition.direction)

    if direction == MetricDirection.NEUTRAL:
        return None

    if direction == MetricDirection.TARGET_IS_BEST:
        if abs(numeric_value - target) <= STABLE_THRESHOLD:
            return "On target"
        return "Off target"

    if numeric_value == target:
        return "On target"
    if direction == MetricDirection.HIGHER_IS_BETTER:
        return "Above target" if numeric_value > target else "Below target"
    if direction == MetricDirection.LOWER_IS_BETTER:
        return "Below target" if numeric_value < target else "Above target"

    if score is not None and score >= Decimal("100"):
        return "On target"
    return "Below target"
