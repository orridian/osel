"""Regenerate this demo's data deterministically: python generate.py

Two scenarios with the SAME +5-point accuracy improvement (70% -> 75%):
  small/: 40 examples   (candidate fixes 4, breaks 2)
  large/: 400 examples  (candidate fixes 40, breaks 20)
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent


def write(folder: str, n: int, base_correct: int, fixes: int, breaks: int) -> None:
    out = HERE / folder
    out.mkdir(exist_ok=True)
    ids = [f"{folder}-{i:04d}" for i in range(n)]
    base_ok = set(ids[:base_correct])
    # candidate breaks the first `breaks` baseline-correct examples and fixes the first `fixes` others
    cand_ok = (base_ok - set(ids[:breaks])) | set(ids[base_correct : base_correct + fixes])

    def jsonl(name: str, rows: list[dict]) -> None:
        (out / name).write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")

    def preds(ok: set[str]) -> list[dict]:
        return [{"id": i, "output": "right" if i in ok else "wrong"} for i in ids]

    jsonl("data.jsonl", [{"id": i, "input": f"question {i}", "reference": "right"} for i in ids])
    jsonl("baseline_predictions.jsonl", preds(base_ok))
    jsonl("candidate_predictions.jsonl", preds(cand_ok))
    for name in ("baseline", "candidate"):
        pred_file = f"{name}_predictions.jsonl"
        (out / f"{name}.yaml").write_text(
            f"name: {folder}-{name}\ndataset: data.jsonl\npredictions: {pred_file}\n"
            "metrics: [exact_match]\nseed: 0\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    write("small", n=40, base_correct=28, fixes=4, breaks=2)
    write("large", n=400, base_correct=280, fixes=40, breaks=20)
    print("wrote small/ and large/")
