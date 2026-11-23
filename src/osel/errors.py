"""Error types. Each carries the CLI exit code it maps to."""

from __future__ import annotations

EXIT_OK = 0
EXIT_REGRESSION = 1
EXIT_INVALID_INPUT = 2
EXIT_INTERNAL_ERROR = 3


class OselError(Exception):
    """Base class for expected OSEL errors."""

    exit_code = EXIT_INTERNAL_ERROR

    def __init__(self, message: str, details: list[str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = list(details or [])

    def __str__(self) -> str:
        if not self.details:
            return self.message
        shown = self.details[:20]
        more = len(self.details) - len(shown)
        lines = [self.message, *(f"  - {d}" for d in shown)]
        if more > 0:
            lines.append(f"  ... and {more} more")
        return "\n".join(lines)


class InvalidInputError(OselError):
    """User-supplied input (dataset, config, run file, arguments) is invalid."""

    exit_code = EXIT_INVALID_INPUT


class IncompatibleRunsError(InvalidInputError):
    """Two runs cannot be compared meaningfully."""


class MetricError(Exception):
    """Raised by a metric when an example cannot be scored."""
