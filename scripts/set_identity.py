"""Replace the launch placeholders everywhere in the repository.

Placeholders:
  [Founder name]    -> how the founder is named publicly (a name or a handle; your choice)
  [osel-org]        -> GitHub organization name
  [osel-domain]     -> email/website domain (e.g. osel.dev)
  [founder-handle]  -> founder's GitHub username (used as @handle in CODEOWNERS)

Usage (dry run first, then --apply):
  python scripts/set_identity.py --founder-name "A. Founder" --org osel-lab \
      --domain osel.dev --founder-handle afounder
  python scripts/set_identity.py ... --apply

Any value can be omitted to leave that placeholder in place. Decide the public name with a
parent/guardian. A handle instead of a full legal name is perfectly fine.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "site", ".astro", "__pycache__", ".pytest_cache",
             ".mypy_cache", ".ruff_cache", "build", "docs_build"}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".cff", ".ts", ".astro", ".mjs", ".txt",
                 ".json", ".html", ".css", ""}
PLACEHOLDERS = {
    "founder_name": "[Founder name]",
    "org": "[osel-org]",
    "domain": "[osel-domain]",
    "founder_handle": "[founder-handle]",
}
VALID = {
    "org": re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$"),
    "founder_handle": re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$"),
    "domain": re.compile(r"^(?=.{4,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$"),
}


def iter_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS) and p.suffix in TEXT_SUFFIXES:
            if p.name == "package-lock.json" or p.resolve() == Path(__file__).resolve():
                continue
            out.append(p)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--founder-name")
    ap.add_argument("--org")
    ap.add_argument("--domain")
    ap.add_argument("--founder-handle")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    values = {k: getattr(args, k) for k in PLACEHOLDERS if getattr(args, k)}
    for key, value in values.items():
        if key in VALID and not VALID[key].match(value):
            print(f"error: invalid --{key.replace('_', '-')}: {value!r}", file=sys.stderr)
            return 2
        if any(c in value for c in "[]<>`\n"):
            print(f"error: --{key.replace('_', '-')} contains invalid characters", file=sys.stderr)
            return 2
    if not values:
        print("Nothing to replace. Pass at least one value (see --help).")

    remaining: dict[str, int] = {ph: 0 for ph in PLACEHOLDERS.values()}
    changed = 0
    for path in iter_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = text
        for key, value in values.items():
            new = new.replace(PLACEHOLDERS[key], value)
        for ph in PLACEHOLDERS.values():
            remaining[ph] += new.count(ph)
        if new != text:
            changed += 1
            print(f"{'updated' if args.apply else 'would update'}: {path.relative_to(ROOT)}")
            if args.apply:
                path.write_text(new, encoding="utf-8")

    print(f"\n{changed} file(s) {'updated' if args.apply else 'would change'}.")
    left = {ph: n for ph, n in remaining.items() if n}
    if left:
        print("Placeholders still present after this run: " + ", ".join(f"{ph} ×{n}" for ph, n in left.items()))
    else:
        print("No placeholders remain.")
    if not args.apply and values:
        print("Dry run only. Re-run with --apply to write the changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
