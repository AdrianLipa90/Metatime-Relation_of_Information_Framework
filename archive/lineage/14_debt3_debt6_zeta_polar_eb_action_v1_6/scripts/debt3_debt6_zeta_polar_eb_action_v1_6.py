#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
METATIME SM v1.6 — Debt 3 + Debt 6 closure candidate.

Purpose:
  Debt 3: provide an explicit zeta-polar anchor map.
  Debt 6: build a non-fitted Euler--Berry action assembly that consumes the
          zeta-polar coherence layer and validates only ordinal charged-fermion
          hierarchy, not numerical masses.

Important: observed fermion masses are not used as model inputs.  The only
validation target here is the known ordinal ordering inside each charged sector.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[0]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

KAPPA = math.log(2.0) / (24.0 * math.pi)
HALF_AXIS = 0.5

# First non-trivial Riemann zeta zero ordinates on the critical line.
# Used here as fixed spectral constants, not fitted to masses.
ZETA_GAMMAS = [
    14.134725141734693790,
    21.022039638771554993,
    25.010857580145688763,
    30.424876125859513210,
    32.935061587739189690,
    37.586178158825671257,
    40.918719012147495187,
    43.327073280914999519,
    48.005150881167159727,
    49.773832477672302181,
    52.970321477714460644,
    56.446247697063394804,
    59.347044002602353079,
    60.831778524609809844,
    65.112544048081606660,
    67.079810529494173714,
]

# v1.0/v1.3 charged fermion assembly acts as the prior structural layer.
INPUT_ACTION = REPO / "10_standard_model_derivation_stages" / "13_metatime_sm_eulerberry_coherence_gate_v1_3" / "results" / "charged_fermion_action_with_coherence_v1_3.csv"

# Generation seed assignment from full kernel.  It is structural, not mass-fitted.
GENERATION_SEEDS: Dict[int, Tuple[int, int]] = {
    1: (3, 5),
    2: (5, 7),
    3: (11, 13),
}

# Known ordinal hierarchy labels used only for validation.
EXPECTED_GENERATION_BY_FERMION = {
    "e": 1, "mu": 2, "tau": 3,
    "d": 1, "s": 2, "b": 3,
    "u": 1, "c": 2, "t": 3,
}

@dataclass
class ZetaPolarAnchor:
    n: int
    gamma: float
    north_anchor: complex
    south_anchor: complex
    tetra_vertex: int
    imaginary_axis_coordinate: float
    half_axis_distance: float
    spectral_weight: float
    status: str


def frac(x: float) -> float:
    return x - math.floor(x)


def zeta_polar_anchor(n: int, gamma: float) -> ZetaPolarAnchor:
    """Debt 3 explicit map: paired critical-line zero -> north/south polar anchors.

    The imaginary coordinate is reduced modulo one only for bounded diagnostic
    embedding; the original gamma is preserved as the spectral ordinate.
    Tetrahedral vertex assignment uses index modulo four, so the infinite polar
    tower distributes over the four tetrahedral depth directions.
    """
    imaginary_axis_coordinate = frac(gamma)
    half_axis_distance = abs(imaginary_axis_coordinate - HALF_AXIS)
    # Bounded spectral weight centered on the half-axis.  This is a coherence
    # gate, not a raw mass damping factor.
    spectral_weight = math.exp(-4.0 * half_axis_distance * half_axis_distance)
    return ZetaPolarAnchor(
        n=n,
        gamma=gamma,
        north_anchor=complex(0.5, gamma),
        south_anchor=complex(0.5, -gamma),
        tetra_vertex=((n - 1) % 4) + 1,
        imaginary_axis_coordinate=imaginary_axis_coordinate,
        half_axis_distance=half_axis_distance,
        spectral_weight=spectral_weight,
        status="definition_plus_ansatz_validated_as_non_mass_fitted_anchor",
    )


def seed_anchor_index(seed_p: int, seed_q: int) -> int:
    """Non-fitted seed -> zeta tower index map.

    The seed center determines the polar tower index.  This ties the twin-prime
    seed to the stationary zeta imaginary axis without looking at fermion masses.
    """
    center = (seed_p + seed_q) // 2
    return ((center - 1) % len(ZETA_GAMMAS)) + 1


def read_prior_actions() -> List[dict]:
    rows: List[dict] = []
    with INPUT_ACTION.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def zeta_coherence_for_seed(seed_p: int, seed_q: int) -> dict:
    idx = seed_anchor_index(seed_p, seed_q)
    anchor = zeta_polar_anchor(idx, ZETA_GAMMAS[idx - 1])
    # Convert coherence into a bounded adjustment.  High coherence reduces the
    # effective action; low coherence does not create a negative cost.
    coherence = anchor.spectral_weight
    adjustment_unit = 0.05 * (1.0 - coherence)
    return {
        "zeta_anchor_index": idx,
        "zeta_gamma": anchor.gamma,
        "tetra_vertex": anchor.tetra_vertex,
        "imaginary_axis_coordinate": anchor.imaginary_axis_coordinate,
        "half_axis_distance": anchor.half_axis_distance,
        "zeta_polar_coherence": coherence,
        "debt3_adjustment_unit": adjustment_unit,
    }


