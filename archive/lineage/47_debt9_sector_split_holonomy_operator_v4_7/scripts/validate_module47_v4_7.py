#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, py_compile, sys

MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
ROOT = MODULE_DIR.parent
SCRIPT = MODULE_DIR / "scripts" / "sector_split_holonomy_operator_v4_7.py"
RESULT = MODULE_DIR / "results" / "sector_split_holonomy_operator_v4_7.json"


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
        issues.append("debt9_numeric_spectrum_must_remain_open")
    if data.get("canon_allowed") is not False:
        issues.append("canon_must_be_false")
    policy = data.get("operator_policy", {})
    for key in ["mass_input_used_inside_operator", "benchmark_input_used_inside_operator", "post_residual_tuning_used", "archived_mass_solver_used", "reference_replay_used"]:
        if policy.get(key) is not False:
            issues.append(f"policy_violation:{key}")
    if policy.get("unit_anchors_used_only_after_freeze_for_benchmark_units") is not True:
        issues.append("missing_unit_anchor_boundary")
    if policy.get("family_unit_anchors_make_this_non_closure") is not True:
        issues.append("missing_non_closure_boundary")
    if not data.get("operator_fingerprint_sha256"):
        issues.append("missing_operator_fingerprint")
    # No nested archives inside the repo root.
    nested = []
    archive_suffixes = {".zip", ".tar", ".tgz", ".bz2", ".7z", ".rar"}
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in archive_suffixes:
            nested.append(str(p.relative_to(ROOT)))
        if p.is_file() and p.name.endswith(".tar.gz"):
            nested.append(str(p.relative_to(ROOT)))
    if nested:
        issues.append("nested_archives_present:" + ",".join(nested[:10]))
    validation = {
        "schema": "VALIDATION_MODULE47_V4_7",
        "module": "47_debt9_sector_split_holonomy_operator_v4_7",
        "result": "PASS" if not issues else "FAIL",
        "issues": issues,
        "checked_files": [str(SCRIPT.relative_to(ROOT)), str(RESULT.relative_to(ROOT))],
    }
    out = MODULE_DIR / "results" / "VALIDATION_MODULE47_v4_7.json"
    out.write_text(json.dumps(validation, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(validation, indent=2))
    if issues:
        sys.exit(1)

if __name__ == "__main__":
    main()
