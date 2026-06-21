#!/usr/bin/env python3
"""
Collatz-Poincare phase workbench for the phase-intention Hamiltonian.
This is a structural simulation, not a physical proof.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "results"
FIG = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

KAPPA = math.log(2.0) / (24.0 * math.pi)


def collatz(n: int) -> int:
    return n // 2 if n % 2 == 0 else 3 * n + 1


def twin_collatz(seed=(11, 13), steps=80):
    a, b = seed
    seq = []
    for k in range(steps):
        seq.append((k, a, b))
        a, b = collatz(a), collatz(b)
    return seq


def rhythm(a: int, b: int) -> float:
    # Bounded positive rhythm extracted from the twin Collatz pair.
    # The log prevents large odd jumps from dominating the phase.
    return (math.log1p(a) + math.log1p(b)) / (1.0 + math.log1p(a + b))


def disk_step(z: complex, rho: float, k: int) -> complex:
    # A Poincare disk automorphism z -> exp(i alpha) (z + beta)/(1+conj(beta)z).
    alpha = (KAPPA * rho * (1 + (k % 7))) % (2 * math.pi)
    beta_abs = min(0.35, 0.04 + 0.015 * rho)
    beta = beta_abs * complex(math.cos(alpha / 2), math.sin(alpha / 2))
    return complex(math.cos(alpha), math.sin(alpha)) * (z + beta) / (1 + beta.conjugate() * z)


def main(seed=(11, 13), steps=80, phi_abe=1.75, d_lambda=0.12, eps_nu=0.031):
    seq = twin_collatz(seed, steps)
    z = 0.0 + 0.0j
    rows = []
    theta_i = 0.0
    for k, a, b in seq:
        rho = rhythm(a, b)
        # A simple winding observable W_s(k); replace with canonical W_s in later work.
        w = ((a - b) % 12) / 12.0 + 0.5
        delta_i0 = 0.07 * KAPPA * math.sin(2 * math.pi * k / 17.0)
        theta_i += rho * (KAPPA * w + delta_i0)
        z = disk_step(z, rho, k)
        phi_total = phi_abe + theta_i
        closure = phi_total - 2 * math.pi * (d_lambda + eps_nu)
        branch = round(closure / (2 * math.pi))
        defect = closure / (2 * math.pi) - branch
        rows.append({
            "k": k, "a": a, "b": b, "rho": rho, "W": w,
            "theta_I": theta_i, "disk_re": z.real, "disk_im": z.imag,
            "phi_total": phi_total, "closure_branch": branch, "closure_defect": defect,
        })

    (OUT / "collatz_poincare_phase.json").write_text(json.dumps({
        "seed": seed,
        "kappa": KAPPA,
        "phi_ABE": phi_abe,
        "D_Lambda": d_lambda,
        "epsilon_nu": eps_nu,
        "rows": rows,
    }, indent=2), encoding="utf-8")

    # Figure 1: disk trajectory.
    xs = [r["disk_re"] for r in rows]
    ys = [r["disk_im"] for r in rows]
    t = np.linspace(0, 2 * np.pi, 400)
    plt.figure(figsize=(5.2, 5.2))
    plt.plot(np.cos(t), np.sin(t), linewidth=1)
    plt.plot(xs, ys, marker="o", markersize=2, linewidth=1)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("Re z")
    plt.ylabel("Im z")
    plt.title("Collatz-driven trajectory on the Poincare disk")
    plt.tight_layout()
    plt.savefig(FIG / "poincare_collatz_trajectory.pdf")
    plt.close()

    # Figure 2: closure defect.
    plt.figure(figsize=(6.5, 3.4))
    plt.plot([r["k"] for r in rows], [r["closure_defect"] for r in rows], linewidth=1.4)
    plt.axhline(0.0, linewidth=0.8)
    plt.xlabel("Collatz step k")
    plt.ylabel("phase closure defect")
    plt.title("Euler-Berry-Lambda-neutrino closure defect")
    plt.tight_layout()
    plt.savefig(FIG / "closure_defect.pdf")
    plt.close()

    # Figure 3: rhythm.
    plt.figure(figsize=(6.5, 3.4))
    plt.plot([r["k"] for r in rows], [r["rho"] for r in rows], linewidth=1.4)
    plt.xlabel("Collatz step k")
    plt.ylabel("rho_s(k)")
    plt.title("Twin-prime Collatz rhythm")
    plt.tight_layout()
    plt.savefig(FIG / "collatz_rhythm.pdf")
    plt.close()


if __name__ == "__main__":
    main()
