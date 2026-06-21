#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, py_compile, sys, zipfile

MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
ROOT = MODULE_DIR.parent
SCRIPT = MODULE_DIR / "scripts" / "document_formula_selection_benchmark_v4_6.py"
RESULT = MODULE_DIR / "results" / "document_formula_selection_benchmark_v4_6.json"


def main() -> None:
    issues = []
    try:
        py_compile.compile(str(SCRIPT), doraise=True)
    except Exception as e:
        issues.append(f"compile_fail:{e}")
    if not RESULT.exists():
        issues.append("missing_result_json")
        data = {}
    else:
        data = json.loads(RESULT.read_text(encoding="utf-8"))
    if data.get("debt9_numeric_spectrum") != "OPEN_NOT_CLOSED":
        issues.append("debt9_status_must_remain_open")
    if data.get("canon_allowed") is not False:
        issues.append("canon_must_be_denied")
    policy = data.get("operator_input_policy", {})
    for key in ["archived_mass_solver_used", "reference_replay_used", "post_residual_formula_editing"]:
        if policy.get(key) is not False:
            issues.append(f"policy_violation:{key}")
    if policy.get("benchmark_masses_used_inside_selected_formula") is not False:
        issues.append("benchmark_inside_selected_formula")
    if not data.get("freeze_sha256"):
        issues.append("missing_freeze_sha")
    # No nested archives in root repo.
    nested = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".zip", ".tar", ".gz", ".tgz", ".bz2", ".7z", ".rar"}:
            nested.append(str(p.relative_to(ROOT)))
    if nested:
        issues.append("nested_archives_present:" + ",".join(nested[:10]))
    validation = {
        "schema": "VALIDATION_MODULE46_V4_6",
        "module": "46_debt9_document_formula_selection_benchmark_v4_6",
        "result": "PASS" if not issues else "FAIL",
        "issues": issues,
        "checked_files": [str(SCRIPT.relative_to(ROOT)), str(RESULT.relative_to(ROOT))],
    }
    out = MODULE_DIR / "results" / "VALIDATION_MODULE46_v4_6.json"
    out.write_text(json.dumps(validation, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(validation, indent=2))
    if issues:
        sys.exit(1)

if __name__ == "__main__":
    main()
