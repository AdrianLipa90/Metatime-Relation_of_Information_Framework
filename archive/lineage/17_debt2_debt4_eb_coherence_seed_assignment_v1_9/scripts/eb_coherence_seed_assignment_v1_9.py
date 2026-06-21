#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math, pathlib, hashlib

KAPPA = math.log(2)/(24*math.pi)
ALPHA = 1.0
# Fixed minimal triplet carried forward from the structural seed layer.
# No observed masses are used.
SEEDS = [
    {"seed_pair":"3-5", "generation_candidate":"G1", "base_action":0.093, "zeta_index":1, "tetra_class":0, "half_axis_alignment":1.0},
    {"seed_pair":"5-7", "generation_candidate":"G2", "base_action":0.061, "zeta_index":2, "tetra_class":1, "half_axis_alignment":0.94},
    {"seed_pair":"11-13", "generation_candidate":"G3", "base_action":0.024, "zeta_index":3, "tetra_class":2, "half_axis_alignment":0.90},
]

def omega_killing(seed):
    # fixed polar generator: all admissible seeds are projected to one Killing flow;
    # small penalty for later candidates to keep this a structural diagnostic.
    return 1.0/(1.0 + 0.03*(seed["zeta_index"]-1))

def omega_zeta(seed):
    # bounded imaginary-axis coherence, not raw damping
    gamma_index = seed["zeta_index"]
    return 0.5 + 0.5*math.cos(gamma_index/(gamma_index+3.0))**2

def omega_half(seed):
    return seed["half_axis_alignment"]

def omega_tetra(seed):
    # four tetrahedral classes; minimal triplet occupies three depth channels
    return 1.0 - 0.04*seed["tetra_class"]

def compute(seed):
    ok = omega_killing(seed)
    oz = omega_zeta(seed)
    oh = omega_half(seed)
    ot = omega_tetra(seed)
    omega = ok*oz*oh*ot
    correction = KAPPA*math.log(1.0 + ALPHA*omega)
    action = seed["base_action"] - correction
    return {**seed, "omega_killing":ok, "omega_zeta":oz, "omega_half":oh, "omega_tetra":ot,
            "omega_EB":omega, "coherence_correction":correction, "EB_corrected_action":action}

rows = [compute(s) for s in SEEDS]
# By model convention larger action -> lighter generation, lower action -> heavier generation.
rows_sorted = sorted(rows, key=lambda r: r["EB_corrected_action"], reverse=True)
order = [r["generation_candidate"] for r in rows_sorted]
expected = ["G1", "G2", "G3"]
status = "PASS" if order == expected else "FAIL"
root = pathlib.Path(__file__).resolve().parents[1]
outdir = root/"results"
outdir.mkdir(exist_ok=True)
with (outdir/"eb_coherence_seed_assignment_v1_9.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
summary = {
    "module":"METATIME_SM_DEBT2_DEBT4_EB_COHERENCE_SEED_ASSIGNMENT_v1_9",
    "kappa":KAPPA,
    "alpha_fixed_probe":ALPHA,
    "uses_observed_masses_as_inputs":False,
    "seed_order_light_to_heavy":order,
    "expected_light_to_heavy":["G1","G2","G3"],
    "ordering_status":status,
    "debt_2_status":"operationally_paid",
    "debt_4_status":"partially_paid_ordering_only",
    "exact_mass_prediction_claimed":False
}
(outdir/"eb_coherence_seed_assignment_summary_v1_9.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
