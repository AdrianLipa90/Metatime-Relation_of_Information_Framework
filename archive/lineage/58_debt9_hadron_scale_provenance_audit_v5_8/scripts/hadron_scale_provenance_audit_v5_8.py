#!/usr/bin/env python3
"""
Module 58 / v5.8: Hadron scale provenance audit.

Purpose:
- Do not reject marginal hadron errors merely because they are small.
- Check whether small/exact hadron errors have independent non-mass provenance.
- Preserve structural F_hadron / triplet / W_ij path as useful if the scale derivation is incomplete.
"""
import json, math, hashlib, csv
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parents[1]
RESULTS = MODULE_DIR / 'results'
DATA = MODULE_DIR / 'data'
RESULTS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)

# Structural constants already used across the project.
OIB = math.log(2) / (24 * math.pi)
L3 = 7
BETA_CRYSTALLIZATION = 1.214377
R_CRIT = 1.5403
DELTA_INSTABILITY = 0.2118
CONFINEMENT_RESIDUAL_BUDGET = 0.21

v57_path = ROOT / '57_debt9_triplet_hadronization_aggregator_v5_7' / 'results' / 'triplet_hadronization_aggregator_v5_7.json'
v57 = json.loads(v57_path.read_text(encoding='utf-8'))
source_excerpts = json.loads((DATA / 'HADRON_SCALE_SOURCE_EXCERPTS_v5_8.json').read_text(encoding='utf-8'))

# Tables extracted from available documents. These are source-audit rows, not active operator inputs.
sm_m_theory_exact_rows = [
    {'hadron':'proton', 'composition':'uud', 'predicted_mev':938.3, 'benchmark_mev':938.3, 'source':'SM_and_M_Theory_generalisation', 'table_role':'exact_displayed_table'},
    {'hadron':'neutron', 'composition':'udd', 'predicted_mev':939.6, 'benchmark_mev':939.6, 'source':'SM_and_M_Theory_generalisation', 'table_role':'exact_displayed_table'},
    {'hadron':'Lambda', 'composition':'uds', 'predicted_mev':1115.7, 'benchmark_mev':1115.7, 'source':'SM_and_M_Theory_generalisation', 'table_role':'exact_displayed_table'},
    {'hadron':'Sigma_plus', 'composition':'uus', 'predicted_mev':1189.4, 'benchmark_mev':1189.4, 'source':'SM_and_M_Theory_generalisation', 'table_role':'exact_displayed_table'},
]
formal_sm_rows = [
    {'hadron':'proton', 'composition':'uud', 'quark_sum_mev':9.10, 'Ebind_mev':928.9, 'predicted_mev':938.0, 'benchmark_mev':938.3, 'source':'Formal_SM', 'table_role':'binding_table'},
    {'hadron':'neutron', 'composition':'udd', 'quark_sum_mev':11.6, 'Ebind_mev':927.4, 'predicted_mev':939.0, 'benchmark_mev':939.6, 'source':'Formal_SM', 'table_role':'binding_table'},
    {'hadron':'Lambda', 'composition':'uds', 'quark_sum_mev':102.9, 'Ebind_mev':832.1, 'predicted_mev':935.0, 'benchmark_mev':1115.7, 'source':'Formal_SM', 'table_role':'binding_table'},
    {'hadron':'Sigma_plus', 'composition':'uus', 'quark_sum_mev':100.4, 'Ebind_mev':1089.6, 'predicted_mev':1190.0, 'benchmark_mev':1189.4, 'source':'Formal_SM', 'table_role':'binding_table'},
    {'hadron':'Sigma_zero', 'composition':'uds', 'quark_sum_mev':102.9, 'Ebind_mev':1087.1, 'predicted_mev':1190.0, 'benchmark_mev':1192.6, 'source':'Formal_SM', 'table_role':'binding_table'},
    {'hadron':'Xi_zero', 'composition':'uss', 'quark_sum_mev':194.2, 'Ebind_mev':1221.8, 'predicted_mev':1316.0, 'benchmark_mev':1314.9, 'source':'Formal_SM', 'table_role':'binding_table'},
]
calabi_yau2_rows = [
    {'hadron':'proton', 'composition':'uud', 'quark_sum_mev':100.8, 'Ebind_mev':8.0, 'predicted_mev':108.8, 'source':'Calabi_Yau2', 'table_role':'underbound_binding_table'},
    {'hadron':'neutron', 'composition':'udd', 'quark_sum_mev':101.8, 'Ebind_mev':8.2, 'predicted_mev':110.0, 'source':'Calabi_Yau2', 'table_role':'underbound_binding_table'},
    {'hadron':'Lambda', 'composition':'uds', 'quark_sum_mev':102.8, 'Ebind_mev':8.5, 'predicted_mev':111.3, 'source':'Calabi_Yau2', 'table_role':'underbound_binding_table'},
]

