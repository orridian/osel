from __future__ import annotations

import math

import pytest

from osel.errors import InvalidInputError, MetricError
from osel.metrics import (
    AbsError,
    Contains,
    ExactMatch,
    TokenF1,
    check_score,
    resolve_metric,
)
from osel.schema import Example


def ex(ref: object = "Paris", has_ref: bool = True) -> Example:
    return Example("id", "q", ref, {}, has_ref)


def test_exact_match() -> None:
    m = ExactMatch()
    assert m.score(" Paris ", ex()) == 1.0
    assert m.score("paris", ex()) == 0.0
    assert ExactMatch(normalize=True).score("  PARIS ", ex()) == 1.0
    assert m.score([1, 2], ex([1, 2])) == 1.0
    with pytest.raises(MetricError):
        m.score("x", ex(has_ref=False))


def test_contains() -> None:
    assert Contains().score("The capital is Paris.", ex()) == 1.0
    assert Contains().score("Lyon", ex()) == 0.0


def test_token_f1_reference_values() -> None:
    f1 = TokenF1()
    assert f1.score("New Delhi", ex("New Delhi")) == 1.0
    assert math.isclose(f1.score("Delhi", ex("New Delhi")), 2 / 3)
    # pred: a b c c ; ref: a c d -> overlap a,c = 2; p = 2/4, r = 2/3; f1 = 4/7
    assert math.isclose(f1.score("a b c c", ex("a c d")), 4 / 7)
    assert f1.score("", ex("")) == 1.0
    assert f1.score("x", ex("")) == 0.0


def test_abs_error() -> None:
    m = AbsError()
    assert m.higher_is_better is False
    assert m.score("2.5", ex(1)) == 1.5
    with pytest.raises(MetricError):
        m.score("abc", ex(1))


def test_check_score() -> None:
    assert check_score(True) == 1.0
    for bad in (float("nan"), float("inf"), "1", None):
        with pytest.raises(MetricError):
            check_score(bad)


def test_resolve_metric_forms() -> None:
    assert resolve_metric("exact_match").name == "exact_match"
    m = resolve_metric({"use": "exact_match", "params": {"normalize": True, "name": "em_norm"}})
    assert m.name == "em_norm"
    custom = resolve_metric("osel.metrics:TokenF1")
    assert custom.name == "token_f1"
    with pytest.raises(InvalidInputError, match="unknown metric"):
        resolve_metric("nope")
    with pytest.raises(InvalidInputError, match="invalid params"):
        resolve_metric({"use": "exact_match", "params": {"bogus": 1}})
    with pytest.raises(InvalidInputError, match="cannot import"):
        resolve_metric("no_such_module_xyz:Thing")
