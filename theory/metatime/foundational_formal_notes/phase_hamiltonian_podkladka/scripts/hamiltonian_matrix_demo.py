#!/usr/bin/env python3
"""
Finite-dimensional consistency demo for the phase-first Hamiltonian.

The demo constructs a Hermitian Information/Intention operator, a simple
covariant kinetic term, and a time-step unitary. It checks Hermiticity and
norm conservation. This is a structural test, not a physical validation.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

KAPPA = math.log(2.0) / (24.0 * math.pi)


def hermitian_random(n: int, rng: np.random.Generator) -> np.ndarray:
    a = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    return 0.5 * (a + a.conj().T)


def unitary_from_hermitian(H: np.ndarray, dt: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(H)
    return vecs @ np.diag(np.exp(-1j * dt * vals)) @ vecs.conj().T


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dim", type=int, default=8)
    ap.add_argument("--steps", type=int, default=60)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=Path, default=Path("results/hamiltonian_matrix_results.json"))
    ap.add_argument("--figdir", type=Path, default=Path("figures"))
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    n = args.dim
    W = hermitian_random(n, rng)
    V0 = hermitian_random(n, rng)
    A = hermitian_random(n, rng) * 0.05
    P = np.diag(np.linspace(-1.0, 1.0, n))

    # Covariant kinetic proxy: Pi = P - A, H_perp = 0.5 Pi^2.
    Pi = P - A
    H_perp = 0.5 * (Pi @ Pi)

    # Phase/free part: kappa*W + small zero fluctuation channel.
    psi = rng.normal(size=n) + 1j * rng.normal(size=n)
    psi = psi / np.linalg.norm(psi)

    norms = []
    herm_errors = []
    energies = []
    dt = 0.08
    for k in range(args.steps):
        rho = 1.0 + 0.25 * math.sin(2.0 * math.pi * k / 7.0)
        fluct = 0.07 * math.cos(2.0 * math.pi * k / 11.0) * V0
        H_free = rho * (KAPPA * W + fluct)
        H = H_free + H_perp
        herm_errors.append(float(np.linalg.norm(H - H.conj().T)))
        energies.append(float(np.real(np.vdot(psi, H @ psi))))
        U = unitary_from_hermitian(H, dt)
        psi = U @ psi
        norms.append(float(np.linalg.norm(psi)))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.figdir.mkdir(parents=True, exist_ok=True)
    result = {
        "dim": n,
        "steps": args.steps,
        "kappa_ln2_over_24pi": KAPPA,
        "max_hermiticity_error": max(herm_errors),
        "max_norm_deviation": max(abs(x - 1.0) for x in norms),
        "energy_expectation_first": energies[0],
        "energy_expectation_last": energies[-1],
    }
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    plt.figure(figsize=(7, 4))
    plt.plot(range(args.steps), norms)
    plt.xlabel("step k")
    plt.ylabel("state norm")
    plt.title("Unitary norm check for phase-first Hamiltonian")
    plt.tight_layout()
    plt.savefig(args.figdir / "unitary_norm_check.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.plot(range(args.steps), energies)
    plt.xlabel("step k")
    plt.ylabel("energy expectation")
    plt.title("Energy expectation under time-dependent phase generator")
    plt.tight_layout()
    plt.savefig(args.figdir / "energy_expectation_demo.png", dpi=180)
    plt.close()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