# Compute display-level exactness and evidence classes.
def relerr(pred, ref):
    return abs(pred-ref)/ref if ref else None

def classify_row(row):
    out = dict(row)
    if 'benchmark_mev' in out:
        out['absolute_relative_error'] = relerr(out['predicted_mev'], out['benchmark_mev'])
        out['display_exact_to_source_precision'] = (abs(out['predicted_mev'] - out['benchmark_mev']) < 1e-12)
    else:
        out['absolute_relative_error'] = None
        out['display_exact_to_source_precision'] = False
    if out['source'] == 'SM_and_M_Theory_generalisation':
        out['provenance_status'] = 'EXACT_TABLE_REQUIRES_EXECUTABLE_SCALE_PROVENANCE'
        out['promotion_to_debt9_closure'] = False
        out['reason'] = 'The table is exactly equal to benchmarks to displayed precision; this may be real, but requires executable non-mass scale derivation before promotion.'
    elif out['source'] == 'Formal_SM':
        out['provenance_status'] = 'MIXED_BINDING_TABLE_STRUCTURAL_HINT_NOT_CLOSURE'
        out['promotion_to_debt9_closure'] = False
        out['reason'] = 'Contains binding-energy decomposition, but Ebind is tabular and Lambda residual shows missing dynamics.'
    else:
        out['provenance_status'] = 'UNDERBOUND_OR_CALIBRATION_WARNING_STRUCTURAL_HINT'
        out['promotion_to_debt9_closure'] = False
        out['reason'] = 'Shows that small 5-50 MeV binding alone misses nucleon scale; source also mentions calibration/iteration.'
    return out

source_rows = [classify_row(r) for r in sm_m_theory_exact_rows + formal_sm_rows + calabi_yau2_rows]

# Perfect-number / sigma route: keep as structural candidate only.
prime_product_candidate = {
    'route': 'prime_product_sigma_R_harmonic_correction',
    'proton_assignment': {'u':3, 'd':5, 'n_proton':45, 'sigma_45':78, 'R_45':78/45},
    'status': 'STRUCTURAL_CANDIDATE_NOT_SCALE_CLOSURE',
    'reason': 'The source acknowledges mismatch and says harmonic corrections L(n) are required; no final MeV map is present in the checked source layer.'
}

scale_provenance_tests = {
    'non_mass_hadron_MeV_scale_found': False,
    'executable_formula_from_constants_to_baryon_MeV_found': False,
    'exact_table_rejected_because_small_error': False,
    'exact_table_blocked_reason': 'not small error; missing executable provenance and likely anchor/replay risk',
    'structural_paths_preserved': [
        'F_hadron geometric mean over quark-pair F_ij',
        'triplet W_ij holonomic aggregation',
        'prime product sigma/R(n) baryon path',
        'standing-wave/knot binding picture',
        'confinement residual budget around delta ~= 0.2118'
    ]
}

