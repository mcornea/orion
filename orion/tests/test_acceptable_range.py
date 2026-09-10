"""Tests for acceptable value range filtering."""

from orion.algorithms.edivisive.edivisive import EDivisive
from orion.algorithms.cmr.cmr import CMR
from orion.tests.conftest import make_change_point


def _algorithm(metric_config):
    algorithm = object.__new__(EDivisive)
    algorithm.metrics_config = {"metric": metric_config}
    return algorithm


def test_steps_outside_acceptable_range():
    algorithm = _algorithm({"acceptable_range": (0.0, 10.0)})
    change_point = make_change_point("metric", 1, mean_1=5.0, mean_2=11.0)

    assert algorithm._steps_outside_acceptable_range("metric", change_point)


def test_changes_inside_or_back_into_range_are_ignored():
    algorithm = _algorithm({"acceptable_range": (0.0, 10.0)})

    inside = make_change_point("metric", 1, mean_1=5.0, mean_2=8.0)
    back_inside = make_change_point("metric", 1, mean_1=12.0, mean_2=8.0)

    assert not algorithm._steps_outside_acceptable_range("metric", inside)
    assert not algorithm._steps_outside_acceptable_range("metric", back_inside)


def test_cmr_range_crossing_ignores_direction_and_percentage_threshold():
    algorithm = CMR.__new__(CMR)
    algorithm.metrics_config = {
        "metric": {
            "direction": 1,
            "threshold": 100,
            "acceptable_range": (0.0, 10.0),
        }
    }
    change_point = make_change_point("metric", 1, mean_1=5.0, mean_2=-1.0)

    assert algorithm._steps_outside_acceptable_range("metric", change_point)
