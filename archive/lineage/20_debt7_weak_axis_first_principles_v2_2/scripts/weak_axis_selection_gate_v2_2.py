#!/usr/bin/env python3
"""Debt 7 weak-axis structural enumeration gate v2.2.

This is not an empirical mass-prediction test. It is a structural-enumeration
check: enumerate candidate axes and verify that exactly one satisfies the
primitive CP1 polar-axis requirements.
"""
from __future__ import annotations
import csv, json
from pathlib import Path

REQUIREMENTS = [
    "two_pole",
    "killing_flow",
    "chirality",
    "charge_splitting",
    "mass_gate",
    "non_arithmetic_selector",
    "non_connection_only",
]

CANDIDATES = [
    {
        "candidate": "Berry phase axis",
        "two_pole": True,
        "killing_flow": False,
        "chirality": False,
        "charge_splitting": False,
        "mass_gate": False,
        "non_arithmetic_selector": True,
        "non_connection_only": False,
        "reason": "connection/transport layer, not primitive selector",
    },
    {
        "candidate": "weak isospin / Bloch quantization axis",
        "two_pole": True,
        "killing_flow": True,
        "chirality": True,
        "charge_splitting": True,
        "mass_gate": True,
        "non_arithmetic_selector": True,
        "non_connection_only": True,
        "reason": "two-component chiral doublet axis; supplies T3 polar pair",
    },
    {
        "candidate": "twin-prime / Collatz generation axis",
        "two_pole": False,
        "killing_flow": False,
        "chirality": False,
        "charge_splitting": False,
        "mass_gate": True,
        "non_arithmetic_selector": False,
        "non_connection_only": True,
        "reason": "discrete arithmetic sector label/projection, not smooth CP1 selector",
    },
    {
        "candidate": "zeta imaginary-zero axis",
        "two_pole": True,
        "killing_flow": False,
        "chirality": False,
        "charge_splitting": False,
        "mass_gate": True,
        "non_arithmetic_selector": True,
        "non_connection_only": True,
        "reason": "spectral coherence/anchor axis constrained by polar pair",
    },
    {
        "candidate": "color SU(3) axis",
        "two_pole": False,
        "killing_flow": False,
        "chirality": False,
        "charge_splitting": False,
        "mass_gate": True,
        "non_arithmetic_selector": True,
        "non_connection_only": True,
        "reason": "triplet internal multiplicity, not CP1 two-pole chiral selector",
    },
    {
        "candidate": "hypercharge U(1) axis",
        "two_pole": False,
        "killing_flow": True,
        "chirality": False,
        "charge_splitting": False,
        "mass_gate": False,
        "non_arithmetic_selector": True,
        "non_connection_only": True,
        "reason": "single U(1) label cannot split a weak doublet by itself",
    },
]

def main() -> int:
    outdir = Path(__file__).resolve().parents[1] / "results"
    outdir.mkdir(exist_ok=True)
    rows = []
    for c in CANDIDATES:
        score = sum(1 for req in REQUIREMENTS if c[req])
        selected = all(c[req] for req in REQUIREMENTS)
        rows.append({
            "candidate": c["candidate"],
            **{req: int(c[req]) for req in REQUIREMENTS},
            "score": score,
            "selected": int(selected),
            "reason": c["reason"],
        })
    selected_rows = [r for r in rows if r["selected"] == 1]
    status = "PASS" if len(selected_rows) == 1 and selected_rows[0]["candidate"].startswith("weak isospin") else "FAIL"
    with (outdir / "axis_candidate_gate_v2_2.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    summary = {
        "gate_id": "DEBT7_WEAK_AXIS_STRUCTURAL_ENUMERATION_v2_2",
        "gate_type": "structural_enumeration_pass",
        "premises_used": REQUIREMENTS,
        "independent_computation": False,
        "uses_observed_masses_as_input": False,
        "status": status,
        "selected_candidates": [r["candidate"] for r in selected_rows],
        "note": "Finite structural candidate enumeration; not empirical mass prediction.",
    }
    (outdir / "axis_candidate_gate_summary_v2_2.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