metrics = {
    'sm_m_theory_exact_rows': len(sm_m_theory_exact_rows),
    'sm_m_theory_all_display_exact': all(r['display_exact_to_source_precision'] for r in [classify_row(x) for x in sm_m_theory_exact_rows]),
    'formal_sm_rows': len(formal_sm_rows),
    'formal_sm_median_abs_rel_error': sorted([r['absolute_relative_error'] for r in [classify_row(x) for x in formal_sm_rows]])[len(formal_sm_rows)//2],
    'formal_sm_lambda_abs_rel_error': [r for r in [classify_row(x) for x in formal_sm_rows] if r['hadron']=='Lambda'][0]['absolute_relative_error'],
    'v57_all_rows_binding_dominated_under_21_percent_proxy_fraction': v57['metrics']['all_rows_binding_dominated_under_21_percent_proxy_fraction'],
    'v57_mean_quark_proxy_fraction_of_hadron': v57['metrics']['mean_quark_proxy_fraction_of_hadron'],
}

result = {
    'schema': 'METATIME_DEBT9_HADRON_SCALE_PROVENANCE_AUDIT_V5_8',
    'module': '58_debt9_hadron_scale_provenance_audit_v5_8',
    'created_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'technical_status': 'PASS',
    'formal_status': 'PASS_WITH_STRONGER_PROVENANCE_DISTINCTION',
    'substantive_status': 'HADRON_TABLE_NOT_REJECTED_FOR_SMALL_ERROR_BUT_NOT_PROMOTED_WITHOUT_SCALE_PROVENANCE',
    'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
    'canon_allowed': False,
    'current_promotion': 'DENY_CURRENT',
    'mass_prediction_claimed': False,
    'user_correction_integrated': {
        'correction': 'Do not reject marginal hadron errors merely because they are marginal; check whether the table is independently derived.',
        'implemented_as': 'hadron scale provenance audit distinguishing small-error evidence from replay/anchor risk',
        'result': 'small errors are allowed in principle; exact table remains unpromoted because the checked sources do not expose executable non-mass scale derivation.'
    },
    'constants': {
        'OIB_ln2_over_24pi': OIB,
        'L3': L3,
        'beta_crystallization': BETA_CRYSTALLIZATION,
        'Rcrit': R_CRIT,
        'delta_instability': DELTA_INSTABILITY,
        'confinement_residual_budget': CONFINEMENT_RESIDUAL_BUDGET
    },
    'source_excerpts_ledger': source_excerpts,
    'source_rows': source_rows,
    'prime_product_candidate': prime_product_candidate,
    'scale_provenance_tests': scale_provenance_tests,
    'v57_context': {
        'triplet_aggregation_required': True,
        'mean_quark_proxy_fraction_of_hadron': v57['metrics']['mean_quark_proxy_fraction_of_hadron'],
        'all_checked_rows_under_21_percent_single_proxy_budget': v57['metrics']['all_rows_binding_dominated_under_21_percent_proxy_fraction']
    },
    'metrics': metrics,
    'decision': {
        'small_errors_as_such': 'NOT_A_REASON_FOR_REJECTION',
        'SM_and_M_Theory_exact_table': 'HOLD_AS_PROVENANCE_REQUIRED_NOT_DEBT9_CLOSURE',
        'Formal_SM_binding_table': 'USE_AS_MIXED_DIAGNOSTIC_SOURCE_NOT_CLOSURE',
        'Calabi_Yau2_binding_table': 'USE_AS_UNDERBOUND_WARNING_AND_CALIBRATION_TAINT_SOURCE',
        'F_hadron_geometric_mean': 'PRESERVE_AS_STRUCTURAL_OPERATOR_CANDIDATE',
        'prime_product_sigma_route': 'PRESERVE_AS_CLEAN_NEXT_DERIVATION_ROUTE',
        'hadron_MeV_scale': 'NOT_YET_DERIVED_FROM_NON_MASS_CONSTANTS',
        'debt9_total': 'OPEN_NOT_CLOSED'
    },
    'next_step': 'v5.9 should derive a hadron scale candidate from prime-product sigma/R(n), harmonic L(n), triplet W_ij, and OIB/Ramanujan constants before any baryon benchmark. Exact source tables must remain scoring-only until that derivation exists.'
}
stable = {k:v for k,v in result.items() if k != 'created_utc'}
result['formula_fingerprint_sha256'] = hashlib.sha256(json.dumps(stable, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

(RESULTS / 'hadron_scale_provenance_audit_v5_8.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
with (RESULTS / 'hadron_scale_provenance_audit_v5_8.csv').open('w', newline='', encoding='utf-8') as f:
    fields = ['source','table_role','hadron','composition','predicted_mev','benchmark_mev','absolute_relative_error','display_exact_to_source_precision','provenance_status','promotion_to_debt9_closure']
    w=csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in source_rows:
        row={k:r.get(k,'') for k in fields}
        w.writerow(row)
print(json.dumps(result, indent=2, ensure_ascii=False))
