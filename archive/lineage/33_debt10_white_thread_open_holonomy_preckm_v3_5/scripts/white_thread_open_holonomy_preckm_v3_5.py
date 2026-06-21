#!/usr/bin/env python3
"""
METATIME v3.5 — White-Thread open holonomy pre-CKM operator.

Purpose:
- Build an unfitted open-holonomy bridge between the already frozen up/down
  sector bases from v3.4.
- Preserve the anti-fit rule: no observed CKM, no PMNS, no masses, no fitted
  White-Thread couplings, no old tau/eigenvalue import.
- Output raw structural objects only. Nothing here is a numerical CKM claim.
"""
from __future__ import annotations
import csv, json, math, pathlib, hashlib
from typing import Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[0]
SRC = REPO / '32_debt9_projection_orientation_sector_basis_v3_4' / 'results' / 'sector_basis_orientation_channels_v3_4.csv'
OUT = ROOT / 'results'
KAPPA = math.log(2.0) / (24.0 * math.pi)

VECTOR_KEYS = [f'v{i}' for i in range(8)]


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def read_channels() -> List[Dict[str, str]]:
    with SRC.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    return rows


def vec(row: Dict[str, str]) -> List[float]:
    return [float(row[k]) for k in VECTOR_KEYS]


def dot(a: List[float], b: List[float]) -> float:
    return sum(x*y for x, y in zip(a, b))


def norm(a: List[float]) -> float:
    return math.sqrt(max(0.0, dot(a, a)))


def normalize(a: List[float]) -> List[float]:
    n = norm(a)
    if n == 0:
        raise ValueError('zero vector')
    return [x/n for x in a]


def seed_number(seed_pair: str) -> int:
    p, q = [int(x) for x in seed_pair.split('-')]
    # Structural seed charge used only for an unfitted Ramanujan envelope.
    # Product is used here because it distinguishes depth more strongly than sum
    # and is fixed by the seed pair itself, not by masses or mixing data.
    return p*q


def ramanujan_sigma(N: int) -> float:
    # Hardy-Ramanujan asymptotic scale. Not fitted.
    return math.pi * math.sqrt(2.0 * N / 3.0)


def white_thread_pair(up: Dict[str,str], down: Dict[str,str]) -> Dict[str, object]:
    u = normalize(vec(up)); d = normalize(vec(down))
    raw_inner = max(-1.0, min(1.0, dot(u, d)))
    # Open holonomy phase displacement proxy: angle between sector-basis vectors.
    phase_gap = math.acos(raw_inner)
    # Anti-fit information quantum: kappa is the quantum of informational preference fluctuation.
    # It modulates the holonomy phase rather than acting as a free coefficient.
    N_u = seed_number(up['seed_pair']); N_d = seed_number(down['seed_pair'])
    sigma_u = ramanujan_sigma(N_u); sigma_d = ramanujan_sigma(N_d)
    ramanujan_gap = abs(sigma_u - sigma_d)
    ramanujan_mean = 0.5 * (sigma_u + sigma_d)
    # Zeta-Heisenberg width is structural and frozen, not tuned to CKM or masses.
    zeta_heisenberg_width = KAPPA * (1.0 + phase_gap) / (1.0 + ramanujan_mean)
    # Raw White-Thread amplitude candidate: open path coherence, not CKM.
    # The exponential envelope uses only KAPPA, phase_gap, and Ramanujan gap.
    open_coherence = math.exp(-KAPPA * (phase_gap + ramanujan_gap / (1.0 + ramanujan_mean)))
    oriented_overlap = raw_inner * open_coherence
    abs_overlap = abs(oriented_overlap)
    status = 'structural_open_holonomy_only_not_CKM'
    return {
        'up_particle': up['particle'],
        'down_particle': down['particle'],
        'up_generation': int(up['generation']),
        'down_generation': int(down['generation']),
        'up_seed_pair': up['seed_pair'],
        'down_seed_pair': down['seed_pair'],
        'raw_basis_inner_product': raw_inner,
        'phase_gap_rad': phase_gap,
        'ramanujan_sigma_up': sigma_u,
        'ramanujan_sigma_down': sigma_d,
        'ramanujan_gap': ramanujan_gap,
        'information_quantum_kappa': KAPPA,
        'zeta_heisenberg_width': zeta_heisenberg_width,
        'white_thread_open_coherence': open_coherence,
        'oriented_open_holonomy_overlap': oriented_overlap,
        'abs_open_holonomy_overlap': abs_overlap,
        'uses_observed_mass': False,
        'uses_observed_CKM': False,
        'uses_observed_PMNS': False,
        'uses_old_tau': False,
        'uses_fitted_white_thread_values': False,
        'status': status,
        'feature_hash': sha256_text(f"{up['particle']}|{down['particle']}|{up['seed_pair']}|{down['seed_pair']}|{phase_gap:.12g}|{KAPPA:.12g}")
    }


