#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDINGS = ROOT / "results" / "old_metatime_reference_findings_v2_5.csv"
OUT = ROOT / "results" / "old_metatime_reference_findings_v2_5.json"

REQUIRED_CATEGORIES = {"scaling", "ckm", "pmns", "fermion_table", "representation"}


def main() -> int:
    rows = []
    with FINDINGS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    categories = {r["category"] for r in rows}
    missing = sorted(REQUIRED_CATEGORIES - categories)
    status_counts = {}
    for r in rows:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
    payload = {
        "module": "old_metatime_debt9_ckm_table_mining_v2_5",
        "gate_type": "structural_source_pass",
        "row_count": len(rows),
        "required_categories_present": not missing,
        "missing_categories": missing,
        "status_counts": status_counts,
        "no_canon_promotion": True,
        "masses_used_as_new_input": False,
        "recommended_next_debt": "Debt 9 one-anchor mass-scale derivation with Ramanujan scaling and zeta-Heisenberg fluctuation",
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if missing:
        print("FAIL missing categories", missing)
        return 1
    print("PASS", json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
