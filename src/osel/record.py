"""Run records: the durable, inspectable result of one evaluation run.

A run record stores what is needed to understand and reproduce a result: run ID, timestamp,
OSEL version, (redacted) config, dataset identity, metric versions, environment metadata,
per-example scores and aggregates.

It never stores environment variables, and config values under secret-looking keys are
replaced with ``"[REDACTED]"``.
"""

from __future__ import annotations

import json
import platform
import re
import shutil
import subprocess  # noqa: S404 - used only for a fixed `git` invocation
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from osel.errors import InvalidInputError

RUN_SCHEMA_VERSION = "1"
REDACTED = "[REDACTED]"
# A key is secret if one of its words (split on non-letters and camelCase) is in this set,
# or the joined key contains one of the compound names. Whole words avoid false positives
# such as "author" or "max_tokens", which must stay visible for reproducibility.
_SECRET_WORDS = frozenset(
    {"password", "passwd", "passphrase", "secret", "token", "apikey", "credential",
     "credentials", "auth", "authorization", "cookie", "session"}
)
_SECRET_COMPOUNDS = ("apikey", "privatekey", "secretkey", "accesskey", "clientsecret")
_SECRET_VALUE = re.compile(
    r"^(sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
    r"|AKIA[0-9A-Z]{16}|xox[abpr]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{30,})$"
)


def is_secret_key(key: str) -> bool:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", key)
    words = [w.lower() for w in re.split(r"[^A-Za-z0-9]+", spaced) if w]
    joined = "".join(words)
    return any(w in _SECRET_WORDS for w in words) or any(c in joined for c in _SECRET_COMPOUNDS)


def redact(obj: Any) -> Any:
    """Recursively redact secret-looking keys and values."""
    if isinstance(obj, dict):
        return {
            k: (REDACTED if isinstance(k, str) and is_secret_key(k) else redact(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    if isinstance(obj, str) and _SECRET_VALUE.match(obj):
        return REDACTED
    return obj


def _git_info(directory: Path) -> dict[str, Any] | None:
    git = shutil.which("git")
    if git is None:
        return None
    try:
        commit = subprocess.run(  # noqa: S603 - fixed argv, no shell
            [git, "rev-parse", "HEAD"],
            cwd=directory, capture_output=True, text=True, timeout=5, check=True,
        ).stdout.strip()
        status = subprocess.run(  # noqa: S603
            [git, "status", "--porcelain"],
            cwd=directory, capture_output=True, text=True, timeout=5, check=True,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return {"commit": commit, "dirty": bool(status.strip())}


def environment_metadata(directory: Path | None = None) -> dict[str, Any]:
    from osel import __version__

    env: dict[str, Any] = {
        "osel_version": __version__,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "byteorder": sys.byteorder,
    }
    if directory is not None:
        env["git"] = _git_info(directory)
    return env


@dataclass
class RunRecord:
    run_id: str
    created_at: str
    name: str
    osel_version: str
    config: dict[str, Any]
    dataset: dict[str, Any]
    metrics: dict[str, dict[str, Any]]
    environment: dict[str, Any]
    statistics: dict[str, Any]
    aggregates: dict[str, dict[str, Any]]
    examples: list[dict[str, Any]]
    warnings: list[str] = field(default_factory=list)
    schema_version: str = RUN_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["config"] = redact(d["config"])
        return {"schema_version": d.pop("schema_version"), **d}

    @classmethod
    def from_dict(cls, d: Any) -> RunRecord:
        if not isinstance(d, dict):
            raise InvalidInputError("run file must contain a JSON object")
        version = d.get("schema_version")
        if version != RUN_SCHEMA_VERSION:
            raise InvalidInputError(
                f"unsupported run schema_version {version!r} (supported: {RUN_SCHEMA_VERSION})"
            )
        required = [
            "run_id", "created_at", "name", "osel_version", "config", "dataset",
            "metrics", "environment", "statistics", "aggregates", "examples",
        ]
        missing = [k for k in required if k not in d]
        if missing:
            raise InvalidInputError("run file is missing fields", missing)
        return cls(**{k: d[k] for k in required}, warnings=list(d.get("warnings", [])))

    def scores_by_id(self, metric: str) -> dict[str, float]:
        return {
            e["id"]: e["scores"][metric]
            for e in self.examples
            if metric in e.get("scores", {})
        }


def save_run(record: RunRecord, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(record.to_dict(), indent=2, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    tmp.replace(p)
    return p


def load_run(path: str | Path) -> RunRecord:
    p = Path(path)
    if not p.is_file():
        raise InvalidInputError(f"run file not found: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InvalidInputError(f"run file {p} is not valid JSON: {exc}") from exc
    return RunRecord.from_dict(data)


class RunStore:
    """Local run store: one JSON file per run under ``<root>`` (default ``.osel/runs``)."""

    def __init__(self, root: str | Path = ".osel/runs") -> None:
        self.root = Path(root)

    def save(self, record: RunRecord) -> Path:
        return save_run(record, self.root / f"{record.run_id}.json")

    def list(self) -> list[Path]:
        """Stored run files, oldest first.

        Ordered by each run's ``created_at`` (microsecond precision), not by file name: run IDs
        only have one-second resolution, so two runs in the same second would otherwise be
        ordered by their hash suffix and ``latest`` could pick the wrong one.
        """
        if not self.root.is_dir():
            return []

        def created(p: Path) -> str:
            try:
                value = json.loads(p.read_text(encoding="utf-8")).get("created_at", "")
            except (OSError, ValueError, AttributeError):
                return ""
            return value if isinstance(value, str) else ""

        return sorted(self.root.glob("*.json"), key=lambda p: (created(p), p.name))

    def resolve(self, ref: str) -> Path:
        """Resolve a file path, a full run ID, a unique run-ID prefix, or ``latest``."""
        as_path = Path(ref)
        if as_path.is_file():
            return as_path
        runs = self.list()
        if ref == "latest":
            if not runs:
                raise InvalidInputError(f"no runs stored in {self.root}")
            return runs[-1]
        exact = self.root / f"{ref}.json"
        if exact.is_file():
            return exact
        matches = [r for r in runs if r.stem.startswith(ref)]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise InvalidInputError(
                f"run reference {ref!r} is ambiguous", [m.stem for m in matches]
            )
        raise InvalidInputError(f"no run file or stored run matches {ref!r} (store: {self.root})")

    def load(self, ref: str) -> RunRecord:
        return load_run(self.resolve(ref))
