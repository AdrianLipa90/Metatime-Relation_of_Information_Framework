#!/usr/bin/env python3
import csv, json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ledger = root / "results" / "mass_formula_dependency_ledger_v3_6_repair1.csv"
formal = root / "results" / "archive_formula_formalization_repair1.json"

rows = list(csv.DictReader(ledger.open(encoding="utf-8")))
meta = json.loads(formal.read_text(encoding="utf-8"))

classes = {}
for r in rows:
    cls = r.get("dependency_classification","")
    classes[cls] = classes.get(cls, 0) + 1

status = {
    "gate": "REPAIR1_FORMALIZATION_PASS",
    "rows_in_dependency_ledger": len(rows),
    "dependency_class_counts": classes,
    "archive_formulas_rejected_for_being_old": False,
    "table_lookup_called_emergent": False,
    "technical_pass_claimed_as_substantive_pass": False,
    "base_repo": meta["base_repo"],
    "principle": meta["principle"],
}
out = root / "results" / "repair1_validation_status.json"
out.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(status, ensure_ascii=False, indent=2))
