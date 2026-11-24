"""OSEL: local-first, reproducible evaluation runs."""

from __future__ import annotations

__version__ = "0.1.0a1"

from osel.compare import Comparison, compare_runs
from osel.config import EvalConfig, load_config
from osel.dataset import Dataset, load_dataset
from osel.errors import IncompatibleRunsError, InvalidInputError, OselError
from osel.metrics import Metric
from osel.record import RunRecord, load_run, save_run
from osel.runner import run_evaluation
from osel.schema import Example

__all__ = [
    "Comparison",
    "Dataset",
    "EvalConfig",
    "Example",
    "IncompatibleRunsError",
    "InvalidInputError",
    "Metric",
    "OselError",
    "RunRecord",
    "__version__",
    "compare_runs",
    "load_config",
    "load_dataset",
    "load_run",
    "run_evaluation",
    "save_run",
]
