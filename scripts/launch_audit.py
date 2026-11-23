"""OSEL launch audit: run every automated release check and list what still needs a person.

Usage:  python scripts/launch_audit.py [--quick] [--report operations/launch-audit-report.md]

  --quick   skip the slow steps (clean-install, docs and website builds)

Result categories:
  PASS   automated check passed
  FAIL   automated check failed (a launch blocker until fixed)
  HUMAN  can't be verified by a script: needs a person (often with a parent/guardian)
  SKIP   tool not available on this machine (e.g. Node.js)

Exit code: 0 if there are no FAILs (HUMAN items may remain), 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import venv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "site", ".astro", "__pycache__", ".pytest_cache",
             ".mypy_cache", ".ruff_cache", "build", "public"}
PLACEHOLDERS = ["[Founder name]", "[osel-org]", "[osel-domain]", "[founder-handle]"]
SECRET_PATTERNS = {
    "private key block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "GitHub token": re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ALLOWED_EMAIL_DOMAINS = ("example.com", "example.org", "anthropic.com", "users.noreply.github.com")
HOME_PATH = re.compile(r"([A-Za-z]:\\\\?Users\\\\?[^\\/\s\"']+|/(?:home|Users)/[a-z][^/\s\"']*/)", re.IGNORECASE)

results: list[tuple[str, str, str]] = []


def record(status: str, name: str, detail: str = "") -> None:
    results.append((status, name, detail))
    print(f"[{status:5}] {name}" + (f" — {detail}" if detail else ""), flush=True)


def run(cmd: list[str], cwd: Path = ROOT, env: dict[str, str] | None = None, timeout: int = 900):
    full_env = {**os.environ, **(env or {})}
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=full_env)


def tail(proc: subprocess.CompletedProcess[str], n: int = 3) -> str:
    lines = (proc.stdout + proc.stderr).strip().splitlines()
    return " | ".join(lines[-n:])


def repo_files() -> list[Path]:
    git = shutil.which("git")
    if git:
        proc = run([git, "ls-files", "--cached", "--others", "--exclude-standard"])
        if proc.returncode == 0:
            return [ROOT / line for line in proc.stdout.splitlines() if line and (ROOT / line).is_file()]
    return [p for p in ROOT.rglob("*") if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS)]


def read(p: Path) -> str | None:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


# --- checks ----------------------------------------------------------------------------------


def check_placeholders(files: list[Path]) -> None:
    counts: dict[str, int] = {ph: 0 for ph in PLACEHOLDERS}
    for f in files:
        if f.name in ("set_identity.py", "launch_audit.py"):
            continue
        text = read(f) or ""
        for ph in PLACEHOLDERS:
            counts[ph] += text.count(ph)
    left = {k: v for k, v in counts.items() if v}
    if left:
        record("HUMAN", "Placeholders replaced",
               ", ".join(f"{k}×{v}" for k, v in left.items()) + " — decide values, then run scripts/set_identity.py")
    else:
        record("PASS", "Placeholders replaced")


def check_secrets_and_personal_info(files: list[Path]) -> None:
    hits, emails, paths = [], set(), []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(".env") or "/.env" in rel or f.suffix in (".pem", ".key"):
            hits.append(f"{rel}: secret-like file")
        text = read(f)
        if text is None or f.name == "launch_audit.py":
            continue
        for label, pat in SECRET_PATTERNS.items():
            if pat.search(text):
                hits.append(f"{rel}: {label}")
        for m in EMAIL.findall(text):
            domain = m.split("@", 1)[1].lower()
            if "[osel-domain]" in m or domain.endswith(ALLOWED_EMAIL_DOMAINS) or m.startswith("git@"):
                continue
            emails.add(f"{m} ({rel})")
        if HOME_PATH.search(text) and f.suffix not in (".lock",):
            paths.append(rel)
    record("FAIL" if hits else "PASS", "No secrets or secret files in the repo", "; ".join(hits[:10]))
    if emails:
        record("HUMAN", "Email addresses are role addresses only",
               "review: " + "; ".join(sorted(emails)[:10]))
    else:
        record("PASS", "No personal email addresses in files")
    record("FAIL" if paths else "PASS", "No local home-folder paths (usernames) in files", ", ".join(paths[:10]))


def check_versions() -> None:
    init = (ROOT / "src/osel/__init__.py").read_text(encoding="utf-8")
    v = re.search(r'__version__ = "([^"]+)"', init)
    version = v.group(1) if v else "?"
    cff = re.search(r"^version: (\S+)", (ROOT / "CITATION.cff").read_text(encoding="utf-8"), re.M)
    site = re.search(r'version: "([^"]+)"', (ROOT / "website/src/site.ts").read_text(encoding="utf-8"))
    found = {"package": version, "CITATION.cff": cff.group(1) if cff else "?", "website": site.group(1) if site else "?"}
    same = len(set(found.values())) == 1
    record("PASS" if same else "FAIL", "Version consistent across package, citation, website",
           ", ".join(f"{k}={v}" for k, v in found.items()))
    if ".dev" in version:
        record("HUMAN", "Release version chosen", f"still {version}; set e.g. 0.1.0a1 at release (checklist step 6)")


def check_python_quality() -> None:
    py = sys.executable
    for name, cmd in (("Tests (pytest)", [py, "-m", "pytest", "-q"]),
                      ("Lint (ruff)", [py, "-m", "ruff", "check", "."]),
                      ("Types (mypy --strict)", [py, "-m", "mypy", "src"])):
        proc = run(cmd)
        record("PASS" if proc.returncode == 0 else "FAIL", name, tail(proc, 1))


def check_clean_install() -> None:
    py = sys.executable
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        proc = run([py, "-m", "build", "--outdir", str(t / "dist")])
        if proc.returncode != 0:
            record("FAIL", "Package builds (sdist + wheel)", tail(proc))
            return
        record("PASS", "Package builds (sdist + wheel)")
        venv.create(t / "venv", with_pip=True)
        bindir = t / "venv" / ("Scripts" if os.name == "nt" else "bin")
        vpy = bindir / ("python.exe" if os.name == "nt" else "python")
        wheel = next((t / "dist").glob("*.whl"))
        proc = run([str(vpy), "-m", "pip", "install", "-q", str(wheel)])
        if proc.returncode != 0:
            record("FAIL", "Clean install from wheel", tail(proc))
            return
        work = t / "qs"
        shutil.copytree(ROOT / "examples" / "quickstart", work)
        osel = [str(vpy), "-m", "osel", "--store", str(t / "store")]
        steps = [
            (["dataset", "validate", "data.jsonl"], 0),
            (["eval", "run", "config.yaml", "-o", "b.json"], 0),
            (["eval", "run", "config_v2.yaml", "-o", "c.json"], 0),
            (["compare", "b.json", "c.json"], 0),
            (["check", "--baseline", "b.json", "--current", "c.json"], 1),
            (["check", "--baseline", "b.json", "--current", "c.json", "--tolerance", "0.25"], 0),
            (["check", "--baseline", "missing.json", "--current", "c.json"], 2),
        ]
        for args, expected in steps:
            proc = run(osel + args, cwd=work, env={"PYTHONPATH": ""})
            if proc.returncode != expected:
                record("FAIL", "Clean install: documented quick start + exit codes",
                       f"`osel {' '.join(args)}` exited {proc.returncode}, expected {expected}")
                return
        b = json.loads((work / "b.json").read_text(encoding="utf-8"))
        ok = abs(b["aggregates"]["exact_match"]["mean"] - 0.8) < 1e-9
        record("PASS" if ok else "FAIL", "Clean install: documented quick start + exit codes",
               "7 steps, results match docs" if ok else "results differ from docs")


def check_docs_and_website(node_ok: bool) -> None:
    py = sys.executable
    public_docs = ROOT / "website" / "public" / "docs"
    for base, docs_url in (("/", "https://osel.example/docs/"), ("/osel/", "https://example.org/osel/docs/")):
        shutil.rmtree(public_docs, ignore_errors=True)
        proc = run([py, "-m", "mkdocs", "build", "-q", "--strict", "--site-dir", str(public_docs)],
                   env={"OSEL_DOCS_URL": docs_url})
        if proc.returncode != 0:
            record("FAIL", "Docs build (mkdocs --strict)", tail(proc))
            return
        if not node_ok:
            record("SKIP", f"Website build + link check (base {base})", "Node.js/npm not found")
            continue
        npm = shutil.which("npm") or "npm"
        web = ROOT / "website"
        if not (web / "node_modules").is_dir():
            run([npm, "ci"], cwd=web)
        env = {"OSEL_BASE": base, "MSYS_NO_PATHCONV": "1"}
        proc = run([npm, "run", "build"], cwd=web, env=env)
        if proc.returncode != 0:
            record("FAIL", f"Website build (base {base})", tail(proc))
            continue
        proc = run([npm, "run", "check-links"], cwd=web, env=env)
        record("PASS" if proc.returncode == 0 else "FAIL",
               f"Website + docs built, links checked (base {base})", tail(proc, 1))
    record("PASS", "Docs build (mkdocs --strict)")
    shutil.rmtree(public_docs, ignore_errors=True)


def check_markdown_links(files: list[Path]) -> None:
    bad = []
    for f in files:
        if f.suffix != ".md" or "website/drafts" in f.as_posix():
            continue
        for href in re.findall(r"\]\(([^)\s]+)\)", read(f) or ""):
            if re.match(r"^(https?:|mailto:|#|/)", href) or "[osel" in href:
                continue
            if not (f.parent / href.split("#")[0]).exists():
                bad.append(f"{f.relative_to(ROOT).as_posix()} -> {href}")
    record("FAIL" if bad else "PASS", "Relative links in Markdown files resolve", "; ".join(bad[:10]))


def check_workflows() -> None:
    unpinned, risky = [], []
    for wf in (ROOT / ".github/workflows").glob("*.yml"):
        text = wf.read_text(encoding="utf-8")
        for m in re.finditer(r"uses:\s*([^\s#]+)", text):
            ref = m.group(1)
            if ref.startswith("./"):
                continue
            if not re.search(r"@[0-9a-f]{40}$", ref):
                unpinned.append(f"{wf.name}: {ref}")
        if "pull_request_target" in text:
            risky.append(f"{wf.name}: pull_request_target")
        if not re.search(r"^permissions:", text, re.M):
            risky.append(f"{wf.name}: no top-level permissions")
    record("FAIL" if unpinned else "PASS", "Third-party actions pinned to commit SHAs", "; ".join(unpinned))
    record("FAIL" if risky else "PASS", "Workflows: least-privilege token, no pull_request_target", "; ".join(risky))
    release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    gated = "vars.PUBLISH_TO_PYPI == 'true'" in release
    record("PASS" if gated else "FAIL", "PyPI publishing is off unless explicitly enabled")


def check_policy_status() -> None:
    index = (ROOT / "policies/README.md").read_text(encoding="utf-8")
    pending = [name for name in ("Open-source license", "Privacy")
               if re.search(rf"\| {name} \|[^\n]*Proposed", index)]
    if pending:
        record("HUMAN", "License and privacy policy approved", "pending review: " + ", ".join(pending))
    else:
        record("PASS", "License and privacy policy approved")


HUMAN_ITEMS = [
    "Choose public founder name/handle, GitHub org name and domain (with a parent/guardian)",
    "Check the OSEL name for conflicts before branding spend; record in the decision log",
    "Create the GitHub organization (2FA on, trusted adult as backup owner) and push the repo",
    "Apply operations/repo-settings.md: branch ruleset, private vulnerability reporting, secret scanning, Dependabot",
    "Enable GitHub Pages (Source: GitHub Actions); confirm the Pages workflow deploys",
    "Set up role email forwarding (hello@, security@, conduct@, privacy@) and test each address",
    "Watch the first CI run go green on Linux, macOS and Windows",
    "Run the GitHub Action in a separate real test repository",
    "Have someone other than the founder follow the quick start on a clean machine",
    "Enable Trusted Publishing and set PUBLISH_TO_PYPI only after license and metadata review",
    "Invite the first 10 early-access testers (programs/early-access.md)",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--report", help="also write a Markdown report to this path")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print(f"OSEL launch audit — {date.today().isoformat()}\n")
    files = repo_files()
    check_placeholders(files)
    check_secrets_and_personal_info(files)
    check_versions()
    check_workflows()
    check_policy_status()
    check_markdown_links(files)
    check_python_quality()
    if args.quick:
        record("SKIP", "Clean install, docs and website builds", "--quick")
    else:
        check_clean_install()
        check_docs_and_website(node_ok=shutil.which("npm") is not None)
    for item in HUMAN_ITEMS:
        record("HUMAN", item)

    counts = {s: sum(1 for r in results if r[0] == s) for s in ("PASS", "FAIL", "HUMAN", "SKIP")}
    summary = " · ".join(f"{k} {v}" for k, v in counts.items())
    print(f"\n{summary}")
    print("Automated checks: " + ("ALL PASSING" if counts["FAIL"] == 0 else "BLOCKERS FOUND"))

    if args.report:
        lines = [f"# Launch audit report — {date.today().isoformat()}", "",
                 "Generated by `python scripts/launch_audit.py`. Re-run after any change.", "",
                 f"**{summary}**", "", "| Status | Check | Detail |", "|---|---|---|"]
        lines += [f"| {s} | {n} | {d.replace('|', '/')} |" for s, n, d in results]
        out = ROOT / args.report
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to {out.relative_to(ROOT)}")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
