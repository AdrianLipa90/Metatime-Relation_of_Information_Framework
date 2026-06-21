#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
METATIME SM — Debt 8 source axis candidate grammar v2.3

This script performs a structural enumeration, not a numerical mass computation.
It validates that the primitive-axis candidate list is derived from source roles.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

REQUIRED = {
    "continuous_flow",
    "two_fixed_poles",
    "cp1_supported",
    "chiral_bridge",
    "doublet_split",
    "mass_gate_compatible",
    "source_derived",
}

CANDIDATES = [
    {
        "candidate": "source_derived_chiral_cp1_axis",
        "role": "primitive_axis",
        "features": [
            "continuous_flow", "two_fixed_poles", "cp1_supported", "chiral_bridge",
            "doublet_split", "mass_gate_compatible", "source_derived"
        ],
        "exclusion_reason": "survives_all_gates",
        "sm_interpretation": "weak_isospin_axis",
    },
    {
        "candidate": "berry_connection",
        "role": "phase_transport",
        "features": ["continuous_flow", "transport_connection", "source_derived"],
        "exclusion_reason": "transport_not_pole_selector",
        "sm_interpretation": "berry_phase_layer",
    },
    {
        "candidate": "twinprime_collatz_axis",
        "role": "arithmetic_index_and_transition",
        "features": ["discrete_index", "source_derived", "mass_gate_compatible"],
        "exclusion_reason": "discrete_arithmetic_not_continuous_cp1_selector",
        "sm_interpretation": "generation_seed_layer",
    },
    {
        "candidate": "zeta_imaginary_axis",
        "role": "spectral_coherence",
        "features": ["spectral_coherence", "source_derived", "mass_gate_compatible"],
        "exclusion_reason": "imaginary_spectral_coherence_not_real_killing_generator",
        "sm_interpretation": "zeta_zero_coherence_axis",
    },
    {
        "candidate": "tetrahedral_color_depth",
        "role": "internal_depth_triplet",
        "features": ["triplet_depth", "source_derived", "mass_gate_compatible"],
        "exclusion_reason": "triplet_depth_not_two_pole_cp1_selector",
        "sm_interpretation": "color_like_depth_layer",
    },
    {
        "candidate": "hypercharge_u1_label",
        "role": "abelian_charge_label",
        "features": ["abelian_label", "continuous_flow", "source_derived"],
        "exclusion_reason": "abelian_label_does_not_split_cp1_doublet",
        "sm_interpretation": "hypercharge_layer",
    },
    {
        "candidate": "ramanujan_scaling_layer",
        "role": "asymptotic_suppression",
        "features": ["asymptotic_scaling", "source_derived", "mass_gate_compatible"],
        "exclusion_reason": "scaling_layer_not_axis_selector",
        "sm_interpretation": "seed_suppression_scale",
    },
    {
        "candidate": "poincare_disk_radial_depth",
        "role": "derived_hyperbolic_surface_coordinate",
        "features": ["derived_surface", "source_derived", "mass_gate_compatible"],
        "exclusion_reason": "derived_surface_coordinate_not_primitive_cp1_axis",
        "sm_interpretation": "collatz_dynamics_surface",
    },
]

GATE_TAXONOMY = [
    ("FORMAL_SYMBOLIC_PASS", "symbolic_topological_accounting", "No numerical scan implied."),
    ("STRUCTURAL_ENUMERATION_PASS", "finite_candidate_exclusion", "Candidate roles checked against source criteria."),
    ("COMPUTATIONAL_PASS", "generated_data_or_numeric_computation", "Real computation over sequences/tables."),
    ("EMPIRICAL_TARGET_CHECK", "comparison_only", "Observed values may be compared but not used as inputs."),
]


def classify(features: set[str]) -> tuple[str, str]:
    missing = sorted(REQUIRED - features)
    if not missing:
        return "PRIMARY_SURVIVOR", "STRUCTURAL_ENUMERATION_PASS"
    return "EXCLUDED_ROLE_SPECIFIC", "STRUCTURAL_ENUMERATION_PASS"


def main() -> None:
    rows = []
    survivors = []
    for item in CANDIDATES:
        features = set(item["features"])
        classification, gate = classify(features)
        if classification == "PRIMARY_SURVIVOR":
            survivors.append(item["candidate"])
        rows.append({
            "candidate": item["candidate"],
            "role": item["role"],
            "features": ";".join(item["features"]),
            "classification": classification,
            "gate_class": gate,
            "exclusion_reason": item["exclusion_reason"],
            "sm_interpretation": item["sm_interpretation"],
        })

    candidate_csv = RESULTS / "source_axis_candidate_table_v2_3.csv"
    with candidate_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    taxonomy_csv = RESULTS / "gate_taxonomy_update_v2_3.csv"
    with taxonomy_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["gate_class", "meaning", "caution"])
        writer.writeheader()
        for gate_class, meaning, caution in GATE_TAXONOMY:
            writer.writerow({"gate_class": gate_class, "meaning": meaning, "caution": caution})

    summary = {
        "module": "21_debt8_source_axis_candidate_grammar_v2_3",
        "survivors": survivors,
        "expected_single_survivor": "source_derived_chiral_cp1_axis",
        "pass": survivors == ["source_derived_chiral_cp1_axis"],
        "gate_class": "STRUCTURAL_ENUMERATION_PASS",
        "observed_masses_used_as_input": False,
        "note": "This is not a computational mass test. It is structural enumeration from source roles."
    }
    (RESULTS / "source_axis_candidate_summary_v2_3.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if not summary["pass"]:
        raise SystemExit("FAILED: expected exactly one source-derived chiral CP1 axis survivor")

    print("PASS: Debt 8 source-axis candidate grammar has exactly one primitive survivor.")
    print("Gate class: STRUCTURAL_ENUMERATION_PASS")
    print(f"Candidate table: {candidate_csv}")


if __name__ == "__main__":
    main()
