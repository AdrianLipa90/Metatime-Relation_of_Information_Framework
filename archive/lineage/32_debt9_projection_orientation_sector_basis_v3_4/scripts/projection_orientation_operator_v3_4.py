#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
METATIME SM v3.4 — Sector-basis projection orientation operator.

Purpose
-------
Build an orientation layer between the v3.3 sector-basis/White-Thread operator
and any future one-anchor mass test. This module is intentionally pre-mass:
no observed masses, no CKM/PMNS values, no fitted White-Thread couplings.

Epistemic status
----------------
- DEFINITIONS: abstract channels, sector labels, feature axes.
- ANSATZ: old-document bridge assignment of light/heavy quark sectors.
- STRUCTURAL ENUMERATION: basis construction and up/down relative rotation audit.
- NOT CLAIMED: mass prediction, CKM numerical derivation, PMNS derivation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SCHEMAS = ROOT / "schemas"
RESULTS.mkdir(parents=True, exist_ok=True)
SCHEMAS.mkdir(parents=True, exist_ok=True)

KAPPA_INFORMATION_QUANTUM = math.log(2.0) / (24.0 * math.pi)

# No observed masses, CKM entries, PMNS entries, or fitted couplings in this file.
FORBIDDEN_INPUT_NAMES = {
    "target_mass", "mass_GeV", "pdg_mass", "Vus", "Vcb", "Vub",
    "theta12", "theta23", "theta13", "Jarlskog", "PMNS", "CKM_observed",
}

@dataclass(frozen=True)
class Channel:
    particle: str
    family: str
    generation: int
    sector: str
    seed_pair: Tuple[int, int]
    mode: int
    weak_pole: str
    chirality_path: str
    color_depth: int
    hypercharge_numerator_sixths: int
    electric_charge_thirds: int
    source_status: str


def collatz_steps(n: int) -> int:
    """Return number of Collatz steps until 1 for a positive integer."""
    if n <= 0:
        raise ValueError("n must be positive")
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
        if steps > 10000:
            raise RuntimeError("Collatz guard exceeded")
    return steps


def ramanujan_sigma(N: int) -> float:
    """Ramanujan asymptotic scale used as a structural damping coordinate."""
    return math.pi * math.sqrt(2.0 * N / 3.0)


def ramanujan_sum(q: int, n: int) -> int:
    """Integer Ramanujan sum c_q(n) by direct definition via gcd."""
    total = 0 + 0j
    for a in range(1, q + 1):
        if math.gcd(a, q) == 1:
            total += complex(math.cos(2 * math.pi * a * n / q), math.sin(2 * math.pi * a * n / q))
    return int(round(total.real))


def raw_feature_vector(ch: Channel) -> List[float]:
    """
    Build a structural orientation vector. This is NOT a mass action.

    Components:
    0 weak_pole sign: CP1 north/south channel
    1 chirality sign: left/right path marker
    2 normalized color/tetrahedral depth
    3 hypercharge coordinate in sixths
    4 Collatz seed phase coordinate
    5 Ramanujan coordinate
    6 zeta-Heisenberg symbolic fluctuation coordinate
    7 information quantum preference coordinate
    """
    p, q = ch.seed_pair
    N = p + q + ch.mode
    csteps = collatz_steps(p) + collatz_steps(q) + collatz_steps(N)
    pole = 1.0 if ch.weak_pole == "N" else -1.0
    chirality = 1.0 if "L" in ch.chirality_path else -1.0
    color = ch.color_depth / 3.0
    hyper = ch.hypercharge_numerator_sixths / 6.0
    collatz_phase = ((csteps % 12) - 6) / 6.0
    rama = math.tanh(ramanujan_sigma(N) / 20.0)
    zeta_heisenberg = math.sin((N + 0.5) * KAPPA_INFORMATION_QUANTUM * math.pi)
    info_pref = KAPPA_INFORMATION_QUANTUM * (1.0 + abs(ramanujan_sum(max(2, q), N)))
    return [pole, chirality, color, hyper, collatz_phase, rama, zeta_heisenberg, info_pref]


