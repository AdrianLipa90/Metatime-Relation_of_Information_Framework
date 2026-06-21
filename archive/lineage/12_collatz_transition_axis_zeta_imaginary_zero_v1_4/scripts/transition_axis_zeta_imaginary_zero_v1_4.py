#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collatz terminal transition axis and zeta imaginary-zero axis kernel v1.4.

Purpose
-------
This module corrects the transition order used by the Standard Model derivation
workbench:

    tetrahedral depth -> Poincare disk -> Collatz trajectory -> terminal axis

The terminal Collatz axis is extended from the integer terminal cycle
4 -> 2 -> 1 to the projective spin-half endpoint 1/2.  The extra 1/2 is not
an integer Collatz iterate.  It is the phase/spin projection point at which the
integer terminal cycle is tied to Euler spin closure and to the Riemann critical
line Re(s)=1/2.

The zeta layer is treated as an imaginary spectral axis over the common half
anchor.  A non-trivial zeta zero is represented as 1/2 + i gamma_n.  The zero
condition itself is not used as a fitted mass cost; it is used as a phase-axis
coherence anchor.

No observed fermion masses are used by this module.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

ZETA_GAMMAS = [
    14.134725141734693790457251983562470270784257115699,
    21.022039638771554992628479593896902777334340524903,
    25.010857580145688763213790992562821818659549672557,
    30.424876125859513210311897530584091320181560023715,
    32.935061587739189690662368964074903488812715603517,
    37.586178158825671257217763480705332821405597350830,
    40.918719012147495187398126914633254395726165962777,
    43.327073280914999519496122165406805782645668371836,
    48.005150881167159727942472749427516041686844001144,
    49.773832477672302181916784678563724057723178299677,
]

TWIN_PRIME_SEEDS = [(3, 5), (5, 7), (11, 13)]
TERMINAL_AXIS = [4.0, 2.0, 1.0, 0.5]
KAPPA = math.log(2.0) / (24.0 * math.pi)
PHI = (1.0 + math.sqrt(5.0)) / 2.0
SPIN_HALF = 0.5


def collatz_step(n: int) -> int:
    if n <= 0:
        raise ValueError("Collatz seed must be positive")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def collatz_sequence(n: int, max_steps: int = 10000) -> List[int]:
    seq = [n]
    while seq[-1] != 1:
        if len(seq) > max_steps:
            raise RuntimeError(f"Collatz sequence exceeded {max_steps} steps for n={n}")
        seq.append(collatz_step(seq[-1]))
    return seq


def terminal_axis_tail(seq: List[int]) -> List[float]:
    """Return the terminal 4->2->1->1/2 tail when the sequence contains 4,2,1."""
    # Every tested positive Collatz sequence reaches 1 and normally contains 4,2,1.
    # The half endpoint is appended as a spin/projective endpoint, not as Collatz(n).
    if len(seq) >= 3 and seq[-3:] == [4, 2, 1]:
        return [4.0, 2.0, 1.0, 0.5]
    # For seeds that begin at 1 or 2 the integer terminal tail is shorter; still append
    # the projective endpoint for consistency.
    tail = []
    for x in [4, 2, 1]:
        if x in seq:
            tail.append(float(x))
    if not tail or tail[-1] != 1.0:
        tail.append(1.0)
    tail.append(0.5)
    return tail


def parity_signature(seq: List[int]) -> str:
    return ''.join('E' if n % 2 == 0 else 'O' for n in seq)


def poincare_radius_from_pair(seq_a: List[int], seq_b: List[int]) -> float:
    """A deterministic disk radius derived only from orbit lengths.

    Radius stays strictly inside the unit disk.  The formula is a structural
    diagnostic, not a fitted mass rule.
    """
    la, lb = len(seq_a) - 1, len(seq_b) - 1
    raw = abs(la - lb) + 1
    scale = la + lb + 2
    return raw / scale


