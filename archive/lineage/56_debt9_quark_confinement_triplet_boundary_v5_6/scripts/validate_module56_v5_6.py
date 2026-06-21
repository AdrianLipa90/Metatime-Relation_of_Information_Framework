#!/usr/bin/env python3
import json, pathlib, sys
MODULE = "56_debt9_quark_confinement_triplet_boundary_v5_6"
ROOT = pathlib.Path(__file__).resolve().parents[2]
RESULT = ROOT / MODULE / "results" / "debt9_quark_confinement_triplet_boundary_v5_6.json"
ACTIVE = ROOT / MODULE / "scripts" / "debt9_quark_confinement_triplet_boundary_v5_6.py"
OUT = ROOT / MODULE / "results" / "VALIDATION_MODULE56_v5_6.json"

data = json.loads(RESULT.read_text(encoding="utf-8"))
active_text = ACTIVE.read_text(encoding="utf-8")
checks = {}
checks["result_exists"] = RESULT.exists()
checks["debt9_open"] = data.get("debt9_numeric_spectrum") == "OPEN_NOT_CLOSED"
checks["no_mass_closure_claim"] = data.get("mass_closure_claimed") is False
checks["single_quark_closure_denied"] = data.get("decision", {}).get("single_quark_exact_mass_scoring") == "DENIED_AS_CLOSURE_CRITERION"
checks["confinement_budget_is_21_percent"] = abs(float(data.get("user_correction_integrated", {}).get("budget", -1)) - 0.21) < 1e-12
checks["triplet_required_next"] = data.get("decision", {}).get("triplet_hadron_aggregation") == "REQUIRED_NEXT"
checks["top_only_nonanchor_inside_budget"] = data.get("metrics", {}).get("within_budget_slots") == ["t"]
checks["no_old_solver_import_in_active_script"] = "import NoParamSM" not in active_text and "noparamSMsolver" not in active_text
checks["no_current_or_canon_promotion"] = data.get("canon_allowed") is False and data.get("current_promotion") == "DENY_CURRENT"
status = "PASS" if all(checks.values()) else "FAIL"
payload = {"schema":"VALIDATION_MODULE56_V5_6", "module": MODULE, "status": status, "checks": checks}
OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2))
sys.exit(0 if status == "PASS" else 1)
