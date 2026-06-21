#!/usr/bin/env python3
"""
Module 57 / v5.7: Triplet W_ij hadronization aggregator.

This executable intentionally does NOT use old mass solvers, PDG tables as inputs,
or exact hadron reference replay. Benchmarks, where present, are post-freeze scoring
only and cannot close Debt 9.
"""
import json, math, csv, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parents[1]
RESULTS = MODULE_DIR / 'results'
DATA = MODULE_DIR / 'data'
RESULTS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)

OIB = math.log(2) / (24 * math.pi)
L3 = 7
# Constants as already used in the project documents; these are structural constants,
# not fitted in this module.
BETA_CRYSTALLIZATION = 1.214377
R_CRIT = 1.5403
DELTA_INSTABILITY = 0.2118
CONFINEMENT_RESIDUAL_BUDGET = 0.21

v56_path = ROOT / '56_debt9_quark_confinement_triplet_boundary_v5_6' / 'results' / 'debt9_quark_confinement_triplet_boundary_v5_6.json'
v40_path = ROOT / '40_holonomic_gluon_wij_couplings_v4_0' / 'results' / 'holonomic_gluon_wij_v4_0.json'
v39_path = ROOT / '39_tetrahedral_triplet_su3_lift_v3_9' / 'results' / 'tetra_triplet_su3_lift_v3_9.json'

v56 = json.loads(v56_path.read_text(encoding='utf-8'))
v40 = json.loads(v40_path.read_text(encoding='utf-8'))
v39 = json.loads(v39_path.read_text(encoding='utf-8'))

quarks = {r['slot']: r for r in v56['quark_boundary_rows']}
qmass = {k: float(v['single_quark_prediction_mev_from_prior_probe']) for k,v in quarks.items()}

# Hadron benchmark values appear only after the operator/structural aggregator is defined.
# They are used to diagnose scale/binding dominance and never to set internal parameters.
benchmarks_scoring_only = {
    'proton': {'composition': ['u','u','d'], 'benchmark_mev': 938.272, 'family': 'baryon', 'source_role': 'post_freeze_scoring_only'},
    'neutron': {'composition': ['u','d','d'], 'benchmark_mev': 939.565, 'family': 'baryon', 'source_role': 'post_freeze_scoring_only'},
    'Lambda_uds': {'composition': ['u','d','s'], 'benchmark_mev': 1115.7, 'family': 'baryon', 'source_role': 'post_freeze_scoring_only'},
    'Sigma_uus': {'composition': ['u','u','s'], 'benchmark_mev': 1189.4, 'family': 'baryon', 'source_role': 'post_freeze_scoring_only'},
}

# Structural triplet kernel documented in the source text; mu_N scale is intentionally
# not assigned here because the source calibrated it to proton mass, which is not allowed
# for no-parameter closure.
triplet_binding_kernel_dimensionless = BETA_CRYSTALLIZATION * math.exp(R_CRIT) * (1.0 - DELTA_INSTABILITY/2.0)
loop = v40['loop_holonomy_validation']
holonomy_defect = float(loop['wilson_loop_defect_3_minus_ReTrU'])
curvature_norm = float(loop['curvature_proxy_frobenius_norm'])
active_modes = loop['active_gell_mann_modes_1_indexed']

# A dimensionless confinement action proxy, not a mass in MeV.
triplet_color_action = triplet_binding_kernel_dimensionless * (1.0 + holonomy_defect) * math.exp(-OIB * L3 * DELTA_INSTABILITY)
confinement_phase_budget = DELTA_INSTABILITY