def zeta_index_for_seed(p: int, q: int, sig_a: str, sig_b: str) -> int:
    """Deterministic zeta-axis selector, independent of masses.

    Uses only seed arithmetic and Collatz parity signatures.  Returns a zero-based
    index into ZETA_GAMMAS.
    """
    parity_weight = (sig_a.count('O') + 2 * sig_b.count('O') + sig_a.count('E'))
    return (p + q + parity_weight) % len(ZETA_GAMMAS)


def seed_record(seed: Tuple[int, int]) -> Dict[str, object]:
    p, q = seed
    seq_p = collatz_sequence(p)
    seq_q = collatz_sequence(q)
    tail_p = terminal_axis_tail(seq_p)
    tail_q = terminal_axis_tail(seq_q)
    sig_p = parity_signature(seq_p)
    sig_q = parity_signature(seq_q)
    zi = zeta_index_for_seed(p, q, sig_p, sig_q)
    gamma = ZETA_GAMMAS[zi]
    r = poincare_radius_from_pair(seq_p, seq_q)
    # Axis coherence diagnostics.
    # terminal_half_lock is exact when both branches end in appended 1/2 endpoint.
    terminal_half_lock = (tail_p[-1] == 0.5 and tail_q[-1] == 0.5)
    # Critical-line lock is exact by construction: Re(zeta zero coordinate)=1/2.
    critical_line_lock = True
    # Imaginary-axis phase is a bounded diagnostic of the selected gamma_n.
    zeta_phase_mod_tau = gamma % (2.0 * math.pi)
    # Combined transition-axis score.  This is not a mass prediction; it measures
    # compatibility of terminal Collatz axis, spin-half anchor, and zeta imaginary axis.
    fibonacci_tension = abs((len(seq_p) + 1) / (len(seq_q) + 1) - 1.0 / PHI)
    kepler_like_period = (r ** 1.5) if r > 0 else 0.0
    axis_action = KAPPA * (SPIN_HALF + fibonacci_tension + kepler_like_period + zeta_phase_mod_tau / (2.0 * math.pi))
    return {
        'seed_p': p,
        'seed_q': q,
        'collatz_steps_p': len(seq_p) - 1,
        'collatz_steps_q': len(seq_q) - 1,
        'terminal_tail_p': '->'.join(str(x).rstrip('0').rstrip('.') if x != 0.5 else '1/2' for x in tail_p),
        'terminal_tail_q': '->'.join(str(x).rstrip('0').rstrip('.') if x != 0.5 else '1/2' for x in tail_q),
        'terminal_half_lock': terminal_half_lock,
        'zeta_zero_index_1based': zi + 1,
        'zeta_gamma': gamma,
        'zeta_coordinate': f'1/2 + i*{gamma:.15f}',
        'critical_line_lock': critical_line_lock,
        'poincare_radius': r,
        'fibonacci_tension': fibonacci_tension,
        'kepler_like_period': kepler_like_period,
        'zeta_phase_mod_tau': zeta_phase_mod_tau,
        'axis_action': axis_action,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    results = root / 'results'
    results.mkdir(parents=True, exist_ok=True)
    records = [seed_record(seed) for seed in TWIN_PRIME_SEEDS]
    csv_path = results / 'transition_axis_zeta_imaginary_zero_v1_4.csv'
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)
    summary = {
        'module': 'collatz_transition_axis_zeta_imaginary_zero_v1_4',
        'canonical_transition_axis': '4 -> 2 -> 1 -> 1/2',
        'half_endpoint_meaning': 'spin/projective endpoint, not an integer Collatz iterate',
        'zeta_axis_meaning': 'imaginary spectral axis over the critical-line half anchor',
        'kappa': KAPPA,
        'all_terminal_half_locked': all(r['terminal_half_lock'] for r in records),
        'all_critical_line_locked': all(r['critical_line_lock'] for r in records),
        'records': records,
    }
    with (results / 'transition_axis_summary_v1_4.json').open('w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
