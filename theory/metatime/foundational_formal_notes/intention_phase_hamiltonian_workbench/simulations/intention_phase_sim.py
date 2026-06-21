#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toy simulation for the relational intention-phase Hamiltonian.

Purpose:
- encode twin-prime seeds;
- generate Collatz/Kolac rhythm;
- build an information/intention operator I = kappa W + zero-level fluctuations;
- evolve a finite-dimensional state by a Floquet phase unitary;
- add AB/Berry/Euler holonomy as a geometric phase channel;
- emit figures and a JSON summary.

This is a formal toy model, not an empirical physical validation.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Tuple, Dict, Any

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    plt = None

KAPPA = math.log(2.0) / (24.0 * math.pi)
HBAR = 1.0


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    r = int(math.isqrt(n))
    for d in range(3, r + 1, 2):
        if n % d == 0:
            return False
    return True


def twin_primes_up_to(limit: int) -> List[Tuple[int, int]]:
    return [(p, p + 2) for p in range(2, limit + 1) if is_prime(p) and is_prime(p + 2)]


def collatz(n: int) -> int:
    if n <= 0:
        raise ValueError("Collatz seed must be positive.")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def collatz_orbit(n: int, steps: int) -> List[int]:
    out = [n]
    for _ in range(steps - 1):
        out.append(collatz(out[-1]))
    return out


def pair_orbit(seed: Tuple[int, int], steps: int) -> List[Tuple[int, int]]:
    a = collatz_orbit(seed[0], steps)
    b = collatz_orbit(seed[1], steps)
    return list(zip(a, b))


def rhythm_from_pair(pair: Tuple[int, int], mode: str = "log_parity") -> float:
    a, b = pair
    if mode == "log":
        return 0.5 * (math.log1p(a) + math.log1p(b))
    if mode == "parity":
        return 0.5 * ((1.0 if a % 2 else -1.0) + (1.0 if b % 2 else -1.0))
    if mode == "log_parity":
        parity = 0.5 * ((1.0 if a % 2 else -1.0) + (1.0 if b % 2 else -1.0))
        scale = 0.5 * (math.log1p(a) + math.log1p(b))
        return scale * (1.0 + 0.25 * parity)
    raise ValueError(f"Unknown rhythm mode: {mode}")


def normalize_rhythm(raw: Iterable[float]) -> np.ndarray:
    arr = np.asarray(list(raw), dtype=float)
    mean_abs = float(np.mean(np.abs(arr))) if len(arr) else 1.0
    if mean_abs == 0.0:
        return arr
    return arr / mean_abs


def hermitian_noise(dim: int, amplitude: float, rng: np.random.Generator) -> np.ndarray:
    real = rng.normal(size=(dim, dim))
    imag = rng.normal(size=(dim, dim))
    a = real + 1j * imag
    h = 0.5 * (a + a.conj().T)
    norm = float(np.linalg.norm(h, ord=2))
    if norm == 0.0:
        return h
    return amplitude * h / norm


def unitary_from_hermitian(h: np.ndarray, phase_scale: float) -> np.ndarray:
    # Exponentiate Hermitian matrix through spectral theorem.
    vals, vecs = np.linalg.eigh(h)
    return vecs @ np.diag(np.exp(-1j * phase_scale * vals)) @ vecs.conj().T


def abe_phase(flux_fraction: float, berry_theta: float, euler_characteristic: int, spin: float = 0.5) -> float:
    # AB phase for flux_fraction in units of flux quantum: 2*pi*Phi/Phi0.
    phi_ab = 2.0 * math.pi * flux_fraction
    # Berry phase for spin-1/2 adiabatic loop at cone angle theta: -Omega/2, Omega=2*pi*(1-cos theta).
    phi_berry = -spin * 2.0 * math.pi * (1.0 - math.cos(berry_theta))
    # Euler/spin connection toy closure: 2*pi*s*chi. For spin=1/2 gives pi*chi.
    phi_euler = 2.0 * math.pi * spin * euler_characteristic
    return phi_ab + phi_berry + phi_euler


@dataclass
class SimulationResult:
    seed: Tuple[int, int]
    steps: int
    kappa: float
    rhythm_mode: str
    final_phase_angle: float
    final_norm: float
    max_unitarity_error: float
    abe_phase: float
    total_phase_last: float


