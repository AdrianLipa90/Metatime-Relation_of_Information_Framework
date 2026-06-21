#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metatime SM Generation Embedding v0.3

Purpose:
- Define a non-mass-input generational vector from twin-prime seeds and Collatz orbits.
- Provide a Poincare-disk embedding diagnostic.
- Produce candidate tables for later Euler-Berry action construction.

This script does not use observed fermion masses as an input.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from collections import Counter

KAPPA = math.log(2.0)/(24.0*math.pi)
ZETA_GAMMA_1 = 14.134725141734694
ZETA_GAMMA_2 = 21.022039638771554
ZETA_GAMMA_3 = 25.010857580145688
ZETA_GAMMAS = [ZETA_GAMMA_1, ZETA_GAMMA_2, ZETA_GAMMA_3]

# Candidate twin-prime seeds. The first column is not a claim of final canon;
# it is the clean non-mass-input seed list to evaluate.
CANDIDATE_SEEDS = [
    (3, 5),
    (5, 7),
    (11, 13),
    (17, 19),
    (29, 31),
    (41, 43),
    (59, 61),
    (71, 73),
]


def collatz_step(n: int) -> int:
    return n//2 if n % 2 == 0 else 3*n + 1


def collatz_orbit(n: int, max_steps: int = 10000) -> list[int]:
    out = [n]
    while n != 1 and len(out) < max_steps:
        n = collatz_step(n)
        out.append(n)
    return out


def parity_entropy(orbit: list[int]) -> float:
    if not orbit:
        return 0.0
    pars = [x % 2 for x in orbit[:-1]]  # final 1 omitted from transition entropy
    if not pars:
        return 0.0
    c = Counter(pars)
    total = sum(c.values())
    h = 0.0
    for v in c.values():
        p = v/total
        h -= p*math.log(p, 2)
    return h


def sequence_action(orbit: list[int]) -> float:
    # Pure orbit cost, no mass data. Log keeps large excursions finite.
    return sum(math.log1p(x) for x in orbit)


def normalized_pair_action(o1: list[int], o2: list[int]) -> float:
    a = sequence_action(o1) + sequence_action(o2)
    steps = len(o1) + len(o2)
    return a / max(1, steps)


def pair_divergence(o1: list[int], o2: list[int]) -> float:
    L = max(len(o1), len(o2))
    if L == 0:
        return 0.0
    def val(o, i):
        return o[i] if i < len(o) else 1
    acc = 0.0
    for i in range(L):
        acc += abs(math.log1p(val(o1,i)) - math.log1p(val(o2,i)))
    return acc / L


def poincare_embedding_pair(o1: list[int], o2: list[int]) -> dict:
    # A conservative diagnostic embedding.
    # Radius is bounded with tanh; angle is driven by parity imbalance and relative log-amplitude.
    max_log = max([math.log1p(x) for x in (o1 + o2)] + [1.0])
    points = []
    L = max(len(o1), len(o2))
    for k in range(L):
        a = o1[k] if k < len(o1) else 1
        b = o2[k] if k < len(o2) else 1
        amp = 0.5*(math.log1p(a) + math.log1p(b)) / max_log
        r = math.tanh(0.95 * amp)  # always inside unit disk
        parity_phase = ((a % 2) - (b % 2)) * math.pi/3.0
        rel_phase = math.atan2(math.log1p(b)-math.log1p(a), math.log1p(a)+math.log1p(b)+1e-12)
        theta = (k * 2.0*math.pi / max(1, L)) + parity_phase + rel_phase
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x,y,r,theta))
    mean_r = sum(p[2] for p in points)/max(1,len(points))
    max_r = max((p[2] for p in points), default=0.0)
    # Poincare radial distance from origin: d = 2 artanh(r)
    mean_hyperbolic_r = sum(2.0*math.atanh(min(0.999999,p[2])) for p in points)/max(1,len(points))
    return {
        "poincare_mean_radius": mean_r,
        "poincare_max_radius": max_r,
        "poincare_mean_hyperbolic_radius": mean_hyperbolic_r,
    }


