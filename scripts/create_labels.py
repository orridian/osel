"""Create/update the issue labels in .github/labels.yml on a GitHub repo, using the `gh` CLI.

  python scripts/create_labels.py --repo ORG/osel           # dry run: print what would happen
  python scripts/create_labels.py --repo ORG/osel --apply   # needs `gh auth login` first
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="OWNER/REPO")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    labels = yaml.safe_load((ROOT / ".github/labels.yml").read_text(encoding="utf-8"))
    gh = shutil.which("gh")
    if args.apply and not gh:
        print("error: GitHub CLI `gh` not found")
        return 2
    for lab in labels:
        cmd = [gh or "gh", "label", "create", lab["name"], "--repo", args.repo,
               "--color", str(lab["color"]), "--description", lab["description"], "--force"]
        if args.apply:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            print(("ok     " if proc.returncode == 0 else "FAILED ") + lab["name"], proc.stderr.strip())
        else:
            print("would create/update:", lab["name"])
    if not args.apply:
        print("Dry run. Add --apply to create the labels.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
