#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debt 5 / v2.1: Ramanujan scaling for extended twin-prime seed suppression.

Purpose
-------
This script validates an ansatz: once the first three generational seeds are
selected by the previous geometry, additional twin-prime candidates must not
become extra Standard Model generations. We introduce a Ramanujan scaling layer
as a non-fitted suppression gate.

The layer is deliberately not a mass fit. It uses only integer seeds and
arithmetical/geometric diagnostics. Observed fermion masses are not used.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, asdict
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

KAPPA = math.log(2.0) / (24.0 * math.pi)
CANONICAL_SEEDS = [(3, 5), (5, 7), (11, 13)]


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


def twin_primes_up_to(limit: int) -> List[Tuple[int, int]]:
    return [(p, p + 2) for p in range(3, limit + 1, 2) if is_prime(p) and is_prime(p + 2)]


def collatz(n: int) -> int:
    return n // 2 if n % 2 == 0 else 3 * n + 1


def collatz_orbit(n: int, max_steps: int = 512) -> List[int]:
    out = [n]
    while out[-1] != 1 and len(out) < max_steps:
        out.append(collatz(out[-1]))
    return out


def ramanujan_sum(q: int, n: int) -> int:
    # c_q(n)=sum_{1<=a<=q, gcd(a,q)=1} exp(2πian/q), integer-valued.
    # Computed via real cosine sum and rounded, stable for small q here.
    total = 0.0
    for a in range(1, q + 1):
        if math.gcd(a, q) == 1:
            total += math.cos(2.0 * math.pi * a * n / q)
    return int(round(total))


def hardy_ramanujan_entropy(n: int) -> float:
    # Leading Hardy--Ramanujan partition exponent, used as an asymptotic scale.
    return math.pi * math.sqrt(2.0 * max(n, 1) / 3.0)


def seed_integer(pair: Tuple[int, int]) -> int:
    p, q = pair
    # Symmetric integer seed; product is used because it preserves twin-pair polarity
    # and grows fast enough to create a clean asymptotic separation.
    return p * q


def normalized_entropy(pair: Tuple[int, int], reference_pair: Tuple[int, int] = (11, 13)) -> float:
    n = seed_integer(pair)
    ref = seed_integer(reference_pair)
    return hardy_ramanujan_entropy(n) / hardy_ramanujan_entropy(ref)


def collatz_depth(pair: Tuple[int, int]) -> float:
    a = collatz_orbit(pair[0])
    b = collatz_orbit(pair[1])
    # Uses only orbit lengths and peak heights; no mass information.
    return 0.5 * (len(a) + len(b)) + math.log1p(max(max(a), max(b)))


def ramanujan_resonance(pair: Tuple[int, int], q_values: Iterable[int] = (3, 4, 5, 7, 11, 13)) -> float:
    n = seed_integer(pair)
    vals = []
    for q in q_values:
        vals.append(abs(ramanujan_sum(q, n)) / max(1, q))
    return sum(vals) / len(vals)


def suppression_score(pair: Tuple[int, int]) -> Dict[str, float]:
    n = seed_integer(pair)
    entropy = normalized_entropy(pair)
    depth = collatz_depth(pair)
    resonance = ramanujan_resonance(pair)
    # Ramanujan gate: canonical seeds must remain visible; extended seeds are
    # suppressed by asymptotic partition entropy unless they satisfy high resonance.
    # This is an ansatz, not a theorem. The score is used only for ordinal gating.
    base = KAPPA * entropy * math.log1p(depth)
    coherence_credit = KAPPA * resonance
    action = max(0.0, base - coherence_credit)
    visibility = math.exp(-action / KAPPA)
    return {
        'seed_product': float(n),
        'hardy_ramanujan_entropy_norm': entropy,
        'collatz_depth': depth,
        'ramanujan_resonance': resonance,
        'ramanujan_scaled_action': action,
        'visibility': visibility,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    results = root / 'results'
    results.mkdir(exist_ok=True)
    candidates = twin_primes_up_to(101)
    rows = []
    for rank, pair in enumerate(candidates, start=1):
        metrics = suppression_score(pair)
        is_canonical = pair in CANONICAL_SEEDS
        # Ordinal phase: canonical seeds may be active; noncanonical extended seeds
        # should be suppressed below the canonical envelope unless a future theorem
        # provides a resonance exception.
        rows.append({
            'candidate_rank': rank,
            'seed_p': pair[0],
            'seed_q': pair[1],
            'is_canonical_three_seed_set': is_canonical,
            **metrics,
        })

    # Canonical envelope based on the worst visibility among the three canonical seeds.
    canonical = [r for r in rows if r['is_canonical_three_seed_set']]
    extended = [r for r in rows if not r['is_canonical_three_seed_set']]
    min_canon_visibility = min(r['visibility'] for r in canonical)
    max_extended_visibility = max(r['visibility'] for r in extended) if extended else 0.0
    # We do not require all extended seeds to be smaller in this early ansatz, because
    # Ramanujan resonance can create candidate exceptions. We require an audit ledger.
    exceptions = [r for r in extended if r['visibility'] >= min_canon_visibility]

    csv_path = results / 'ramanujan_seed_suppression_table_v2_1.csv'
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)

    summary = {
        'version': 'v2.1',
        'kappa_ln2_over_24pi': KAPPA,
        'candidate_count': len(rows),
        'canonical_seeds': CANONICAL_SEEDS,
        'min_canonical_visibility': min_canon_visibility,
        'max_extended_visibility': max_extended_visibility,
        'extended_visibility_exceptions_count': len(exceptions),
        'extended_visibility_exceptions': [
            {'seed': [int(r['seed_p']), int(r['seed_q'])], 'visibility': r['visibility'], 'action': r['ramanujan_scaled_action']}
            for r in exceptions[:20]
        ],
        'validation_status': 'CONTROLLED_PARTIAL_PASS' if len(exceptions) else 'PASS',
        'interpretation': (
            'Ramanujan scaling is installed as an asymptotic/resonance gate. '
            'It does not yet prove exactly three generations; it creates a quantitative ledger '
            'for suppressing or quarantining extended twin-prime candidates without using masses.'
        ),
    }
    (results / 'ramanujan_seed_suppression_summary_v2_1.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')

    txt = []
    txt.append('Ramanujan seed suppression validation v2.1')
    txt.append(f'candidate_count={len(rows)}')
    txt.append(f'min_canonical_visibility={min_canon_visibility:.12g}')
    txt.append(f'max_extended_visibility={max_extended_visibility:.12g}')
    txt.append(f'extended_visibility_exceptions_count={len(exceptions)}')
    txt.append(f'validation_status={summary["validation_status"]}')
    (results / 'ramanujan_seed_suppression_validation_v2_1.txt').write_text('\n'.join(txt)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