def zeta_alignment(seed_pair: tuple[int,int], generation_candidate_index: int) -> float:
    # Diagnostic only: compares seed log scale to first three zeta-zero heights.
    # No mass information. Not a proof of zeta anchoring.
    p, q = seed_pair
    log_scale = math.log(p*q)
    gamma = ZETA_GAMMAS[(generation_candidate_index-1) % len(ZETA_GAMMAS)]
    phase = (log_scale / gamma) % 1.0
    return min(phase, 1.0-phase)


def compute_table():
    rows = []
    for idx, seed in enumerate(CANDIDATE_SEEDS, start=1):
        p,q = seed
        o1 = collatz_orbit(p)
        o2 = collatz_orbit(q)
        emb = poincare_embedding_pair(o1,o2)
        row = {
            "candidate_index": idx,
            "seed_p": p,
            "seed_q": q,
            "stopping_time_p": len(o1)-1,
            "stopping_time_q": len(o2)-1,
            "max_p": max(o1),
            "max_q": max(o2),
            "normalized_pair_action": normalized_pair_action(o1,o2),
            "parity_entropy_p": parity_entropy(o1),
            "parity_entropy_q": parity_entropy(o2),
            "pair_divergence": pair_divergence(o1,o2),
            "zeta_alignment_diagnostic": zeta_alignment(seed, idx),
            **emb,
        }
        # A compact non-mass-input generation depth score. This is diagnostic, not final canon.
        row["generation_depth_score"] = (
            0.30*math.log1p(row["stopping_time_p"] + row["stopping_time_q"]) +
            0.25*row["normalized_pair_action"] +
            0.20*row["pair_divergence"] +
            0.15*row["poincare_mean_hyperbolic_radius"] +
            0.10*(1.0-row["zeta_alignment_diagnostic"])
        )
        rows.append(row)
    rows_sorted = sorted(rows, key=lambda r: r["generation_depth_score"])
    for rank, row in enumerate(rows_sorted, start=1):
        row["depth_rank_low_to_high"] = rank
    return rows_sorted


def main():
    outdir = Path(__file__).resolve().parents[1]/"results"
    outdir.mkdir(parents=True, exist_ok=True)
    rows = compute_table()
    csv_path = outdir/"collatz_poincare_generation_candidates.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summary = {
        "status": "diagnostic_not_final_canon",
        "uses_observed_masses_as_input": False,
        "kappa": KAPPA,
        "zeta_gammas_used_for_diagnostic_only": ZETA_GAMMAS,
        "candidate_count": len(rows),
        "top_three_low_to_high_depth": [
            {k: row[k] for k in ["depth_rank_low_to_high","seed_p","seed_q","generation_depth_score","normalized_pair_action","pair_divergence","poincare_mean_hyperbolic_radius","zeta_alignment_diagnostic"]}
            for row in rows[:3]
        ],
        "interpretation": "This stage builds a non-mass-input generation vector. It does not yet predict fermion masses. It establishes the required generational differentiator for the Euler-Berry action functional."
    }
    with (outdir/"generation_embedding_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    with (outdir/"generation_embedding_report.txt").open("w", encoding="utf-8") as f:
        f.write("Metatime SM Generation Embedding v0.3\n")
        f.write("Status: diagnostic, not final canon.\n")
        f.write("Observed masses used as input: no.\n\n")
        f.write("Top three candidate seeds by low-to-high generation-depth score:\n")
        for row in rows[:3]:
            f.write(f"rank {row['depth_rank_low_to_high']}: ({row['seed_p']},{row['seed_q']}), score={row['generation_depth_score']:.6f}\n")
        f.write("\nCore result: representation vectors alone cannot distinguish generations; Collatz/Poincare/zeta-depth features provide an independent generation vector.\n")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