rows = []
for name, h in benchmarks_scoring_only.items():
    comp = h['composition']
    pair_count = len(comp) * (len(comp)-1) // 2
    proxy_sum = sum(qmass[q] for q in comp)
    benchmark = h['benchmark_mev']
    quark_proxy_fraction_of_hadron = proxy_sum / benchmark
    binding_dominance_fraction = 1.0 - quark_proxy_fraction_of_hadron
    # This is a scale-free signature. It is not turned into a MeV prediction.
    flavor_instability_signature = sum(abs(quarks[q]['absolute_relative_residual']) for q in comp) / len(comp)
    needs_triplet_binding = quark_proxy_fraction_of_hadron < CONFINEMENT_RESIDUAL_BUDGET
    rows.append({
        'hadron': name,
        'family': h['family'],
        'composition': ''.join(comp),
        'composition_list': comp,
        'quark_proxy_sum_mev_from_v56': proxy_sum,
        'benchmark_mev_scoring_only': benchmark,
        'quark_proxy_fraction_of_hadron': quark_proxy_fraction_of_hadron,
        'binding_dominance_fraction': binding_dominance_fraction,
        'pair_count': pair_count,
        'tetrahedral_triplet_required': True,
        'W_ij_loop_required': True,
        'single_quark_mass_closure_allowed': False,
        'triplet_binding_kernel_dimensionless': triplet_binding_kernel_dimensionless,
        'holonomy_defect_from_v40': holonomy_defect,
        'curvature_norm_from_v40': curvature_norm,
        'active_gluon_modes_from_v40': active_modes,
        'triplet_color_action_dimensionless': triplet_color_action,
        'flavor_instability_signature_from_v56': flavor_instability_signature,
        'within_21_percent_single_proxy_budget': quark_proxy_fraction_of_hadron < CONFINEMENT_RESIDUAL_BUDGET,
        'diagnostic_status': 'BINDING_DOMINATED_TRIPLET_REQUIRED' if needs_triplet_binding else 'REVIEW_REQUIRED',
        'mass_prediction_mev_claimed': False,
        'numeric_debt9_closure_allowed': False,
    })

metrics = {
    'rows_count': len(rows),
    'mean_quark_proxy_fraction_of_hadron': sum(r['quark_proxy_fraction_of_hadron'] for r in rows)/len(rows),
    'max_quark_proxy_fraction_of_hadron': max(r['quark_proxy_fraction_of_hadron'] for r in rows),
    'all_rows_binding_dominated_under_21_percent_proxy_fraction': all(r['quark_proxy_fraction_of_hadron'] < CONFINEMENT_RESIDUAL_BUDGET for r in rows),
    'triplet_binding_kernel_dimensionless': triplet_binding_kernel_dimensionless,
    'triplet_color_action_dimensionless': triplet_color_action,
    'holonomic_loop_defect_v40': holonomy_defect,
    'curvature_norm_v40': curvature_norm,
}

source_taint_ledger = {
    'readme_hadron_geometric_mean_prescription': {
        'status': 'USE_AS_STRUCTURAL_HINT_ONLY',
        'reason': 'The README gives F_hadron geometric mean for hadron binding, which is structurally aligned with triplet aggregation but the numeric table exactly matches benchmarks; therefore it cannot close Debt 9.'
    },
    'readme_hadron_exact_table': {
        'status': 'TAINTED_EXACT_REFERENCE_REPLAY_OR_ANCHORED_TABLE',
        'examples': ['Proton predicted 938.3 vs benchmark 938.3', 'Neutron predicted 939.6 vs benchmark 939.6', 'Lambda predicted 1115.7 vs benchmark 1115.7'],
        'promotion_allowed': False
    },
    'metatheory_nucleon_mu0_scale': {
        'status': 'TAINTED_UNIT_ANCHOR',
        'reason': 'The source explicitly calibrates mu0_N to proton mass; it can document a hadron scale boundary but not a no-parameter prediction.'
    },
    'v40_Wij_holonomy': {
        'status': 'ACTIVE_STRUCTURAL_INPUT',
        'reason': 'W_ij loop defect/curvature is structural and PDG-free in module 40; used only as dimensionless action diagnostic.'
    },
    'v56_quark_single_proxy': {
        'status': 'DIAGNOSTIC_INPUT_NOT_CLOSURE',
        'reason': 'Single-quark proxies are non-asymptotic and cannot be exact mass closure criteria.'
    }
}