def run_single(seed: Tuple[int, int], steps: int, dim: int, fluctuation: float, mode: str, rng_seed: int) -> Dict[str, Any]:
    rng = np.random.default_rng(rng_seed)
    orbit = pair_orbit(seed, steps)
    rhythm = normalize_rhythm(rhythm_from_pair(pair, mode=mode) for pair in orbit)

    # Winding / information charge operator. Zero-trace half-integer ladder.
    charges = np.linspace(-(dim - 1) / 2.0, (dim - 1) / 2.0, dim)
    W = np.diag(charges)

    psi = np.zeros(dim, dtype=complex)
    psi[0] = 1.0
    phases = []
    norms = []
    unitarity_errors = []

    phi_abe = abe_phase(flux_fraction=0.25, berry_theta=math.pi / 3.0, euler_characteristic=2, spin=0.5)
    global_abe = np.exp(1j * phi_abe)

    U_total = np.eye(dim, dtype=complex)
    for k, rho in enumerate(rhythm):
        noise = hermitian_noise(dim, fluctuation, rng)
        I = KAPPA * W + noise
        U = unitary_from_hermitian(I, phase_scale=float(rho))
        err = float(np.linalg.norm(U.conj().T @ U - np.eye(dim), ord=2))
        unitarity_errors.append(err)
        psi = global_abe * (U @ psi)
        U_total = global_abe * U @ U_total
        phases.append(float(np.angle(np.vdot(np.eye(dim)[0], psi))))
        norms.append(float(np.linalg.norm(psi)))

    result = SimulationResult(
        seed=seed,
        steps=steps,
        kappa=KAPPA,
        rhythm_mode=mode,
        final_phase_angle=float(phases[-1]),
        final_norm=float(norms[-1]),
        max_unitarity_error=float(max(unitarity_errors)),
        abe_phase=float(phi_abe),
        total_phase_last=float(np.angle(np.linalg.det(U_total))),
    )
    return {
        "result": asdict(result),
        "orbit": orbit,
        "rhythm": rhythm.tolist(),
        "phases": phases,
        "norms": norms,
        "unitarity_errors": unitarity_errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("../data/simulation_summary.json"))
    parser.add_argument("--fig-dir", type=Path, default=Path("../figures"))
    parser.add_argument("--steps", type=int, default=64)
    parser.add_argument("--dim", type=int, default=4)
    parser.add_argument("--fluctuation", type=float, default=0.05)
    parser.add_argument("--limit", type=int, default=80)
    args = parser.parse_args()

    seeds = twin_primes_up_to(args.limit)[:8]
    summaries = []
    traces = {}
    for idx, seed in enumerate(seeds):
        data = run_single(seed, args.steps, args.dim, args.fluctuation, "log_parity", 1000 + idx)
        summaries.append(data["result"])
        traces[str(seed)] = data

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.fig_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "toy_model_only_not_empirical_validation",
        "kappa_ln2_over_24pi": KAPPA,
        "seeds": seeds,
        "summaries": summaries,
        "traces": traces,
    }
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if plt is not None:
        # Figure 1: phase traces for first three seeds.
        plt.figure(figsize=(8, 4.8))
        for seed in seeds[:3]:
            trace = traces[str(seed)]["phases"]
            plt.plot(range(len(trace)), trace, marker="o", markersize=2, linewidth=1, label=str(seed))
        plt.xlabel("Collatz step k")
        plt.ylabel("phase angle arg(<0|psi_k>) [rad]")
        plt.title("Intention-phase Floquet trace for twin-prime seeds")
        plt.legend()
        plt.tight_layout()
        plt.savefig(args.fig_dir / "phase_trace.pdf")
        plt.savefig(args.fig_dir / "phase_trace.png", dpi=180)
        plt.close()

        # Figure 2: unitarity error scan.
        plt.figure(figsize=(8, 4.8))
        labels = [str(s["seed"]) for s in summaries]
        errors = [s["max_unitarity_error"] for s in summaries]
        plt.bar(range(len(labels)), errors)
        plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
        plt.ylabel("max ||U*U-I||_2")
        plt.title("Numerical unitarity diagnostic")
        plt.tight_layout()
        plt.savefig(args.fig_dir / "unitarity_scan.pdf")
        plt.savefig(args.fig_dir / "unitarity_scan.png", dpi=180)
        plt.close()

        # Figure 3: final phase angle by seed.
        plt.figure(figsize=(8, 4.8))
        angles = [s["final_phase_angle"] for s in summaries]
        plt.plot(range(len(labels)), angles, marker="o")
        plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
        plt.ylabel("final phase angle [rad]")
        plt.title("Final phase by twin-prime seed")
        plt.tight_layout()
        plt.savefig(args.fig_dir / "seed_final_phase.pdf")
        plt.savefig(args.fig_dir / "seed_final_phase.png", dpi=180)
        plt.close()


if __name__ == "__main__":
    main()
