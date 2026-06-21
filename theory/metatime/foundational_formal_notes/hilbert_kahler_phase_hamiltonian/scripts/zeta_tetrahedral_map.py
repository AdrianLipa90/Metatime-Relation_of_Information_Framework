#!/usr/bin/env python3
"""Tetrahedral depth map with zeta-zero pole labels as a model axiom."""
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

# First four imaginary parts of nontrivial zeta zeros, used as spectral labels.
# These are labels in this model, not a derivation from standard CP^1 geometry.
ZETA_GAMMA = [14.134725141, 21.022039639, 25.010857580, 30.424876126]


def tetra_vertices():
    verts = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
    ], dtype=float)
    return verts / np.linalg.norm(verts, axis=1)[:, None]


def sic_probs(n, verts):
    # Tetrahedral qubit SIC coordinates. Sum_j p_j = 1.
    return np.array([(1.0 + float(np.dot(n, v))) / 4.0 for v in verts])


def main():
    verts = tetra_vertices()
    gram = [[float(np.dot(verts[i], verts[j])) for j in range(4)] for i in range(4)]
    north = np.array([0.0, 0.0, 1.0])
    south = np.array([0.0, 0.0, -1.0])
    data = {
        "zeta_pole_axiom": {
            "north_pole_label": "1/2 + i gamma_1",
            "south_pole_label": "1/2 - i gamma_1",
            "gamma_1": ZETA_GAMMA[0],
        },
        "tetrahedral_vertices": verts.tolist(),
        "dot_product_matrix": gram,
        "sic_probabilities_north": sic_probs(north, verts).tolist(),
        "sic_probabilities_south": sic_probs(south, verts).tolist(),
        "zeta_labels_for_vertices": [f"1/2 + i*{g}" for g in ZETA_GAMMA],
    }
    (OUT / "zeta_tetrahedral_map.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    # Spherical projection figure.
    fig = plt.figure(figsize=(5.2, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(x, y, z, linewidth=0.25, alpha=0.35)
    ax.scatter(verts[:,0], verts[:,1], verts[:,2], s=35)
    for i, p in enumerate(verts):
        ax.text(p[0], p[1], p[2], f"T{i+1}")
    ax.scatter([0,0],[0,0],[1,-1], s=45)
    ax.text(0,0,1.1,"N: zeta zero")
    ax.text(0,0,-1.15,"S: conjugate")
    ax.set_title("Zeta-labelled poles and tetrahedral depth frame")
    ax.set_box_aspect((1,1,1))
    plt.tight_layout()
    plt.savefig(FIG / "zeta_tetrahedral_frame.pdf")
    plt.close()

if __name__ == "__main__":
    main()
