#!/usr/bin/env python3
"""Euler-Berry spin gate v2.4.

Auxiliary sanity check only. The proof in the report is formal/symbolic.
The script enumerates candidate spin sectors and tests the stated closure rule:
- hemisphere Berry loop has non-trivial projective sign,
- doubled loop closes to identity,
- choose the minimal positive sector.
"""
from __future__ import annotations

import cmath
import csv
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

TOL = 1e-9

def close(a: complex, b: complex, tol: float = TOL) -> bool:
    return abs(a - b) < tol

# Candidate spin sectors up to 4 in half-integer steps.
candidates = [Fraction(n, 2) for n in range(0, 9)]
rows = []
selected = None
for s in candidates:
    # Hemisphere solid angle = 2*pi, Berry phase = s * 2*pi.
    hemisphere_phase = 2 * math.pi * float(s)
    doubled_phase = 2 * hemisphere_phase
    hemisphere_holonomy = cmath.exp(1j * hemisphere_phase)
    doubled_holonomy = cmath.exp(1j * doubled_phase)
    nontrivial_sign = close(hemisphere_holonomy, -1 + 0j)
    doubled_identity = close(doubled_holonomy, 1 + 0j)
    passes = bool(s > 0 and nontrivial_sign and doubled_identity)
    if selected is None and passes:
        selected = s
    rows.append({
        "spin_s": str(s),
        "hemisphere_phase_over_pi": float(hemisphere_phase / math.pi),
        "hemisphere_holonomy_real": round(hemisphere_holonomy.real, 12),
        "hemisphere_holonomy_imag": round(hemisphere_holonomy.imag, 12),
        "nontrivial_projective_sign": nontrivial_sign,
        "doubled_loop_identity": doubled_identity,
        "passes_gate": passes,
    })

summary = {
    "gate_type": "COMPUTATIONAL_SANITY_CHECK",
    "central_proof_type": "FORMAL_SYMBOLIC_PASS",
    "selected_minimal_spin": str(selected),
    "expected_selected_minimal_spin": "1/2",
    "pass": str(selected) == "1/2",
    "mass_inputs_used": False,
}

with (RESULTS / "euler_berry_spin_candidates_v2_4.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

with (RESULTS / "euler_berry_spin_gate_summary_v2_4.json").open("w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

if not summary["pass"]:
    raise SystemExit("Euler-Berry spin gate sanity check failed")

print(json.dumps(summary, indent=2))
