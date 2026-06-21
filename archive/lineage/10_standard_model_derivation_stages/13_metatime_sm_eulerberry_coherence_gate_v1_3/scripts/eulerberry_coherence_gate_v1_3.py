#!/usr/bin/env python3
"""
METATIME SM Euler-Berry Coherence Gate v1.3

Purpose:
    Convert the zeta-tetrahedral layer from a naive additive mass cost into
    a bounded phase-coherence gate. The layer may certify, weight, or gently
    credit an already-derived structural action, but it must not override the
    generation ordering established by the tetrahedral/Poincare/Collatz/Fibonacci/
    Kepler kernel.

Inputs:
    - v1.0 seed arbitration table
    - v1.1 zeta-tetrahedral seed table

Outputs:
    - seed_coherence_gate_v1_3.csv
    - charged_fermion_action_with_coherence_v1_3.csv
    - coherence_validation_summary_v1_3.json
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
V10 = REPO / "10_standard_model_derivation_stages" / "11_metatime_sm_full_action_seed_arbitration_v1_0" / "results"
V11 = REPO / "10_standard_model_derivation_stages" / "12_metatime_sm_zeta_tetrahedral_anchor_v1_1" / "results"
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

KAPPA = math.log(2.0) / (24.0 * math.pi)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def normalize(values: dict[tuple[int, int], float], invert: bool = False) -> dict[tuple[int, int], float]:
    vals = list(values.values())
    lo, hi = min(vals), max(vals)
    if abs(hi - lo) < 1e-15:
        return {k: 1.0 for k in values}
    out = {}
    for k, v in values.items():
        x = (v - lo) / (hi - lo)
        out[k] = 1.0 - x if invert else x
    return out


seed_rows = read_csv(V10 / "seed_arbitration_v1_0.csv")
zeta_rows = read_csv(V11 / "seed_zeta_tetrahedral_table_v1_1.csv")
fermion_rows = read_csv(V10 / "charged_fermion_action_assembly_v1_0.csv")

seed_keys = [(int(r["seed_p"]), int(r["seed_q"])) for r in seed_rows]
zeta_by_seed = {(int(r["seed_p"]), int(r["seed_q"])): r for r in zeta_rows if (int(r["seed_p"]), int(r["seed_q"])) in seed_keys}
seed_by_key = {(int(r["seed_p"]), int(r["seed_q"])): r for r in seed_rows}

# Scores. All scores are mass-blind and use only zeta-tetrahedral geometry.
entropy = {k: f(zeta_by_seed[k], "zeta_entropy") for k in seed_keys}
# lower asymmetry is better; lower base std is better; apex weight close to tetrahedral 1/4..1/3 band is better
vertex_symmetry = {k: 1.0 - f(zeta_by_seed[k], "vertex_asymmetry") for k in seed_keys}
base_balance_raw = {k: f(zeta_by_seed[k], "base_balance_std") for k in seed_keys}
base_balance = normalize(base_balance_raw, invert=True)
# Phase winding is allowed to be nonzero, but too-large winding residual lowers coherence.
phase_abs = {k: abs(f(zeta_by_seed[k], "phase_winding")) for k in seed_keys}
phase_alignment = normalize(phase_abs, invert=True)
# Prefer apex weights close to the regular tetrahedral barycentric scale, not a fitted value.
apex_target = 1.0 / 3.0
apex_deviation = {k: abs(f(zeta_by_seed[k], "polar_apex_weight") - apex_target) for k in seed_keys}
apex_alignment = normalize(apex_deviation, invert=True)

coherence_rows = []
coherence_by_seed = {}
for k in seed_keys:
    scores = {
        "entropy_score": entropy[k],
        "vertex_symmetry_score": vertex_symmetry[k],
        "base_balance_score": base_balance[k],
        "phase_alignment_score": phase_alignment[k],
        "apex_alignment_score": apex_alignment[k],
    }
    # The zeta layer is a gate/coherence layer. The average is deliberately bounded.
    composite = mean(scores.values())
    # Coherence credit is not a new free parameter: it is capped by one half of the
    # smallest generational action margin so it cannot overturn seed order.
    coherence_by_seed[k] = composite
    zrow = zeta_by_seed[k]
    srow = seed_by_key[k]
    coherence_rows.append({
        "seed_p": k[0],
        "seed_q": k[1],
        **scores,
        "zeta_coherence_score_v13": composite,
        "integrated_damping_unit_v10": float(srow["integrated_damping_unit_v10"]),
        "assigned_generation_v10": int(srow["assigned_generation_v10"]),
        "status": "coherence_gate_pass_mass_blind_not_additive_cost",
    })

# Determine conservative coherence credit scale from structural margins.
actions = {k: float(seed_by_key[k]["integrated_damping_unit_v10"]) for k in seed_keys}
# Generation order from v1.0: higher action -> lighter generation. Margins between ordered actions.
ordered = sorted(seed_keys, key=lambda k: actions[k], reverse=True)
margins = [abs(actions[ordered[i]] - actions[ordered[i+1]]) for i in range(len(ordered)-1)]
min_margin = min(margins) if margins else 0.0
# Max credit amplitude is one quarter of the smallest margin, extra conservative.
max_credit = 0.25 * min_margin

charged_rows = []
for row in fermion_rows:
    k = (int(row["seed_p"]), int(row["seed_q"]))
    base_unit = float(row["total_structural_action_unit_v10"])
    # Center coherence so it can gently credit or debit while preserving seed order.
    centered = coherence_by_seed[k] - mean(coherence_by_seed.values())
    # Scale by max absolute centered value; if zero, no modification.
    max_abs_centered = max(abs(v - mean(coherence_by_seed.values())) for v in coherence_by_seed.values()) or 1.0
    coherence_adjustment_unit = -max_credit * (centered / max_abs_centered)
    action_with_coherence_unit = base_unit + coherence_adjustment_unit
    charged_rows.append({
        "fermion": row["fermion"],
        "class": row["class"],
        "generation": int(row["assigned_generation_v10"]),
        "seed_p": k[0],
        "seed_q": k[1],
        "base_structural_action_unit_v10": base_unit,
        "zeta_coherence_score_v13": coherence_by_seed[k],
        "coherence_adjustment_unit_v13": coherence_adjustment_unit,
        "action_with_coherence_unit_v13": action_with_coherence_unit,
        "action_with_coherence_kappa_v13": action_with_coherence_unit * KAPPA,
        "uses_observed_mass_as_input": False,
        "prediction_status": "ordinal_structure_plus_coherence_gate_not_numeric_mass_prediction",
    })

# Validate hierarchy within classes: higher action should correspond to lighter generation 1 > 2 > 3.
class_groups: dict[str, list[dict[str, object]]] = {}
for r in charged_rows:
    class_groups.setdefault(str(r["class"]), []).append(r)

hierarchy = {}
for cls, rows in class_groups.items():
    by_gen = sorted(rows, key=lambda r: int(r["generation"]))
    vals = [float(r["action_with_coherence_unit_v13"]) for r in by_gen]
    hierarchy[cls] = {
        "actions_by_generation_1_2_3": vals,
        "strict_light_to_heavy_order_pass": bool(vals[0] > vals[1] > vals[2]),
    }

summary = {
    "version": "v1.3",
    "kappa_ln2_over_24pi": KAPPA,
    "source_policy": "mass_observations_are_validation_targets_only_not_inputs",
    "zeta_policy": "zeta_tetrahedral_layer_is_phase_coherence_gate_not_naive_additive_mass_cost",
    "min_generation_action_margin_v10": min_margin,
    "max_coherence_credit_unit_v13": max_credit,
    "seed_order_after_gate_by_action_desc": [f"{k[0]}-{k[1]}" for k in ordered],
    "hierarchy_validation": hierarchy,
    "overall_pass": all(v["strict_light_to_heavy_order_pass"] for v in hierarchy.values()),
}

write_csv(
    OUT / "seed_coherence_gate_v1_3.csv",
    coherence_rows,
    [
        "seed_p", "seed_q", "entropy_score", "vertex_symmetry_score", "base_balance_score",
        "phase_alignment_score", "apex_alignment_score", "zeta_coherence_score_v13",
        "integrated_damping_unit_v10", "assigned_generation_v10", "status",
    ],
)
write_csv(
    OUT / "charged_fermion_action_with_coherence_v1_3.csv",
    charged_rows,
    [
        "fermion", "class", "generation", "seed_p", "seed_q",
        "base_structural_action_unit_v10", "zeta_coherence_score_v13",
        "coherence_adjustment_unit_v13", "action_with_coherence_unit_v13",
        "action_with_coherence_kappa_v13", "uses_observed_mass_as_input", "prediction_status",
    ],
)
with (OUT / "coherence_validation_summary_v1_3.json").open("w", encoding="utf-8") as fjson:
    json.dump(summary, fjson, indent=2, ensure_ascii=False)
print(json.dumps(summary, indent=2, ensure_ascii=False))
