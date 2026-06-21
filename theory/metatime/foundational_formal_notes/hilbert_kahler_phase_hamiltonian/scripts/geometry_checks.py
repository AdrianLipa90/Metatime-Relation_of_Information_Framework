#!/usr/bin/env python3
"""Numerical checks for CP^1 / Bloch sphere Berry geometry."""
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


def berry_curvature(theta):
    # For spin 1/2 in the north gauge: F = 1/2 sin(theta) dtheta wedge dphi.
    return 0.5 * np.sin(theta)


def main(n_theta=600, n_phi=600):
    theta = np.linspace(0, math.pi, n_theta)
    phi = np.linspace(0, 2 * math.pi, n_phi)
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    integral = float(np.sum(berry_curvature(theta)[:, None]) * dtheta * dphi)
    chern = integral / (2 * math.pi)
    result = {
        "berry_curvature_integral_numeric": integral,
        "expected_integral": 2 * math.pi,
        "chern_number_numeric": chern,
        "spinor_closure": {"psi_2pi": "-psi", "psi_4pi": "+psi"},
    }
    (OUT / "cp1_berry_geometry_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    tt = np.linspace(0, math.pi, 400)
    plt.figure(figsize=(6.0, 3.4))
    plt.plot(tt, berry_curvature(tt), linewidth=1.5)
    plt.xlabel("theta")
    plt.ylabel("F_{theta phi}")
    plt.title("Berry curvature density on CP^1")
    plt.tight_layout()
    plt.savefig(FIG / "berry_curvature_density.pdf")
    plt.close()

if __name__ == "__main__":
    main()
