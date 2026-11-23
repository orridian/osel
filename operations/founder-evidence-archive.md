# Founder evidence archive

A dated record of what was founded, when and by whom. **Primary evidence** is public (Git history and releases). **Administrative records** are private, in the planning folder, shared with a parent/guardian.

## Keep (dated)

| Evidence | Where | Public? |
|---|---|---|
| Founding statement ([FOUNDING.md](../FOUNDING.md)) | Repo | Yes |
| First product specification (docs/ + ROADMAP at first commit) | Repo history | Yes |
| Repository creation and first commits | GitHub, `git log --reverse` | Yes |
| First releases | GitHub releases and tags | Yes |
| Roadmap changes | `git log -- ROADMAP.md` | Yes |
| Maintainer appointments | GOVERNANCE.md history + decision log | Yes |
| Account ownership records (registrar, PyPI, GitHub org) | Private folder | No |
| Correspondence establishing collaborations | Private folder | No |

## Rules

- Publish a founder history **only when accurate**, and keep it concise.
- Never expose your home address, school schedule, private phone number or personal accounts.
- Use titles precisely: founder ≠ co-founder ≠ contributor ≠ advisor ≠ maintainer ≠ employee.
- Optional, for extra durability: export a signed tag at milestones (`git tag -s founding-2026-11-11`).
