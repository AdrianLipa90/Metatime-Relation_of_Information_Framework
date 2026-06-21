#!/usr/bin/env python3
from __future__ import annotations
import json, re, zipfile, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[0]
SCRIPT = ROOT / "scripts" / "debt9_yukawa_boundary_resolution_v4_2.py"
RESULT = ROOT / "results" / "debt9_yukawa_boundary_resolution_v4_2.json"

# Execute active script first so validation is about generated state, not stale files.
run = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
(ROOT / "results" / "debt9_yukawa_boundary_resolution_v4_2.stdout.json").write_text(run.stdout, encoding="utf-8")
(ROOT / "results" / "debt9_yukawa_boundary_resolution_v4_2.stderr.txt").write_text(run.stderr, encoding="utf-8")

payload = json.loads(RESULT.read_text(encoding="utf-8")) if RESULT.exists() else {}
script_text = SCRIPT.read_text(encoding="utf-8", errors="ignore")
result_text = RESULT.read_text(encoding="utf-8", errors="ignore") if RESULT.exists() else ""

# Patterns detect actual embedded reference dictionaries/tables or hidden reference-mass machinery.
forbidden_code_patterns = {
    "reference_mass_dictionary_assignment": r"\b(PD" + r"G|reference_masses|mass_ref)\s*=\s*[{\[]",
    "flavour_matrix_numeric_assignment": r"\b(CK" + r"M|PM" + r"NS)\s*=\s*[{\[]",
    "noparam_import_or_exec": r"No" + r"ParamSM|noparamSMsolver",
}
code_hits = {name: pat for name, pat in forbidden_code_patterns.items() if re.search(pat, script_text)}

# Numeric forbidden tokens are not scanned in prose docs; only active script/result.  They are split to avoid the validator matching itself.
forbidden_numeric_tokens = [
    "0.510" + "998", "105." + "658", "1776" + ".86", "172" + "760", "173" + "000",
]
num_hits = [tok for tok in forbidden_numeric_tokens if tok in script_text or tok in result_text]

nested_archives = [str(p.relative_to(REPO)) for p in REPO.rglob("*") if p.is_file() and p.suffix.lower() in {".zip", ".tar", ".gz", ".tgz", ".7z", ".rar"}]

checks = {
    "active_script_executed": run.returncode == 0,
    "result_status_pass": payload.get("status") == "PASS",
    "sm_internal_boundary_resolved": payload.get("debt9_split", {}).get("Debt9_SM_internal") == "RESOLVED_AS_YUKAWA_BOUNDARY_NOT_NUMERIC_PREDICTION",
    "numeric_spectrum_not_closed": payload.get("debt9_split", {}).get("Debt9_numeric_mass_spectrum") == "OPEN_NOT_CLOSED_IN_THIS_MODULE",
    "observed_masses_not_used": payload.get("observed_masses_used") is False,
    "reference_spectrum_not_used": payload.get("reference_spectrum_used") is False,
    "old_tau_not_used": payload.get("old_tau_used") is False,
    "mass_prediction_not_made": payload.get("mass_prediction_made") is False,
    "yukawa_gauge_invariance_pass": payload.get("yukawa_gauge_invariance_all_pass") is True,
    "anomaly_checks_pass": payload.get("anomaly_checks_all_zero") is True,
    "no_hidden_reference_code_patterns": not bool(code_hits),
    "no_forbidden_reference_mass_tokens": not bool(num_hits),
    "no_nested_archives_in_repo": not bool(nested_archives),
}
issues = []
if run.returncode != 0:
    issues.append({"script_stderr": run.stderr})
if code_hits:
    issues.append({"forbidden_code_hits": code_hits})
if num_hits:
    issues.append({"forbidden_numeric_reference_tokens": num_hits})
if nested_archives:
    issues.append({"nested_archives": nested_archives[:50], "count": len(nested_archives)})
for key, ok in checks.items():
    if not ok and key not in {"no_hidden_reference_code_patterns", "no_forbidden_reference_mass_tokens", "no_nested_archives_in_repo"}:
        issues.append({key: ok})

status = "PASS" if all(checks.values()) else "FAIL"
validation = {
    "schema": "METATIME_SM_MODULE42_VALIDATION_V4_2",
    "status": status,
    "scope": "active v4.2 module scripts/results plus repo archive hygiene",
    "checks": checks,
    "issues": issues,
    "doctor_verdict": "DEBT9_SM_BOUNDARY_VALIDATION_PASS__NUMERIC_MASS_SPECTRUM_OPEN" if status == "PASS" else "STOP_CRITICAL",
}
(ROOT / "results" / "VALIDATION_MODULE42_v4_2.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
print(json.dumps(validation, indent=2))
