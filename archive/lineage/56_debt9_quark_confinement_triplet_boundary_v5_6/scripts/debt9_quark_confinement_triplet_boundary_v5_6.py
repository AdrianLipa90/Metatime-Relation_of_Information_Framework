#!/usr/bin/env python3
"""
Module 56: Quark confinement / hadron-triplet boundary for Debt 9.

Purpose:
- preserve v5.4/v5.5 charged-lepton freeze,
- stop evaluating quarks by exact isolated single-quark closure,
- introduce a diagnostic confinement/hadronization residual budget around 21%,
- require a future triplet-hadron aggregation test before any quark numeric closure claim.

This executable does not import old solvers and does not optimize parameters.
"""
import json, pathlib, csv, hashlib, datetime

MODULE = "56_debt9_quark_confinement_triplet_boundary_v5_6"
SCHEMA = "METATIME_DEBT9_QUARK_CONFINEMENT_TRIPLET_BOUNDARY_V5_6"
CONFINEMENT_RESIDUAL_BUDGET = 0.21
ROOT = pathlib.Path(__file__).resolve().parents[2]
INPUT = ROOT / "55_debt9_lepton_freeze_full_sector_boundary_v5_5" / "results" / "debt9_lepton_freeze_full_sector_boundary_v5_5.json"
OUT_JSON = ROOT / MODULE / "results" / "debt9_quark_confinement_triplet_boundary_v5_6.json"
OUT_CSV = ROOT / MODULE / "results" / "debt9_quark_confinement_triplet_boundary_v5_6.csv"

with INPUT.open("r", encoding="utf-8") as f:
    v55 = json.load(f)

rows = v55.get("blind_full_charged_fermion_boundary_probe_rows", [])
quark_rows = [r for r in rows if "quark" in r.get("family", "")]
lepton_rows = v55.get("charged_lepton_rows", [])

classified = []
for r in quark_rows:
    slot = r["slot"]
    err = float(r["blind_extended_absolute_relative_error"])
    anchor = bool(r.get("unit_anchor_slot", False))
    if anchor:
        status = "ANCHOR_NOT_PROBATIVE"
        closure_allowed = False
    elif err <= CONFINEMENT_RESIDUAL_BUDGET:
        status = "WITHIN_CONFINEMENT_RESIDUAL_BUDGET_DIAGNOSTIC_ONLY"
        closure_allowed = False
    else:
        status = "OUTSIDE_CONFINEMENT_RESIDUAL_BUDGET_NEEDS_TRIPLET_HADRONIZATION"
        closure_allowed = False
    classified.append({
        "slot": slot,
        "family": r["family"],
        "single_quark_prediction_mev_from_prior_probe": r["blind_extended_prediction_mev"],
        "reference_benchmark_mev_scoring_only": r["benchmark_mev_post_freeze_scoring_only"],
        "absolute_relative_residual": err,
        "confinement_residual_budget": CONFINEMENT_RESIDUAL_BUDGET,
        "within_budget": (not anchor) and err <= CONFINEMENT_RESIDUAL_BUDGET,
        "unit_anchor_slot": anchor,
        "quark_single_state_observable": False,
        "triplet_hadron_test_required": True,
        "status": status,
        "numeric_closure_allowed": closure_allowed,
    })

non_anchor = [r for r in classified if not r["unit_anchor_slot"]]
within = [r for r in non_anchor if r["within_budget"]]
outside = [r for r in non_anchor if not r["within_budget"]]

summary_payload = {
    "schema": SCHEMA,
    "module": MODULE,
    "created_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    "technical_status": "PASS",
    "formal_status": "PASS_WITH_CONFINEMENT_BOUNDARY",
    "substantive_status": "QUARK_SINGLE_STATE_EXACT_CLOSURE_DENIED_TRIPLET_BOUNDARY_INSTALLED",
    "debt9_numeric_spectrum": "OPEN_NOT_CLOSED",
    "canon_allowed": False,
    "current_promotion": "DENY_CURRENT",
    "mass_closure_claimed": False,
    "user_correction_integrated": {
        "claim": "Quarks are a different sector; isolated quarks are unstable/non-asymptotic, and the meaningful diagnostic should tolerate about 21% confinement/hadronization spread before triplet aggregation.",
        "implemented_as": "confinement_residual_budget_for_single_quark_diagnostics_only",
        "budget": CONFINEMENT_RESIDUAL_BUDGET,
        "not_implemented_as": "automatic Debt 9 closure or arbitrary error forgiveness",
    },
    "charged_lepton_freeze_preserved": {
        "source": "v5.5 charged_lepton_rows",
        "rows": lepton_rows,
        "status": "UNCHANGED_STRONG_DIAGNOSTIC_NOT_FULL_DEBT9_CLOSURE",
    },
    "quark_boundary_rows": classified,
    "metrics": {
        "quark_non_anchor_slots": len(non_anchor),
        "within_21_percent_budget_count": len(within),
        "outside_21_percent_budget_count": len(outside),
        "within_budget_slots": [r["slot"] for r in within],
        "outside_budget_slots": [r["slot"] for r in outside],
        "mean_single_quark_residual_non_anchor": sum(r["absolute_relative_residual"] for r in non_anchor)/len(non_anchor) if non_anchor else None,
        "max_single_quark_residual_non_anchor": max((r["absolute_relative_residual"] for r in non_anchor), default=None),
    },
    "decision": {
        "single_quark_exact_mass_scoring": "DENIED_AS_CLOSURE_CRITERION",
        "confinement_budget_21_percent": "ACCEPTED_AS_DIAGNOSTIC_BOUNDARY_ONLY",
        "triplet_hadron_aggregation": "REQUIRED_NEXT",
        "debt9_quark_sector": "OPEN_PENDING_TRIPLET_WIJ_HADRONIZATION_OPERATOR",
        "debt9_total": "OPEN_NOT_CLOSED",
    },
    "next_step": "v5.7 should build a triplet W_ij hadronization aggregator from tetrahedral triplet + holonomic gluon couplings, then score baryon/meson-level observables rather than isolated quark exact masses.",
}

fingerprint_src = json.dumps({
    "budget": CONFINEMENT_RESIDUAL_BUDGET,
    "classified": classified,
    "decision": summary_payload["decision"],
}, sort_keys=True).encode("utf-8")
summary_payload["formula_fingerprint_sha256"] = hashlib.sha256(fingerprint_src).hexdigest()

OUT_JSON.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
    fieldnames = [
        "slot","family","single_quark_prediction_mev_from_prior_probe","reference_benchmark_mev_scoring_only",
        "absolute_relative_residual","confinement_residual_budget","within_budget","unit_anchor_slot",
        "quark_single_state_observable","triplet_hadron_test_required","status","numeric_closure_allowed"
    ]
    w=csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for row in classified:
        w.writerow({k: row[k] for k in fieldnames})
print(json.dumps({"status":"PASS", "out": str(OUT_JSON), "fingerprint": summary_payload["formula_fingerprint_sha256"]}, indent=2))
