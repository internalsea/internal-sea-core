from decimal import Decimal
from types import SimpleNamespace

from app.domain.enums import MetricDirection, PerformanceTrend
from app.modules.performance.scoring import (
    calculate_metric_score,
    calculate_trend,
    interpret_metric,
)


def _definition(**kwargs):
    defaults = {
        "target_value": Decimal("90"),
        "direction": MetricDirection.HIGHER_IS_BETTER.value,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _value(numeric):
    return SimpleNamespace(value_numeric=Decimal(str(numeric)), value_text=None, value_bool=None)


def test_score_calculation_higher_is_better() -> None:
    definition = _definition(direction=MetricDirection.HIGHER_IS_BETTER.value, target_value=Decimal("90"))
    score = calculate_metric_score(definition, _value(92))
    assert score == Decimal("102.22")


def test_score_calculation_lower_is_better() -> None:
    definition = _definition(direction=MetricDirection.LOWER_IS_BETTER.value, target_value=Decimal("10"))
    score = calculate_metric_score(definition, _value(8))
    assert score == Decimal("120.00")


def test_trend_calculation_up() -> None:
    assert calculate_trend(Decimal("90"), Decimal("80"), MetricDirection.HIGHER_IS_BETTER) == PerformanceTrend.UP


def test_trend_calculation_stable() -> None:
    assert calculate_trend(Decimal("90"), Decimal("90"), MetricDirection.HIGHER_IS_BETTER) == PerformanceTrend.STABLE


def test_trend_calculation_unknown() -> None:
    assert calculate_trend(None, Decimal("80"), MetricDirection.HIGHER_IS_BETTER) == PerformanceTrend.UNKNOWN


def test_interpret_metric_no_target() -> None:
    definition = _definition(target_value=None)
    assert interpret_metric(definition, _value(50), None) == "No target defined"