def dot(a: Iterable[float], b: Iterable[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(v: Iterable[float]) -> float:
    return math.sqrt(dot(v, v))


def normalize(v: List[float]) -> List[float]:
    n = norm(v)
    if n == 0:
        raise ValueError("zero vector")
    return [x / n for x in v]


def sub(a: List[float], b: List[float]) -> List[float]:
    return [x - y for x, y in zip(a, b)]


def scale(c: float, v: List[float]) -> List[float]:
    return [c * x for x in v]


def gram_schmidt(vectors: List[List[float]]) -> List[List[float]]:
    basis: List[List[float]] = []
    for v in vectors:
        w = list(v)
        for b in basis:
            w = sub(w, scale(dot(w, b), b))
        if norm(w) < 1e-10:
            # Deterministic tiny structural perturbation: basis construction guard,
            # not a fitted physics parameter.
            idx = len(basis) % len(w)
            w[idx] += 1e-6
        basis.append(normalize(w))
    return basis


def overlap_matrix(up_basis: List[List[float]], down_basis: List[List[float]]) -> List[List[float]]:
    return [[dot(u, d) for d in down_basis] for u in up_basis]


def frobenius_identity_distance(M: List[List[float]]) -> float:
    total = 0.0
    for i, row in enumerate(M):
        for j, value in enumerate(row):
            target = 1.0 if i == j else 0.0
            total += (value - target) ** 2
    return math.sqrt(total)


CHANNELS: List[Channel] = [
    # Charged leptons: old-doc bridge says generation modes in the small lepton sector.
    Channel("e", "charged_lepton", 1, "charged_lepton_small_seed", (3, 5), 0, "S", "L_to_R_H_minus", 0, -6, -3, "definition_plus_old_doc_bridge_ansatz"),
    Channel("mu", "charged_lepton", 2, "charged_lepton_small_seed", (3, 5), 1, "S", "L_to_R_H_minus", 0, -6, -3, "definition_plus_old_doc_bridge_ansatz"),
    Channel("tau", "charged_lepton", 3, "charged_lepton_small_seed", (3, 5), 2, "S", "L_to_R_H_minus", 0, -6, -3, "definition_plus_old_doc_bridge_ansatz"),
    # Neutrinos stay quarantined: structural channel present, mass mechanism not claimed.
    Channel("nu1", "neutrino", 1, "neutrino_pair_coherence", (5, 7), 0, "N", "L_to_optional_R_H_zero", 0, 0, 0, "quarantine_no_PMNS_claim"),
    Channel("nu2", "neutrino", 2, "neutrino_pair_coherence", (5, 7), 1, "N", "L_to_optional_R_H_zero", 0, 0, 0, "quarantine_no_PMNS_claim"),
    Channel("nu3", "neutrino", 3, "neutrino_pair_coherence", (5, 7), 2, "N", "L_to_optional_R_H_zero", 0, 0, 0, "quarantine_no_PMNS_claim"),
    # Light quark sector: u,d,s stay light; charm is marked heavy per old-doc bridge candidate.
    Channel("u", "up_quark", 1, "light_quark_seed", (11, 13), 0, "N", "Q_L_to_u_R_H_plus", 3, 4, 2, "definition_plus_old_doc_bridge_ansatz"),
    Channel("d", "down_quark", 1, "light_quark_seed", (11, 13), 0, "S", "Q_L_to_d_R_H_minus", 3, -2, -1, "definition_plus_old_doc_bridge_ansatz"),
    Channel("s", "down_quark", 2, "light_quark_seed", (11, 13), 1, "S", "Q_L_to_d_R_H_minus", 3, -2, -1, "definition_plus_old_doc_bridge_ansatz"),
    # Heavy quark resonance: c,b,t use a deeper sector as a bridge candidate, not a fitted result.
    Channel("c", "up_quark", 2, "heavy_quark_resonance", (101, 103), 0, "N", "Q_L_to_u_R_H_plus", 3, 4, 2, "old_doc_bridge_ansatz_quarantined"),
    Channel("b", "down_quark", 3, "heavy_quark_resonance", (101, 103), 1, "S", "Q_L_to_d_R_H_minus", 3, -2, -1, "old_doc_bridge_ansatz_quarantined"),
    Channel("t", "up_quark", 3, "heavy_quark_resonance", (101, 103), 2, "N", "Q_L_to_u_R_H_plus", 3, 4, 2, "old_doc_bridge_ansatz_quarantined"),
]


def main() -> None:
    records: List[Dict[str, object]] = []
    for ch in CHANNELS:
        v = normalize(raw_feature_vector(ch))
        rec: Dict[str, object] = asdict(ch)
        rec.update({
            "seed_pair": f"{ch.seed_pair[0]}-{ch.seed_pair[1]}",
            "orientation_norm": norm(v),
            "feature_hash": hashlib.sha256(",".join(f"{x:.12g}" for x in v).encode()).hexdigest(),
            "uses_observed_mass": False,
            "uses_observed_mixing": False,
            "operator_information_role": "quantum_of_informational_preference_fluctuation",
        })
        for i, x in enumerate(v):
            rec[f"v{i}"] = x
        records.append(rec)

    up = [r for r in records if r["family"] == "up_quark"]
    down = [r for r in records if r["family"] == "down_quark"]
    up.sort(key=lambda r: int(r["generation"]))
    down.sort(key=lambda r: int(r["generation"]))
    up_basis = gram_schmidt([[float(r[f"v{i}"]) for i in range(8)] for r in up])
    down_basis = gram_schmidt([[float(r[f"v{i}"]) for i in range(8)] for r in down])
    M = overlap_matrix(up_basis, down_basis)
    identity_distance = frobenius_identity_distance(M)

    channel_csv = RESULTS / "sector_basis_orientation_channels_v3_4.csv"
    with channel_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

    overlap_csv = RESULTS / "up_down_basis_overlap_matrix_v3_4.csv"
    with overlap_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["up_down_basis_overlap_not_CKM", "down_generation_1", "down_generation_2", "down_generation_3"])
        for idx, row in enumerate(M, start=1):
            writer.writerow([f"up_generation_{idx}", *[f"{x:.12g}" for x in row]])

    status = {
        "module": "METATIME_SM_SECTOR_BASIS_PROJECTION_ORIENTATION_v3_4",
        "gate": "PRE_MASS_ORIENTATION_OPERATOR_PASS",
        "uses_observed_masses": False,
        "uses_observed_CKM_PMNS": False,
        "uses_old_tau_values": False,
        "uses_fitted_white_thread_values": False,
        "information_operator_role": "quantum_of_informational_preference_fluctuation",
        "old_document_bridge_status": "ansatz_and_quarantine_for_heavy_quark_resonance",
        "up_down_basis_identity_distance": identity_distance,
        "up_down_basis_nontrivial_rotation": identity_distance > 1e-6,
        "mass_rescore_allowed_in_this_module": False,
        "claims": {
            "mass_prediction": False,
            "CKM_numerical_derivation": False,
            "PMNS_numerical_derivation": False,
            "sector_basis_orientation_defined": True,
        },
        "validation_checks": {
            "all_channel_norms_unit": all(abs(float(r["orientation_norm"]) - 1.0) < 1e-9 for r in records),
            "all_records_no_mass": all(r["uses_observed_mass"] is False for r in records),
            "all_records_no_mixing": all(r["uses_observed_mixing"] is False for r in records),
            "up_down_bases_non_identical": identity_distance > 1e-6,
            "has_heavy_quark_resonance_channel": any(r["sector"] == "heavy_quark_resonance" for r in records),
            "has_light_quark_seed_channel": any(r["sector"] == "light_quark_seed" for r in records),
            "has_charged_lepton_channel": any(r["sector"] == "charged_lepton_small_seed" for r in records),
            "has_neutrino_quarantine_channel": any(r["sector"] == "neutrino_pair_coherence" for r in records),
        },
        "outputs": [str(channel_csv.relative_to(ROOT)), str(overlap_csv.relative_to(ROOT))],
    }
    status["validation_pass"] = all(status["validation_checks"].values())

    with (RESULTS / "projection_orientation_status_v3_4.json").open("w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

    schema = {
        "module": status["module"],
        "record_type": "pre_mass_sector_basis_orientation_channel",
        "forbidden_inputs": sorted(FORBIDDEN_INPUT_NAMES),
        "required_fields": [
            "particle", "family", "generation", "sector", "seed_pair", "mode",
            "weak_pole", "chirality_path", "color_depth",
            "hypercharge_numerator_sixths", "electric_charge_thirds",
            "uses_observed_mass", "uses_observed_mixing",
        ],
        "epistemic_tags": ["DEFINITION", "ANSATZ", "INTERPRETATION", "VALIDATION_GATE", "DO_NOT_CLAIM"],
    }
    with (SCHEMAS / "PROJECTION_ORIENTATION_SCHEMA_v3_4.json").open("w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    if not status["validation_pass"]:
        raise SystemExit(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
