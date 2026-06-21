#!/usr/bin/env python3
"""Finite-dimensional Hermiticity/unitarity check for the phase Hamiltonian."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

KAPPA_I = math.log(2.0) / (24.0 * math.pi)


def build_hamiltonian(n: int, rho: float, delta_tau: float, flux_phase: float) -> np.ndarray:
    # Rotor sectors m = -M,...,+M.
    m = np.arange(-(n // 2), n // 2 + 1, dtype=float)
    n = len(m)
    J = np.diag(m)
    W = np.diag(np.tanh(m / max(1.0, n / 4.0)))
    # A simple Hermitian nearest-neighbor shape coupling with a holonomy phase.
    T = np.zeros((n, n), dtype=complex)
    for i in range(n - 1):
        T[i, i + 1] = np.exp(1j * flux_phase)
        T[i + 1, i] = np.exp(-1j * flux_phase)
    H_phase = (rho / delta_tau) * KAPPA_I * W
    H_shape = 0.12 * (J @ J) + 0.05 * T
    return H_phase + H_shape


def unitary_from_hermitian(H: np.ndarray, dt: float) -> np.ndarray:
    eigvals, eigvecs = np.linalg.eigh(H)
    return eigvecs @ np.diag(np.exp(-1j * eigvals * dt)) @ eigvecs.conj().T


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=17)
    parser.add_argument("--rho", type=float, default=1.13)
    parser.add_argument("--delta-tau", type=float, default=1.0)
    parser.add_argument("--flux-phase", type=float, default=0.48)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--out-dir", type=Path, default=Path("results"))
    parser.add_argument("--fig-dir", type=Path, default=Path("figures"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.fig_dir.mkdir(parents=True, exist_ok=True)

    H = build_hamiltonian(args.n, args.rho, args.delta_tau, args.flux_phase)
    hermiticity_error = float(np.linalg.norm(H - H.conj().T))
    U = unitary_from_hermitian(H, dt=0.1)
    unitarity_error = float(np.linalg.norm(U.conj().T @ U - np.eye(U.shape[0])))

    psi = np.zeros(H.shape[0], dtype=complex)
    psi[H.shape[0] // 2] = 1.0
    norms = []
    energies = []
    for _ in range(args.steps):
        norms.append(float(np.linalg.norm(psi)))
        energies.append(float(np.real(psi.conj().T @ H @ psi)))
        psi = U @ psi

    summary = {
        "dimension": int(H.shape[0]),
        "kappa_I": KAPPA_I,
        "hermiticity_error": hermiticity_error,
        "unitarity_error": unitarity_error,
        "initial_energy": energies[0],
        "final_energy": energies[-1],
        "max_norm_error": max(abs(x - 1.0) for x in norms),
    }
    (args.out_dir / "hamiltonian_matrix_result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    plt.figure(figsize=(7.2, 4.2))
    plt.plot(range(len(norms)), norms, linewidth=1.4)
    plt.xlabel("evolution step")
    plt.ylabel("state norm")
    plt.title("Unitary norm check")
    plt.tight_layout()
    plt.savefig(args.fig_dir / "unitary_norm_check.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.2, 4.2))
    plt.plot(range(len(energies)), energies, linewidth=1.4)
    plt.xlabel("evolution step")
    plt.ylabel("energy expectation")
    plt.title("Energy expectation under a time-independent reference H")
    plt.tight_layout()
    plt.savefig(args.fig_dir / "energy_expectation_demo.png", dpi=180)
    plt.close()

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