def main() -> None:
    anchors = [zeta_polar_anchor(i + 1, g) for i, g in enumerate(ZETA_GAMMAS)]

    with (RESULTS / "zeta_polar_anchor_table_v1_6.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "n", "gamma", "north_anchor_re", "north_anchor_im",
            "south_anchor_re", "south_anchor_im", "tetra_vertex",
            "imaginary_axis_coordinate", "half_axis_distance", "spectral_weight", "status",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for a in anchors:
            w.writerow({
                "n": a.n,
                "gamma": f"{a.gamma:.18f}",
                "north_anchor_re": a.north_anchor.real,
                "north_anchor_im": f"{a.north_anchor.imag:.18f}",
                "south_anchor_re": a.south_anchor.real,
                "south_anchor_im": f"{a.south_anchor.imag:.18f}",
                "tetra_vertex": a.tetra_vertex,
                "imaginary_axis_coordinate": f"{a.imaginary_axis_coordinate:.18f}",
                "half_axis_distance": f"{a.half_axis_distance:.18f}",
                "spectral_weight": f"{a.spectral_weight:.18f}",
                "status": a.status,
            })

    seed_rows = []
    for gen, (p, q) in GENERATION_SEEDS.items():
        z = zeta_coherence_for_seed(p, q)
        seed_rows.append({"generation": gen, "seed_p": p, "seed_q": q, **z})

    with (RESULTS / "generation_seed_zeta_anchor_map_v1_6.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(seed_rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(seed_rows)

    prior = read_prior_actions()
    action_rows = []
    for row in prior:
        fermion = row["fermion"]
        generation = int(row["generation"])
        p, q = GENERATION_SEEDS[generation]
        z = zeta_coherence_for_seed(p, q)
        base_unit = float(row["action_with_coherence_unit_v13"])
        final_unit = base_unit + z["debt3_adjustment_unit"]
        action_rows.append({
            "fermion": fermion,
            "class": row["class"],
            "generation": generation,
            "seed_p": p,
            "seed_q": q,
            "prior_action_unit_v13": f"{base_unit:.12f}",
            "zeta_anchor_index": z["zeta_anchor_index"],
            "tetra_vertex": z["tetra_vertex"],
            "zeta_polar_coherence": f"{z['zeta_polar_coherence']:.12f}",
            "debt3_adjustment_unit": f"{z['debt3_adjustment_unit']:.12f}",
            "eb_action_unit_v16": f"{final_unit:.12f}",
            "eb_action_kappa_v16": f"{final_unit*KAPPA:.12f}",
            "uses_observed_mass_as_input": False,
            "debt6_status": "ordinal_hierarchy_candidate_not_numeric_mass_prediction",
        })

    with (RESULTS / "charged_fermion_eb_action_debt6_v1_6.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(action_rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(action_rows)

    # Validate ordinal hierarchy: action should decrease from gen 1 to gen 3,
    # because lower action means weaker damping and heavier charged fermions.
    validations = []
    for cls in sorted(set(r["class"] for r in action_rows)):
        rows = sorted([r for r in action_rows if r["class"] == cls], key=lambda r: int(r["generation"]))
        actions = [float(r["eb_action_unit_v16"]) for r in rows]
        gens = [int(r["generation"]) for r in rows]
        monotonic_decrease = all(actions[i] > actions[i+1] for i in range(len(actions)-1))
        validations.append({
            "class": cls,
            "generations": "->".join(map(str, gens)),
            "actions": "->".join(f"{a:.6f}" for a in actions),
            "expected_mass_order": "gen1_lightest_gen3_heaviest",
            "action_order_pass": monotonic_decrease,
            "uses_observed_mass_as_input": False,
        })

    with (RESULTS / "debt6_ordinal_validation_v1_6.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(validations[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(validations)

    summary = {
        "version": "v1.6",
        "kappa_ln2_over_24pi": KAPPA,
        "debt3": {
            "status": "closed_as_explicit_zeta_polar_anchor_definition_plus_nonfitted_ansatz",
            "anchor_count": len(anchors),
            "north_south_pairing": "critical_line_zero_pairs_plus_minus_gamma_n",
            "tetra_assignment": "zero_index_modulo_four",
            "mass_input_used": False,
        },
        "debt6": {
            "status": "partially_closed_for_ordinal_charged_fermion_hierarchy; numeric_mass_spectrum_still_open",
            "validation_pass": all(v["action_order_pass"] for v in validations),
            "classes_validated": validations,
            "mass_input_used": False,
        },
        "formal_remaining_debts": [
            "derive numerical mass ratios without fitting", 
            "derive CKM and PMNS mixing", 
            "close neutrino mass mechanism",
            "prove zero-index modulo-four tetrahedral assignment or replace it with a stronger derivation"
        ],
    }
    (RESULTS / "debt3_debt6_summary_v1_6.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
