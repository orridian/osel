# Data handling policy

**Owner:** Founder · **Contact:** `privacy@[osel-domain]` · **Enforcement:** data received outside this policy is deleted.

## Part A — How the `osel` software handles your data (IN FORCE: describes current behavior)

- osel reads your dataset and predictions from local files and **writes run records only to your disk**: `.osel/runs/` in the current folder, plus any `--output` file. Nothing is sent anywhere. There is no telemetry and no network access.
- A run record contains your **config** (with secret-looking keys redacted), **dataset identity** (a hash, not the data), each example's **id**, **scores**, **errors** and, by default, the **prediction** itself. Set `record_predictions: false` if predictions are sensitive.
- Example **inputs and references are not copied** into run records.
- Redaction is a safety net, not a guarantee. Don't put secrets in configs, and review run files before sharing or committing them.
- Run records you commit (e.g. CI baselines) become public if your repository is public.

## Part B — Data sent to OSEL maintainers (DRAFT: not in force)

**Trigger:** before OSEL handles any user-submitted data (e.g. datasets sent for a case study or benchmark).

## Classification

| Class | Examples | Rules |
|---|---|---|
| Public | Open datasets, published results | May be stored in public repos with attribution |
| Internal | Alpha-tester notes, metric ledger | Private repo/drive; maintainers only |
| Confidential | Datasets shared privately by a user or organization | Written permission; named access list; encrypted storage; never in Git |
| Prohibited | Health, financial, government ID, children's data, credentials | **Do not accept.** Delete immediately if received, and notify the sender. |

## Access

Least privilege. Access lists for Internal and Confidential data are reviewed quarterly ([access review](../operations/access-review.md)).

## Storage and backup

Confidential data stays only in the agreed location. It is never committed to Git, never placed in CI artifacts, and never shared with third-party tools (including AI services) without written permission.

## Sharing

Data goes only to people named in the agreement.

## Deletion

Delete at the end of the agreed purpose or within 30 days of a request. Record the deletion in the records log.
