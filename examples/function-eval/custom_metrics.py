"""A custom metric: implement name, version, higher_is_better and score()."""

from osel.errors import MetricError


class WithinTolerance:
    """1.0 if |prediction - reference| <= tolerance, else 0.0."""

    version = "1"
    higher_is_better = True

    def __init__(self, tolerance: float = 1e-9, name: str = "within_tolerance") -> None:
        self.tolerance = tolerance
        self.name = name

    def score(self, prediction, example) -> float:
        if not example.has_reference:
            raise MetricError("needs a reference")
        return float(abs(float(prediction) - float(example.reference)) <= self.tolerance)
