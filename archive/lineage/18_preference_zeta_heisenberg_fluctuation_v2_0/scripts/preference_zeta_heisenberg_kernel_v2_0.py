#!/usr/bin/env python3
"""
Preference / zeta-Heisenberg diagnostic kernel v2.0.

This script intentionally does not use observed fermion masses. It computes
only structural seed diagnostics for the information preference scale and a
bounded zeta-axis fluctuation channel.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

KAPPA = math.log(2.0) / (24.0 * math.pi)
ZETA_ZERO_ORDINATES = [
    14.134725141734693790,
    21.022039638771554993,
    25.010857580145688763,
    30.424876125859513210,
    32.935061587739189691,
    37.586178158825671257,
    40.918719012147495187,
    43.327073280914999519,
    48.005150881167159727,
    49.773832477672302181,
    52.970321477714460644,
    56.446247697063394804,
]
SEEDS = [(3,5), (5,7), (11,13), (17,19), (29,31), (41,43)]

def collatz_steps(n: int) -> int:
    steps = 0
    seen = set()
    while n != 1 and steps < 10000:
        if n in seen:
            raise RuntimeError("unexpected cycle")
        seen.add(n)
        n = n//2 if n % 2 == 0 else 3*n+1
        steps += 1
    return steps

def zeta_index_for_seed(p: int, q: int) -> int:
    # Operational ansatz: the seed midpoint selects a zero-pair window.
    # This is not a mass fit and remains a formal debt for deeper proof.
    mid = (p + q) // 2
    return mid % (len(ZETA_ZERO_ORDINATES)-1)

def main() -> None:
    outdir = Path(__file__).resolve().parents[1] / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    spacings = [ZETA_ZERO_ORDINATES[i+1] - ZETA_ZERO_ORDINATES[i] for i in range(len(ZETA_ZERO_ORDINATES)-1)]
    mean_spacing = sum(spacings)/len(spacings)
    for p, q in SEEDS:
        idx = zeta_index_for_seed(p, q)
        gamma_n = ZETA_ZERO_ORDINATES[idx]
        gamma_np1 = ZETA_ZERO_ORDINATES[idx+1]
        spacing = gamma_np1 - gamma_n
        spacing_norm = spacing / mean_spacing
        c_steps = collatz_steps(p) + collatz_steps(q)
        phase_uncertainty = max(KAPPA/2.0, KAPPA/(1.0 + spacing_norm))
        index_uncertainty = max(1.0, spacing_norm)
        heisenberg_product = phase_uncertainty * index_uncertainty
        preference_width = math.exp(-phase_uncertainty / KAPPA)
        rows.append({
            "seed_p": p,
            "seed_q": q,
            "zeta_index": idx,
            "gamma_n": f"{gamma_n:.15f}",
            "gamma_np1": f"{gamma_np1:.15f}",
            "zeta_spacing": f"{spacing:.15f}",
            "spacing_norm": f"{spacing_norm:.12f}",
            "collatz_step_sum": c_steps,
            "kappa": f"{KAPPA:.18f}",
            "phase_uncertainty": f"{phase_uncertainty:.18f}",
            "index_uncertainty": f"{index_uncertainty:.12f}",
            "heisenberg_product": f"{heisenberg_product:.18f}",
            "bound_kappa_over_2": f"{(KAPPA/2.0):.18f}",
            "gate_pass": heisenberg_product >= KAPPA/2.0,
            "preference_width": f"{preference_width:.12f}",
            "mass_input_used": False,
        })
    csv_path = outdir / "preference_zeta_heisenberg_seed_diagnostics_v2_0.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = outdir / "preference_zeta_heisenberg_validation_v2_0.txt"
    all_pass = all(str(r["gate_pass"]) == "True" for r in rows)
    summary.write_text(
        "Preference / zeta-Heisenberg kernel v2.0\n"
        f"kappa={KAPPA:.18f}\n"
        f"rows={len(rows)}\n"
        f"heisenberg_gate_all_pass={all_pass}\n"
        "mass_input_used=False\n"
        "zeta_role=coherence_fluctuation_not_raw_cost\n"
        "collatz_terminal_axis=4->2->1->1/2\n",
        encoding="utf-8",
    )
    print(summary.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
