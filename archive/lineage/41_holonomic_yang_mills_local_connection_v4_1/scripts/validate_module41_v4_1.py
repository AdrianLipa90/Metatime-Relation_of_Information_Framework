#!/usr/bin/env python3
"""Validation gate for module 41 v4.1."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SCRIPT = ROOT / "scripts" / "holonomic_yang_mills_local_connection_v4_1.py"


def main() -> int:
    RESULTS.mkdir(exist_ok=True)
    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(ROOT), text=True, capture_output=True)
    (RESULTS / "holonomic_yang_mills_local_connection_v4_1.stdout.json").write_text(proc.stdout, encoding="utf-8")
    (RESULTS / "holonomic_yang_mills_local_connection_v4_1.stderr.txt").write_text(proc.stderr, encoding="utf-8")

    checks = []
    def add(name: str, ok: bool, detail=None):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    add("script_exit_zero", proc.returncode == 0, proc.returncode)
    result_path = RESULTS / "holonomic_yang_mills_local_connection_v4_1.json"
    add("result_json_exists", result_path.exists(), str(result_path))
    payload = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}

    add("schema_ok", payload.get("schema") == "METATIME_SM_HOLONOMIC_YANG_MILLS_LOCAL_CONNECTION_V4_1", payload.get("schema"))
    add("status_pass", payload.get("status") == "PASS", payload.get("status"))
    guard = payload.get("guardrails", {})
    add("no_pdg_or_mass_reference_input", guard.get("PDG_or_mass_reference_input") is False, guard)
    add("no_observed_masses_input", guard.get("observed_masses_input") is False, guard)
    add("no_ckm_pmns_input", guard.get("flavour_mixing_matrix_input") is False, guard)
    add("no_noparamsm_input", guard.get("NoParamSM_input") is False, guard)
    add("mass_prediction_not_claimed", guard.get("mass_prediction_claimed") is False, guard)
    add("full_qcd_not_claimed", guard.get("full_QCD_claimed") is False, guard)
    add("debt9_open", guard.get("Debt_9_status") == "OPEN_NOT_CLOSED", guard.get("Debt_9_status"))

    conn = payload.get("connection_layer", {})
    add("all_local_links_su3", conn.get("all_local_links_are_su3") is True, conn)

    curv = payload.get("curvature_layer", {})
    add("plaquette_is_su3", curv.get("plaquette_is_su3") is True, curv)
    add("su3_projection_residual_small", float(curv.get("su3_projection_residual", 1.0)) < 1e-8, curv.get("su3_projection_residual"))
    add("nontrivial_active_modes", len(curv.get("active_gell_mann_modes_1_indexed", [])) > 0, curv.get("active_gell_mann_modes_1_indexed"))
    add("positive_wilson_defect", float(curv.get("wilson_defect_3_minus_ReTrU", 0.0)) > 0.0, curv.get("wilson_defect_3_minus_ReTrU"))

    gauge = payload.get("gauge_covariance_validation", {})
    add("gauge_covariance_pass", gauge.get("gauge_covariance_pass") is True, gauge)
    add("trace_invariance_pass", gauge.get("trace_invariance_pass") is True, gauge)
    add("curvature_norm_invariance_pass", gauge.get("curvature_norm_invariance_pass") is True, gauge)

    ym = payload.get("yang_mills_candidate", {})
    add("ym_action_density_positive", float(ym.get("action_density_proxy_half_Tr_F2", 0.0)) > 0.0, ym)
    add("information_operator_present", float(ym.get("information_operator_g_info_ln2_over_24pi", 0.0)) > 0.0, ym)
    add("ramanujan_not_fit", ym.get("ramanujan_scaling_status") == "LOCKED_FOR_FUTURE_COUPLING_NORMALIZATION_NOT_USED_AS_FIT_FACTOR_HERE", ym.get("ramanujan_scaling_status"))

    scaling = payload.get("small_loop_scaling", {})
    ratios = scaling.get("ratios", [])
    add("small_loop_scaling_ratios_present", len(ratios) >= 3, ratios)
    add("small_loop_scaling_area_squared", all(abs(r.get("wilson_defect_ratio", 0.0) / r.get("expected_for_area_squared", 1.0) - 1.0) < 0.01 for r in ratios), ratios)

    forbidden_active_source_phrases = [
        "mass_calc == reference",
        "reference_spectrum_execution",
        "self.mass_ref",
        "PDG[",
        "noparamSMsolver",
            ]
    main_script_text = SCRIPT.read_text(encoding="utf-8", errors="ignore")
    hits = [phrase for phrase in forbidden_active_source_phrases if phrase in main_script_text]
    add("no_known_reimport_or_mixing_engine_in_main_execution_script", not hits, hits)

    status = "PASS" if all(c["ok"] for c in checks) else "FAIL"
    report = {
        "schema": "VALIDATION_MODULE41_HOLONOMIC_YANG_MILLS_LOCAL_CONNECTION_V4_1",
        "status": status,
        "checks": checks,
    }
    (RESULTS / "VALIDATION_MODULE41_v4_1.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
