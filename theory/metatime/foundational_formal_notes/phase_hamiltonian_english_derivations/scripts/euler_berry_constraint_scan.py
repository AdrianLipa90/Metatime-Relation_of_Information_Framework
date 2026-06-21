#!/usr/bin/env python3
"""Scan Euler-Berry phase closure defects across a small parameter grid."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt


def closure_defect(phi_ab: float, phi_b: float, chi_euler: float, theta_i: float, spin: float = 0.5) -> dict:
    # Gauss-Bonnet convention: integral curvature contribution = 2*pi*chi.
    # Spin contribution uses spin * 2*pi*chi.
    phi_e = spin * 2.0 * math.pi * chi_euler
    total = phi_ab + phi_b + phi_e + theta_i
    D = round(total / (2.0 * math.pi))
    epsilon = total / (2.0 * math.pi) - D
    return {"phi_euler": phi_e, "total_phase": total, "D": D, "epsilon": epsilon}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("results"))
    parser.add_argument("--fig-dir", type=Path, default=Path("figures"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.fig_dir.mkdir(parents=True, exist_ok=True)

    phi_ab = 0.31
    theta_i = 0.42
    berry_values = [(-math.pi + 2.0 * math.pi * i / 120.0) for i in range(121)]
    chi_values = [-2, -1, 0, 1, 2]
    records = []
    for chi in chi_values:
        for phi_b in berry_values:
            rec = closure_defect(phi_ab=phi_ab, phi_b=phi_b, chi_euler=chi, theta_i=theta_i)
            rec.update({"phi_ab": phi_ab, "phi_berry": phi_b, "chi_euler": chi, "theta_i": theta_i})
            records.append(rec)

    (args.out_dir / "euler_berry_scan.json").write_text(json.dumps(records, indent=2), encoding="utf-8")

    plt.figure(figsize=(7.2, 4.2))
    for chi in chi_values:
        xs = [r["phi_berry"] for r in records if r["chi_euler"] == chi]
        ys = [abs(r["epsilon"]) for r in records if r["chi_euler"] == chi]
        plt.plot(xs, ys, linewidth=1.2, label=f"chi={chi}")
    plt.xlabel("Berry phase phi_B")
    plt.ylabel("absolute closure defect |epsilon|")
    plt.title("Euler-Berry closure defect scan")
    plt.legend(loc="best", fontsize=8)
    plt.tight_layout()
    plt.savefig(args.fig_dir / "euler_berry_constraint_scan.png", dpi=180)
    plt.close()

    best = min(records, key=lambda r: abs(r["epsilon"]))
    print(json.dumps({"best_closure": best}, indent=2))


if __name__ == "__main__":
    main()