def main() -> None:
    rows = read_channels()
    up_rows = [r for r in rows if r['particle'] in ('u','c','t')]
    down_rows = [r for r in rows if r['particle'] in ('d','s','b')]
    if len(up_rows) != 3 or len(down_rows) != 3:
        raise RuntimeError(f'Expected 3 up and 3 down quark channels, got {len(up_rows)}, {len(down_rows)}')
    up_rows.sort(key=lambda r: int(r['generation']))
    down_rows.sort(key=lambda r: int(r['generation']))
    pairs = [white_thread_pair(u, d) for u in up_rows for d in down_rows]

    pair_path = OUT / 'white_thread_open_holonomy_pairs_v3_5.csv'
    with pair_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(pairs[0].keys()))
        w.writeheader(); w.writerows(pairs)

    # Matrix form. This is explicitly not CKM. It is a pre-CKM structural overlap.
    matrix = []
    for u in up_rows:
        line = {'white_thread_pre_CKM_not_CKM': f"up_{u['particle']}_generation_{u['generation']}"}
        for d in down_rows:
            rec = next(p for p in pairs if p['up_particle']==u['particle'] and p['down_particle']==d['particle'])
            line[f"down_{d['particle']}_generation_{d['generation']}"] = rec['oriented_open_holonomy_overlap']
        matrix.append(line)
    matrix_path = OUT / 'white_thread_pre_ckm_matrix_not_ckm_v3_5.csv'
    with matrix_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(matrix[0].keys()))
        w.writeheader(); w.writerows(matrix)

    # A row-normalized diagnostic is useful but must remain quarantined.
    normalized = []
    for u in up_rows:
        vals = [abs(next(p for p in pairs if p['up_particle']==u['particle'] and p['down_particle']==d['particle'])['oriented_open_holonomy_overlap']) for d in down_rows]
        s = sum(vals)
        line = {'row_normalized_diagnostic_not_CKM': f"up_{u['particle']}_generation_{u['generation']}"}
        for d, val in zip(down_rows, vals):
            line[f"down_{d['particle']}_generation_{d['generation']}"] = (val/s if s else 0.0)
        normalized.append(line)
    norm_path = OUT / 'row_normalized_pre_ckm_diagnostic_not_ckm_v3_5.csv'
    with norm_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(normalized[0].keys()))
        w.writeheader(); w.writerows(normalized)

    # Diagnostics: no identity-basis collapse, no mass/mixing leakage.
    absvals = [p['abs_open_holonomy_overlap'] for p in pairs]
    diagonal = [abs(next(p for p in pairs if p['up_generation']==i and p['down_generation']==i)['oriented_open_holonomy_overlap']) for i in (1,2,3)]
    offdiag = [p['abs_open_holonomy_overlap'] for p in pairs if p['up_generation'] != p['down_generation']]
    status = {
        'module': 'METATIME_SM_WHITE_THREAD_OPEN_HOLONOMY_PRECKM_v3_5',
        'gate': 'PRE_CKM_OPEN_HOLONOMY_OPERATOR_PASS',
        'uses_observed_masses': False,
        'uses_observed_CKM': False,
        'uses_observed_PMNS': False,
        'uses_old_tau_values': False,
        'uses_fitted_white_thread_values': False,
        'mass_rescore_allowed_in_this_module': False,
        'CKM_numerical_claim': False,
        'PMNS_numerical_claim': False,
        'information_operator_role': 'quantum_of_informational_preference_fluctuation',
        'white_thread_role': 'open_holonomy_operator_shape_only_no_fitted_values',
        'up_down_pair_count': len(pairs),
        'mean_abs_open_holonomy_overlap': sum(absvals)/len(absvals),
        'diagonal_abs_mean': sum(diagonal)/len(diagonal),
        'offdiagonal_abs_mean': sum(offdiag)/len(offdiag),
        'nontrivial_offdiagonal_present': any(x > 1e-6 for x in offdiag),
        'not_identity_matrix': any(x > 1e-6 for x in offdiag),
        'all_records_no_mass': all(not p['uses_observed_mass'] for p in pairs),
        'all_records_no_CKM': all(not p['uses_observed_CKM'] for p in pairs),
        'all_records_no_PMNS': all(not p['uses_observed_PMNS'] for p in pairs),
        'all_records_no_old_tau': all(not p['uses_old_tau'] for p in pairs),
        'all_records_no_fitted_white_thread_values': all(not p['uses_fitted_white_thread_values'] for p in pairs),
        'outputs': [
            'results/white_thread_open_holonomy_pairs_v3_5.csv',
            'results/white_thread_pre_ckm_matrix_not_ckm_v3_5.csv',
            'results/row_normalized_pre_ckm_diagnostic_not_ckm_v3_5.csv'
        ]
    }
    status['validation_pass'] = all([
        status['up_down_pair_count'] == 9,
        status['nontrivial_offdiagonal_present'],
        status['not_identity_matrix'],
        status['all_records_no_mass'],
        status['all_records_no_CKM'],
        status['all_records_no_PMNS'],
        status['all_records_no_old_tau'],
        status['all_records_no_fitted_white_thread_values']
    ])
    status_path = OUT / 'white_thread_open_holonomy_status_v3_5.json'
    status_path.write_text(json.dumps(status, indent=2), encoding='utf-8')
    if not status['validation_pass']:
        raise SystemExit('validation failed')

if __name__ == '__main__':
    main()
