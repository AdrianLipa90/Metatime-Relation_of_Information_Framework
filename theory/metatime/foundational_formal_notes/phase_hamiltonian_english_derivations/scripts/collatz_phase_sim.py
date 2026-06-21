#!/usr/bin/env python3
"""
Reference simulation for the intention-phase Hamiltonian scaffold.

This is not an experimental proof. It is a finite numerical model used to
check the internal consistency of the proposed formal structure:

twin-prime seed -> Collatz rhythm -> information/intention phase ->
Euler-Berry closure defect.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt

KAPPA_I = math.log(2.0) / (24.0 * math.pi)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def collatz(n: int) -> int:
    return n // 2 if n % 2 == 0 else 3 * n + 1


def orbit(n0: int, steps: int) -> List[int]:
    values = [n0]
    n = n0
    for _ in range(steps):
        n = collatz(n)
        values.append(n)
    return values


def bounded_collatz_rhythm(values: List[int], eta: float = 0.35) -> List[float]:
    """A bounded positive rhythm extracted from a Collatz orbit.

    The exact rhythm map is a model choice. The formal requirement is only
    rho_s(k) > 0. This reference choice uses parity and logarithmic scale so
    that very large Collatz excursions do not dominate the phase numerically.
    """
    logs = [math.log1p(v) for v in values]
    mean = sum(logs) / len(logs)
    var = sum((x - mean) ** 2 for x in logs) / max(1, len(logs) - 1)
    std = math.sqrt(var) if var > 0 else 1.0
    rho = []
    for n, x in zip(values[:-1], logs[:-1]):
        parity = 1.0 if n % 2 else -1.0
        z = math.tanh((x - mean) / std)
        rho.append(1.0 + eta * parity * (0.5 + 0.5 * z))
    return rho


def winding_signal(values: List[int]) -> List[float]:
    """A simple winding channel W_s(k).

    In a full theory W_s is an operator. For the reference scalar simulation
    it is represented by a bounded number derived from the Collatz orbital.
    """
    return [math.atan(math.log1p(n)) / math.pi for n in values[:-1]]


@dataclass
class CollatzPhaseResult:
    twin_prime_seed: Tuple[int, int]
    scalar_seed: int
    steps: int
    kappa_I: float
    eta: float
    theta_intention: float
    phase_ab: float
    phase_berry: float
    phase_euler: float
    total_phase: float
    closest_D: int
    epsilon: float
    unitary_modulus_error: float


def run(seed_p: int, steps: int, eta: float, phase_ab: float, phase_berry: float, phase_euler: float) -> CollatzPhaseResult:
    if not (is_prime(seed_p) and is_prime(seed_p + 2)):
        raise ValueError(f"{seed_p} and {seed_p + 2} are not a twin-prime seed")
    n0 = seed_p * (seed_p + 2)
    values = orbit(n0, steps)
    rho = bounded_collatz_rhythm(values, eta=eta)
    W = winding_signal(values)
    increments = [r * KAPPA_I * w for r, w in zip(rho, W)]
    theta_I = sum(increments)
    total = theta_I + phase_ab + phase_berry + phase_euler
    closest_D = round(total / (2.0 * math.pi))
    epsilon = total / (2.0 * math.pi) - closest_D
    U = complex(math.cos(total), math.sin(total))
    unitary_modulus_error = abs(abs(U) - 1.0)
    return CollatzPhaseResult(
        twin_prime_seed=(seed_p, seed_p + 2),
        scalar_seed=n0,
        steps=steps,
        kappa_I=KAPPA_I,
        eta=eta,
        theta_intention=theta_I,
        phase_ab=phase_ab,
        phase_berry=phase_berry,
        phase_euler=phase_euler,
        total_phase=total,
        closest_D=closest_D,
        epsilon=epsilon,
        unitary_modulus_error=unitary_modulus_error,
    )


def make_figures(seed_p: int, steps: int, eta: float, out_dir: Path) -> None:
    n0 = seed_p * (seed_p + 2)
    values = orbit(n0, steps)
    rho = bounded_collatz_rhythm(values, eta=eta)
    W = winding_signal(values)
    increments = [r * KAPPA_I * w for r, w in zip(rho, W)]
    cumulative = []
    acc = 0.0
    for x in increments:
        acc += x
        cumulative.append(acc)

    out_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7.2, 4.2))
    plt.plot(range(len(values)), values, marker="o", markersize=2, linewidth=1)
    plt.yscale("log")
    plt.xlabel("Collatz step k")
    plt.ylabel("n_k (log scale)")
    plt.title("Collatz orbit from twin-prime scalar seed")
    plt.tight_layout()
    plt.savefig(out_dir / "collatz_orbit.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.2, 4.2))
    plt.plot(range(len(rho)), rho, linewidth=1.4)
    plt.xlabel("Collatz step k")
    plt.ylabel("rho_s(k)")
    plt.title("Bounded Collatz rhythm")
    plt.tight_layout()
    plt.savefig(out_dir / "collatz_rhythm.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.2, 4.2))
    plt.plot(range(len(cumulative)), cumulative, linewidth=1.4)
    plt.xlabel("Collatz step k")
    plt.ylabel("cumulative theta_I")
    plt.title("Accumulated intention/information phase")
    plt.tight_layout()
    plt.savefig(out_dir / "intention_phase_accumulation.png", dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-p", type=int, default=17)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--eta", type=float, default=0.35)
    parser.add_argument("--phase-ab", type=float, default=0.31)
    parser.add_argument("--phase-berry", type=float, default=0.73)
    parser.add_argument("--phase-euler", type=float, default=math.pi)
    parser.add_argument("--out-dir", type=Path, default=Path("results"))
    parser.add_argument("--fig-dir", type=Path, default=Path("figures"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    result = run(args.seed_p, args.steps, args.eta, args.phase_ab, args.phase_berry, args.phase_euler)
    (args.out_dir / "collatz_phase_result.json").write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
    make_figures(args.seed_p, args.steps, args.eta, args.fig_dir)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