result = {
    'schema': 'METATIME_DEBT9_TRIPLET_HADRONIZATION_AGGREGATOR_V5_7',
    'module': '57_debt9_triplet_hadronization_aggregator_v5_7',
    'created_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'technical_status': 'PASS',
    'formal_status': 'PASS_WITH_HADRON_SOURCE_TAINT_LEDGER',
    'substantive_status': 'TRIPLET_HADRONIZATION_AGGREGATOR_INSTALLED_NUMERIC_CLOSURE_DENIED',
    'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
    'canon_allowed': False,
    'current_promotion': 'DENY_CURRENT',
    'mass_prediction_claimed': False,
    'user_correction_integrated': {
        'claim': 'Quarks are not lepton-like isolated states; they require triplet/hadron aggregation, with an approximately 21 percent confinement diagnostic budget before exact hadron-level tests.',
        'implemented_as': 'triplet W_ij hadronization structural aggregator plus source-taint ledger',
        'not_implemented_as': 'automatic acceptance of quark errors or replay of exact hadron tables'
    },
    'operator_definition': {
        'structural_path': 'tetrahedral triplet -> W_ij holonomic gluon links -> triplet binding kernel -> hadron aggregation boundary',
        'triplet_binding_kernel_dimensionless': 'beta * exp(Rcrit) * (1 - delta/2)',
        'triplet_color_action_dimensionless': 'triplet_binding_kernel * (1 + W_loop_defect) * exp(-OIB * L3 * delta)',
        'MeV_scale_assigned': False,
        'reason_no_MeV_scale': 'Available source calibrates hadron scale to proton mass; that is an anchor and cannot close Debt 9.'
    },
    'constants': {
        'OIB_ln2_over_24pi': OIB,
        'L3': L3,
        'beta_crystallization': BETA_CRYSTALLIZATION,
        'Rcrit': R_CRIT,
        'delta_instability': DELTA_INSTABILITY,
        'confinement_residual_budget': CONFINEMENT_RESIDUAL_BUDGET
    },
    'tetrahedral_triplet_source': {
        'module': '39_tetrahedral_triplet_su3_lift_v3_9',
        'edge_modes_independent': v39['tetrahedron']['edge_modes_independent'],
        'triplet_reading': v39['tetrahedron']['triplet_reading']
    },
    'W_ij_source': {
        'module': '40_holonomic_gluon_wij_couplings_v4_0',
        'loop_is_SU3': loop['U_loop_is_SU3'],
        'wilson_loop_defect': holonomy_defect,
        'curvature_proxy_frobenius_norm': curvature_norm,
        'active_gell_mann_modes_1_indexed': active_modes
    },
    'hadron_rows': rows,
    'metrics': metrics,
    'source_taint_ledger': source_taint_ledger,
    'decision': {
        'quark_single_state_exact_scoring': 'DENIED',
        'triplet_aggregation_required': True,
        'readme_exact_hadron_table_promotion': 'DENIED_AS_TAINTED',
        'hadron_scale_mu0_promotion': 'DENIED_AS_PROTON_ANCHOR',
        'debt9_quark_sector': 'OPEN_PENDING_DERIVED_HADRON_SCALE_AND_PAIRWISE_FLAVOR_WIJ',
        'debt9_total': 'OPEN_NOT_CLOSED'
    },
    'next_step': 'v5.8 should derive pairwise flavor W_ij/F_ij for quark pairs without exact hadron-table replay, or derive a hadronic MeV scale from non-mass constants before any baryon benchmark.',
}
# stable fingerprint excludes created timestamp
stable = {k:v for k,v in result.items() if k != 'created_utc'}
result['formula_fingerprint_sha256'] = hashlib.sha256(json.dumps(stable, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

(RESULTS / 'triplet_hadronization_aggregator_v5_7.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
with (RESULTS / 'triplet_hadronization_aggregator_v5_7.csv').open('w', newline='', encoding='utf-8') as f:
    fieldnames = ['hadron','family','composition','quark_proxy_sum_mev_from_v56','benchmark_mev_scoring_only','quark_proxy_fraction_of_hadron','binding_dominance_fraction','pair_count','triplet_binding_kernel_dimensionless','holonomy_defect_from_v40','triplet_color_action_dimensionless','diagnostic_status','mass_prediction_mev_claimed','numeric_debt9_closure_allowed']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow({k:r[k] for k in fieldnames})
(DATA / 'HADRON_SOURCE_TAINT_LEDGER_v5_7.json').write_text(json.dumps(source_taint_ledger, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(result, indent=2, ensure_ascii=False))
