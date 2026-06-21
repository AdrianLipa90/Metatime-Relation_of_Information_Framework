#!/usr/bin/env python3
"""
Debt 9 one-anchor mass scaling pilot v2.6.

This script is deliberately a stress test, not a mass derivation claim.
It uses exactly one observed Standard Model mass as the dimensional anchor: electron mass.
All other observed masses are validation targets only.

Inputs are previous v2.x structural artifacts:
- EB action table v1.6;
- Ramanujan seed suppression table v2.1;
- zeta-Heisenberg fluctuation diagnostics v2.0;
- validation target table v0.1.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(parents=True, exist_ok=True)

KAPPA = math.log(2.0) / (24.0 * math.pi)
ANCHOR = "e"
VEV_GEV = 246.0
SQRT2 = math.sqrt(2.0)

ACTION_CSV = ROOT / "14_debt3_debt6_zeta_polar_eb_action_v1_6/results/charged_fermion_eb_action_debt6_v1_6.csv"
RAMANUJAN_CSV = ROOT / "19_debt5_ramanujan_seed_suppression_v2_1/results/ramanujan_seed_suppression_table_v2_1.csv"
ZH_CSV = ROOT / "18_preference_zeta_heisenberg_fluctuation_v2_0/results/preference_zeta_heisenberg_seed_diagnostics_v2_0.csv"
TARGET_CSV = ROOT / "10_standard_model_derivation_stages/02_metatime_sm_mass_vectorization_v0_1/mass_action_validation_targets.csv"


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ffloat(row, key):
    return float(row[key])


def seed_pair(row):
    return f"{int(float(row['seed_p']))}-{int(float(row['seed_q']))}"


def main() -> None:
    action_rows = read_csv(ACTION_CSV)
    ram_rows = read_csv(RAMANUJAN_CSV)
    zh_rows = read_csv(ZH_CSV)
    target_rows = read_csv(TARGET_CSV)

    ram_by_seed = {seed_pair(r): r for r in ram_rows}
    zh_by_seed = {seed_pair(r): r for r in zh_rows}
    targets = {r["fermion"]: r for r in target_rows}

    merged = []
    for r in action_rows:
        sp = seed_pair(r)
        if sp not in ram_by_seed or sp not in zh_by_seed or r["fermion"] not in targets:
            continue
        rr = ram_by_seed[sp]
        zr = zh_by_seed[sp]
        tr = targets[r["fermion"]]
        merged.append({
            "fermion": r["fermion"],
            "class": r["class"],
            "generation": int(r["generation"]),
            "seed_pair": sp,
            "eb_action_kappa": ffloat(r, "eb_action_kappa_v16"),
            "eb_action_unit": ffloat(r, "eb_action_unit_v16"),
            "ramanujan_scaled_action": ffloat(rr, "ramanujan_scaled_action"),
            "ramanujan_visibility": ffloat(rr, "visibility"),
            "ramanujan_entropy_norm": ffloat(rr, "hardy_ramanujan_entropy_norm"),
            "ramanujan_resonance": ffloat(rr, "ramanujan_resonance"),
            "phase_uncertainty": ffloat(zr, "phase_uncertainty"),
            "preference_width": ffloat(zr, "preference_width"),
            "target_mass_GeV": ffloat(tr, "mass_GeV"),
            "target_S_required": ffloat(tr, "S_required_if_y_exp_minus_S_over_kappa"),
            "target_minus_ln_y": ffloat(tr, "minus_ln_y"),
            "target_status": tr["target_status"],
        })

    anchor = next(r for r in merged if r["fermion"] == ANCHOR)
    S_anchor = anchor["target_S_required"]
    m_anchor = anchor["target_mass_GeV"]
    A_anchor = anchor["eb_action_kappa"]
    R_anchor = anchor["ramanujan_scaled_action"]
    U_anchor = anchor["phase_uncertainty"]
    W_anchor = anchor["preference_width"]

    variants = {
        "EB_ONLY": {
            "description": "electron anchored EB action only",
            "uses_ramanujan": False,
            "uses_zeta_heisenberg": False,
        },
        "EB_MINUS_RAMANUJAN": {
            "description": "electron anchored EB action with Ramanujan release term",
            "uses_ramanujan": True,
            "uses_zeta_heisenberg": False,
        },
        "EB_MINUS_RAMANUJAN_ZH_CENTER": {
            "description": "same as EB_MINUS_RAMANUJAN plus zeta-Heisenberg central phase correction",
            "uses_ramanujan": True,
            "uses_zeta_heisenberg": True,
        },
    }

    rows = []
    for variant in variants:
        for r in merged:
            # One-anchor map: structural suppression S is anchored by the electron target S.
            S = S_anchor * (r["eb_action_kappa"] / A_anchor)
            if variant in ("EB_MINUS_RAMANUJAN", "EB_MINUS_RAMANUJAN_ZH_CENTER"):
                # Ramanujan layer is a release/tunnelling term: larger Ramanujan action in deeper seed
                # reduces the suppression. This is an ansatz, not fitted to masses.
                S -= (r["ramanujan_scaled_action"] - R_anchor)
            if variant == "EB_MINUS_RAMANUJAN_ZH_CENTER":
                # zeta-Heisenberg fluctuation central correction, still not a fitted knob.
                S -= KAPPA * (r["phase_uncertainty"] - U_anchor)

            y_pred = math.exp(-S / KAPPA)
            mass_pred = y_pred * VEV_GEV / SQRT2
            ratio_to_anchor_pred = mass_pred / m_anchor
            ratio_to_anchor_target = r["target_mass_GeV"] / m_anchor
            log_error = math.log(mass_pred / r["target_mass_GeV"])
            abs_log_error = abs(log_error)

            # zeta-Heisenberg width as uncertainty band in S, not tuned per particle.
            width_S = KAPPA * max(r["preference_width"], W_anchor)
            mass_low = math.exp(-(S + width_S) / KAPPA) * VEV_GEV / SQRT2
            mass_high = math.exp(-(S - width_S) / KAPPA) * VEV_GEV / SQRT2
            target_in_band = mass_low <= r["target_mass_GeV"] <= mass_high

            rows.append({
                "variant": variant,
                "fermion": r["fermion"],
                "class": r["class"],
                "generation": r["generation"],
                "seed_pair": r["seed_pair"],
                "anchor_used": ANCHOR,
                "is_anchor": r["fermion"] == ANCHOR,
                "S_pred": S,
                "S_target_validation_only": r["target_S_required"],
                "target_minus_ln_y_validation_only": r["target_minus_ln_y"],
                "mass_pred_GeV": mass_pred,
                "mass_pred_low_GeV": mass_low,
                "mass_pred_high_GeV": mass_high,
                "target_mass_GeV_validation_only": r["target_mass_GeV"],
                "target_in_zeta_heisenberg_band": target_in_band,
                "ratio_to_anchor_pred": ratio_to_anchor_pred,
                "ratio_to_anchor_target_validation_only": ratio_to_anchor_target,
                "log_error_vs_target": log_error,
                "abs_log_error_vs_target": abs_log_error,
                "eb_action_kappa": r["eb_action_kappa"],
                "ramanujan_scaled_action": r["ramanujan_scaled_action"],
                "phase_uncertainty": r["phase_uncertainty"],
                "preference_width": r["preference_width"],
                "uses_observed_mass_as_input": r["fermion"] == ANCHOR,
            })

    # variant summaries excluding the anchor
    summary_rows = []
    for variant in variants:
        vr = [r for r in rows if r["variant"] == variant and not r["is_anchor"]]
        abs_logs = [r["abs_log_error_vs_target"] for r in vr]
        in_band_count = sum(1 for r in vr if r["target_in_zeta_heisenberg_band"])
        # class order checks
        class_order = {}
        for cls in sorted({r["class"] for r in vr}):
            cr = sorted([x for x in rows if x["variant"] == variant and x["class"] == cls], key=lambda x: x["generation"])
            pred_masses = [x["mass_pred_GeV"] for x in cr]
            class_order[cls] = all(pred_masses[i] < pred_masses[i+1] for i in range(len(pred_masses)-1))
        summary_rows.append({
            "variant": variant,
            "gate_class": "COMPUTATIONAL_STRESS_TEST_PASS",
            "debt9_closure_status": "NOT_CLOSED_NUMERIC_RATIOS_REMAIN_OPEN",
            "anchor": ANCHOR,
            "anchor_mass_GeV": m_anchor,
            "non_anchor_count": len(vr),
            "median_abs_log_error_excluding_anchor": median(abs_logs),
            "max_abs_log_error_excluding_anchor": max(abs_logs),
            "targets_inside_zeta_heisenberg_band_excluding_anchor": in_band_count,
            "charged_lepton_generation_order_pass": class_order.get("charged_lepton", False),
            "down_quark_generation_order_pass": class_order.get("down_quark", False),
            "up_quark_generation_order_pass": class_order.get("up_quark", False),
            "uses_observed_masses_as_inputs_other_than_anchor": False,
        })

    # debt ledger update
    ledger = [
        {"debt": "Debt 9", "status": "partially advanced / not closed", "note": "One-anchor pipeline implemented; ratios are a stress test and do not yet match charged fermion spectrum."},
        {"debt": "Debt 5", "status": "dependency reused", "note": "Ramanujan seed suppression enters scaling as mandatory non-fit layer."},
        {"debt": "zeta-Heisenberg fluctuation", "status": "dependency reused", "note": "Used as uncertainty/coherence width, not as fitted correction."},
    ]

    # write outputs
    fieldnames = list(rows[0].keys())
    with (OUT / "one_anchor_mass_scaling_predictions_v2_6.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)

    fieldnames = list(summary_rows[0].keys())
    with (OUT / "one_anchor_mass_scaling_summary_v2_6.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(summary_rows)

    with (OUT / "debt9_status_update_v2_6.json").open("w", encoding="utf-8") as f:
        json.dump({
            "module": "debt9_one_anchor_mass_scaling_v2_6",
            "anchor": ANCHOR,
            "anchor_mass_GeV": m_anchor,
            "kappa_ln2_over_24pi": KAPPA,
            "vev_GeV_used_for_yukawa_conversion": VEV_GEV,
            "observed_masses_used_as_inputs": [ANCHOR],
            "observed_masses_used_as_validation_targets": [r["fermion"] for r in merged if r["fermion"] != ANCHOR],
            "debt9_status": "PARTIAL_ADVANCE_NOT_CLOSED",
            "gate_class": "COMPUTATIONAL_STRESS_TEST_PASS",
            "debt_ledger": ledger,
            "summary": summary_rows,
        }, f, indent=2)

    print(json.dumps({
        "status": "PASS",
        "gate_class": "COMPUTATIONAL_STRESS_TEST_PASS",
        "debt9_status": "PARTIAL_ADVANCE_NOT_CLOSED",
        "anchor": ANCHOR,
        "row_count": len(rows),
        "summary": summary_rows,
    }, indent=2))


if __name__ == "__main__":
    main()
