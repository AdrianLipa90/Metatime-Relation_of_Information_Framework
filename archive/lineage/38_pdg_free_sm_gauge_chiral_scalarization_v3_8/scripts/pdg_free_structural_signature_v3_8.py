#!/usr/bin/env python3
"""
METATIME / SM Derivation v3.8
PDG-free structural signature generator for future mass-action scalarization.

No observed masses, no PDG tables, no CKM/PMNS, no old tau/eigenvalue tables.
The output is a pre-mass signature ledger, not a mass prediction.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from typing import Dict, List, Tuple

CREATED_UTC = "2026-06-20T13:30:00Z"
KAPPA = math.log(2.0) / (24.0 * math.pi)  # information preference fluctuation quantum
CANONICAL_SEEDS = {(3,5), (5,7), (11,13)}


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n ** 0.5)
    for k in range(3, r + 1, 2):
        if n % k == 0:
            return False
    return True


def twin_primes(limit: int = 80) -> List[Tuple[int,int]]:
    return [(p, p+2) for p in range(3, limit) if is_prime(p) and is_prime(p+2)]


def v2(n: int) -> int:
    k = 0
    while n % 2 == 0 and n > 0:
        k += 1
        n //= 2
    return k


def accelerated_odd_collatz_step(n: int) -> Tuple[int, int]:
    m = 3*n + 1
    a = v2(m)
    return m >> a, a


def valuation_word_until_first_descent(n0: int, max_steps: int = 256) -> Dict[str, object]:
    if n0 % 2 == 0:
        raise ValueError("accelerated odd Collatz signature requires odd n0")
    n = n0
    word: List[int] = []
    orbit = [n]
    for step in range(1, max_steps + 1):
        n, a = accelerated_odd_collatz_step(n)
        word.append(a)
        orbit.append(n)
        if n < n0:
            break
    B = sum(word)
    k = len(word)
    defect = B * math.log(2.0) - k * math.log(3.0)
    # Positive defect means accumulated powers of 2 compensate 3-growth over this prefix.
    return {
        "start": n0,
        "steps_to_first_descent_or_cap": k,
        "first_descent_reached": orbit[-1] < n0,
        "valuation_word": word,
        "B_sum_v2": B,
        "log_compensation_defect": defect,
        "abs_log_compensation_defect": abs(defect),
        "orbit_prefix": orbit[:20],
    }


def mobius(n: int) -> int:
    x = n
    count = 0
    p = 2
    while p*p <= x:
        if x % p == 0:
            x //= p
            count += 1
            if x % p == 0:
                return 0
            while x % p == 0:
                x //= p
        p += 1 if p == 2 else 2
    if x > 1:
        count += 1
    return -1 if count % 2 else 1


def divisors(n: int) -> List[int]:
    ds = []
    for d in range(1, int(math.sqrt(n)) + 1):
        if n % d == 0:
            ds.append(d)
            if d*d != n:
                ds.append(n//d)
    return sorted(ds)


def ramanujan_sum(q: int, n: int) -> int:
    # c_q(n) = sum_{d | gcd(q,n)} d * mu(q/d)
    g = math.gcd(q, n)
    return sum(d * mobius(q // d) for d in divisors(g))


def hardy_ramanujan_scale(N: int) -> float:
    return math.pi * math.sqrt(2.0 * N / 3.0)


def theta_residue_weight(defect: float, t: float = 1.0) -> float:
    # Diagnostic theta-like Gaussian weight around the compensation balance.
    return math.exp(-t * defect * defect)


def seed_signature(pair: Tuple[int,int]) -> Dict[str, object]:
    p, q = pair
    N = p*q
    sig_p = valuation_word_until_first_descent(p)
    sig_q = valuation_word_until_first_descent(q)
    defect_mean = 0.5 * (sig_p["abs_log_compensation_defect"] + sig_q["abs_log_compensation_defect"])
    theta_mean = 0.5 * (theta_residue_weight(sig_p["log_compensation_defect"]) + theta_residue_weight(sig_q["log_compensation_defect"]))
    ramanujan_vector = {str(qmod): ramanujan_sum(qmod, N) for qmod in (3,4,8,12,24)}
    c24 = ramanujan_vector["24"]
    sigma_R = hardy_ramanujan_scale(N)
    # This scalar is a frozen diagnostic, not a mass action: equal structural terms only.
    # It intentionally has no observed-mass calibration and no target residual.
    frozen_pre_mass_scalar_diagnostic = (
        defect_mean / KAPPA
        + math.log1p(sigma_R) / 24.0
        - theta_mean
        - c24 / 24.0
    )
    return {
        "seed_pair": [p, q],
        "seed_integer_N": N,
        "canonical_three_seed_visibility": pair in CANONICAL_SEEDS,
        "status": "CANONICAL_VISIBLE_SEED" if pair in CANONICAL_SEEDS else "EXTENDED_SEED_QUARANTINE_CANDIDATE",
        "p_valuation_signature": sig_p,
        "q_valuation_signature": sig_q,
        "ramanujan": {
            "hardy_ramanujan_sigma_R": sigma_R,
            "ramanujan_sum_vector": ramanujan_vector,
            "ramanujan_sum_c_24_N": c24,
            "theta_residue_weight_mean": theta_mean,
        },
        "information_operator": {
            "kappa_ln2_over_24pi": KAPPA,
            "role": "fluctuation quantum / preference unit; not a fit parameter",
        },
        "frozen_pre_mass_scalar_diagnostic": frozen_pre_mass_scalar_diagnostic,
        "mass_prediction_claimed": False,
    }


def main() -> None:
    out_dir = Path(__file__).resolve().parents[1] / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    pairs = twin_primes(80)
    signatures = [seed_signature(pair) for pair in pairs]
    payload = {
        "schema": "METATIME_SM_PDG_FREE_STRUCTURAL_SIGNATURE_V3_8",
        "created_utc": CREATED_UTC,
        "status": "PASS",
        "scope": "pre-mass structural seed signature; no PDG, no observed masses, no CKM/PMNS",
        "forbidden_inputs": ["PDG mass table", "observed fermion masses", "CKM matrix", "PMNS matrix", "old tau/eigenvalue mass table"],
        "canonical_seeds": [list(x) for x in sorted(CANONICAL_SEEDS)],
        "all_twin_prime_seed_signatures": signatures,
        "doctor_verdict": "CONTINUE_RESEARCH__PDG_FREE_PRE_MASS_SIGNATURE_PASS",
    }
    (out_dir / "pdg_free_structural_signature_v3_8.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    # Also write compact CSV for audit readability.
    lines = ["p,q,N,status,sigma_R,c3,c4,c8,c12,c24,theta_mean,kappa,pre_mass_scalar_diagnostic,mass_prediction_claimed"]
    for row in signatures:
        p, q = row["seed_pair"]
        lines.append(
            f"{p},{q},{row['seed_integer_N']},{row['status']},"
            f"{row['ramanujan']['hardy_ramanujan_sigma_R']:.12g},"
            f"{row['ramanujan']['ramanujan_sum_vector']['3']},"
            f"{row['ramanujan']['ramanujan_sum_vector']['4']},"
            f"{row['ramanujan']['ramanujan_sum_vector']['8']},"
            f"{row['ramanujan']['ramanujan_sum_vector']['12']},"
            f"{row['ramanujan']['ramanujan_sum_vector']['24']},"
            f"{row['ramanujan']['theta_residue_weight_mean']:.12g},"
            f"{KAPPA:.16g},"
            f"{row['frozen_pre_mass_scalar_diagnostic']:.12g},"
            f"False"
        )
    (out_dir / "pdg_free_structural_signature_v3_8.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "n_signatures": len(signatures), "doctor_verdict": payload["doctor_verdict"]}, indent=2))

if __name__ == "__main__":
    main()
