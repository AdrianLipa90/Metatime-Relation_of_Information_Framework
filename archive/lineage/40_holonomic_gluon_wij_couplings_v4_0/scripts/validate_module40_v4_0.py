#!/usr/bin/env python3
"""Validation gate for module 40 v4.0."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SCRIPT = ROOT / "scripts" / "holonomic_gluon_wij_v4_0.py"


def main() -> int:
    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(ROOT), text=True, capture_output=True)
    (RESULTS / "holonomic_gluon_wij_v4_0.stdout.json").write_text(proc.stdout, encoding="utf-8")
    (RESULTS / "holonomic_gluon_wij_v4_0.stderr.txt").write_text(proc.stderr, encoding="utf-8")

    checks = []
    def add(name: str, ok: bool, detail=None):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    add("script_exit_zero", proc.returncode == 0, proc.returncode)
    result_path = RESULTS / "holonomic_gluon_wij_v4_0.json"
    add("result_json_exists", result_path.exists(), str(result_path))
    if not result_path.exists():
        payload = {}
    else:
        payload = json.loads(result_path.read_text(encoding="utf-8"))

    add("schema_ok", payload.get("schema") == "METATIME_SM_HOLONOMIC_GLUON_WIJ_V4_0", payload.get("schema"))
    add("status_pass", payload.get("status") == "PASS", payload.get("status"))
    guard = payload.get("guardrails", {})
    add("no_pdg_or_mass_reference_input", guard.get("PDG_or_mass_reference_input") is False, guard)
    add("no_observed_masses_input", guard.get("observed_masses_input") is False, guard)
    add("no_ckm_pmns_input", guard.get("CKM_PMNS_input") is False, guard)
    add("mass_prediction_not_claimed", guard.get("mass_prediction_claimed") is False, guard)
    add("full_qcd_not_claimed", guard.get("full_QCD_claimed") is False, guard)
    add("debt9_open", guard.get("Debt_9_status") == "OPEN_NOT_CLOSED", guard.get("Debt_9_status"))

    link = payload.get("link_validation", {})
    add("all_links_su3", link.get("all_links_su3") is True, link)
    add("reverse_links_are_daggers", link.get("all_reverse_links_are_daggers") is True, link)

    loop = payload.get("loop_holonomy_validation", {})
    add("loop_holonomy_is_su3", loop.get("U_loop_is_SU3") is True, loop)
    add("su3_projection_residual_small", float(loop.get("su3_projection_residual", 1.0)) < 1e-10, loop.get("su3_projection_residual"))
    add("nontrivial_active_gluon_modes", len(loop.get("active_gell_mann_modes_1_indexed", [])) > 0, loop.get("active_gell_mann_modes_1_indexed"))
    add("nonzero_wilson_defect", float(loop.get("wilson_loop_defect_3_minus_ReTrU", 0.0)) > 0.0, loop.get("wilson_loop_defect_3_minus_ReTrU"))

    gauge = payload.get("gauge_covariance_validation", {})
    add("gauge_covariance_pass", gauge.get("gauge_covariance_pass") is True, gauge)
    add("trace_invariance_pass", gauge.get("trace_invariance_pass") is True, gauge)
    add("curvature_norm_invariance_pass", gauge.get("curvature_norm_invariance_pass") is True, gauge)

    action = payload.get("action_layer_candidate", {})
    add("information_operator_present", float(action.get("information_operator_g_info_ln2_over_24pi", 0.0)) > 0.0, action)
    add("ramanujan_not_used_as_fit", action.get("ramanujan_scaling_status") == "LOCKED_FOR_FUTURE_COUPLING_NORMALIZATION_NOT_USED_AS_FIT_FACTOR_HERE", action.get("ramanujan_scaling_status"))

    forbidden_active_source_phrases = [
        "mass_calc == reference",
        "reference_spectrum_execution",
        "self.mass_ref",
        "PDG[",
        "noparamSMsolver",
    ]
    main_script_text = SCRIPT.read_text(encoding="utf-8", errors="ignore")
    hits = [phrase for phrase in forbidden_active_source_phrases if phrase in main_script_text]
    add("no_known_reimport_engine_in_main_execution_script", not hits, hits)

    status = "PASS" if all(c["ok"] for c in checks) else "FAIL"
    report = {
        "schema": "VALIDATION_MODULE40_HOLONOMIC_GLUON_WIJ_V4_0",
        "status": status,
        "checks": checks,
    }
    (RESULTS / "VALIDATION_MODULE40_v4_0.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
