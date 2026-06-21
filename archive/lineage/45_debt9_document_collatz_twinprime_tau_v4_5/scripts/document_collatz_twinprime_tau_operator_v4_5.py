#!/usr/bin/env python3
"""
METATIME / Standard Model derivation v4.5
Debt 9 document-derived Collatz/twin-prime tau operator trace.

This executable uses only document-declared arithmetic/topological calculations:
- twin-prime pairs and center seed p+1;
- family Collatz map metadata;
- document tau/eigenvalue table;
- L3 = ordinary Collatz stopping length of 3;
- information quantum ln(2)/(24*pi);
- Ramanujan-theta residue diagnostic from valuation words.

It deliberately does not import archived mass solvers, observed mass tables, reference spectra,
or coefficients fitted from masses. Any document formula that used observed masses is recorded
only in a taint ledger and not used by the active operator trace.
"""
from __future__ import annotations
import csv, hashlib, json, math, pathlib
from typing import Dict, List, Any, Tuple

MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
OUT = MODULE_DIR / 'results'
LEDGER = MODULE_DIR / 'data' / 'DOCUMENT_SOURCE_LEDGER_v4_5.json'

# Document-declared seeds and tau/eigenvalues from Formal_SM and framework summary.
FAMILIES = {
    'leptons':      {'pair': (3, 5),     'center_seed': 4,   'eta': 1.1, 'threshold': 4.4,   'slots': ['e','mu','tau']},
    'neutrinos':    {'pair': (5, 7),     'center_seed': 6,   'eta': 1.1, 'threshold': 6.6,   'slots': ['nu1','nu2','nu3']},
    'light_quarks': {'pair': (11, 13),   'center_seed': 12,  'eta': 1.0, 'threshold': 12.0,  'slots': ['u','d','s']},
    'heavy_quarks': {'pair': (101, 103), 'center_seed': 102, 'eta': 1.0, 'threshold': 102.0, 'slots': ['c','b','t']},
}
SLOTS = {
    'e':   {'family':'leptons','generation':1,'tau_doc':4.0,   'doc_origin':'terminal_center_seed_from_(3,5): 4 -> 2 -> 1', 'origin_class':'clean_document_seed'},
    'mu':  {'family':'leptons','generation':2,'tau_doc':1.0,   'doc_origin':'fixed point / minimal cycle', 'origin_class':'clean_document_fixed_point'},
    'tau': {'family':'leptons','generation':3,'tau_doc':10.0,  'doc_origin':'document says seed/eigenvalue 10; label conflicts with (11,13) center 12', 'origin_class':'document_inconsistency_review'},
    'nu1': {'family':'neutrinos','generation':1,'tau_doc':0.02, 'doc_origin':'sub-threshold minimal', 'origin_class':'document_subthreshold'},
    'nu2': {'family':'neutrinos','generation':2,'tau_doc':0.05, 'doc_origin':'sub-threshold minimal', 'origin_class':'document_subthreshold'},
    'nu3': {'family':'neutrinos','generation':3,'tau_doc':0.10, 'doc_origin':'sub-threshold minimal', 'origin_class':'document_subthreshold'},
    'u':   {'family':'light_quarks','generation':1,'tau_doc':0.05, 'doc_origin':'sub-threshold minimal', 'origin_class':'document_subthreshold'},
    'd':   {'family':'light_quarks','generation':2,'tau_doc':0.10, 'doc_origin':'sub-threshold minimal', 'origin_class':'document_subthreshold'},
    's':   {'family':'light_quarks','generation':3,'tau_doc':0.40, 'doc_origin':'sub-threshold minimal', 'origin_class':'document_subthreshold'},
    'c':   {'family':'heavy_quarks','generation':1,'tau_doc':5.0,  'doc_origin':'document labels power-law anchor', 'origin_class':'tainted_power_law_anchor'},
    'b':   {'family':'heavy_quarks','generation':2,'tau_doc':10.0, 'doc_origin':'document labels power-law anchor', 'origin_class':'tainted_power_law_anchor'},
    't':   {'family':'heavy_quarks','generation':3,'tau_doc':100.0,'doc_origin':'document labels power-law anchor', 'origin_class':'tainted_power_law_anchor'},
}

# Canonical document constants.
INFO_QUANTUM = math.log(2.0)/(24.0*math.pi)
LEGACY_I0_APPROX = 0.009
PHI = (1.0 + math.sqrt(5.0))/2.0
L3_EXPECTED = 7


def collatz_orbit(n:int, max_steps:int=10000)->List[int]:
    if n < 1: raise ValueError('n must be positive')
    x=n; out=[x]
    for _ in range(max_steps):
        if x == 1: break
        x = x//2 if x % 2 == 0 else 3*x + 1
        out.append(x)
    return out


def ordinary_stopping_length(n:int)->int:
    o = collatz_orbit(n)
    return len(o)-1


def v2(n:int)->int:
    if n == 0: return 0
    c=0
    while n % 2 == 0:
        c += 1; n//=2
    return c


def accelerated_odd_valuation_word(seed:int, max_odd_steps:int=24)->List[int]:
    # For odd seed: word of 2-adic valuations of 3m+1 under accelerated odd map.
    if seed % 2 == 0:
        # reduce to odd carrier first: this is a diagnostic bridge, not a proof step.
        while seed % 2 == 0 and seed > 1:
            seed//=2
    if seed < 1: return []
    m = seed
    word=[]
    seen=set()
    for _ in range(max_odd_steps):
        if m == 1 or m in seen: break
        seen.add(m)
        a = v2(3*m + 1)
        word.append(a)
        m = (3*m + 1) // (2**a)
        if m % 2 == 0:
            while m % 2 == 0 and m > 1:
                m//=2
    return word


def ramanujan_theta_residue(word:List[int], t:float=1.0/L3_EXPECTED)->Dict[str,float]:
    # Step 7 diagnostic: delta_k = B_k - k log_2 3; K_t = exp(-2*pi*t*delta_k^2).
    k=len(word)
    B=sum(word)
    delta = B - k*math.log2(3.0)
    log_weight = -2.0*math.pi*t*delta*delta
    weight = math.exp(log_weight) if log_weight > -700 else 0.0
    return {'k':float(k), 'B':float(B), 'delta':delta, 'theta_weight':weight, 'log_theta_weight':log_weight, 'log10_theta_weight':log_weight/math.log(10.0)}


def twin_prime_complementarity(pair:Tuple[int,int])->Dict[str,Any]:
    p,q=pair
    ap=v2(3*p+1)
    bp=v2(3*q+1)
    if p == 3 and q == 5:
        status = 'BASE_PAIR_SPECIAL_CASE_INCLUDED_BY_L3_AXIS'
    else:
        status = 'PASS' if min(ap,bp)==1 and max(ap,bp)>=2 else 'FAIL'
    return {'pair':[p,q], 'a_p':ap, 'b_p':bp, 'status':status}


def document_tau_driver(slot:str, tau_doc:float, generation:int, family:str)->Dict[str,float]:
    # This is a dimensionless trace, not a mass prediction. It uses no observed masses.
    # It intentionally exposes several candidate coordinates for v4.6 selection/freeze.
    fam = FAMILIES[family]
    center = fam['center_seed']
    L3 = ordinary_stopping_length(3)
    orbit_len_center = ordinary_stopping_length(center)
    word = accelerated_odd_valuation_word(center)
    theta = ramanujan_theta_residue(word)
    gen_phase = generation / L3
    terminal_norm = 0.5  # from terminal projective endpoint 4->2->1->1/2.
    info_phase = INFO_QUANTUM * (orbit_len_center + generation)
    # Three frozen coordinates. v4.5 does NOT choose one as mass formula.
    tau_depth_coordinate = math.log1p(tau_doc) / L3
    collatz_center_coordinate = orbit_len_center / L3
    log_release = info_phase + theta['log_theta_weight'] + math.log(1.0 + terminal_norm*gen_phase)
    holonomy_release_coordinate = math.exp(log_release) if log_release > -700 else 0.0
    # A composite trace for fingerprinting; not benchmarked here. Store log version to avoid losing heavy-sector information to underflow.
    composite_log = math.log(max(tau_depth_coordinate, 1e-300)) + log_release + math.log(1.0 + collatz_center_coordinate)
    composite = math.exp(composite_log) if composite_log > -700 else 0.0
    return {
        'L3': float(L3),
        'center_seed': float(center),
        'center_orbit_length': float(orbit_len_center),
        'tau_depth_coordinate': tau_depth_coordinate,
        'collatz_center_coordinate': collatz_center_coordinate,
        'ramanujan_delta': theta['delta'],
        'ramanujan_theta_weight': theta['theta_weight'],
        'ramanujan_log_theta_weight': theta['log_theta_weight'],
        'ramanujan_log10_theta_weight': theta['log10_theta_weight'],
        'information_phase': info_phase,
        'holonomy_release_log_coordinate': log_release,
        'holonomy_release_coordinate': holonomy_release_coordinate,
        'composite_document_tau_trace_log': composite_log,
        'composite_document_tau_trace': composite,
    }


def main()->None:
    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    L3 = ordinary_stopping_length(3)
    if L3 != L3_EXPECTED:
        raise RuntimeError(f'L3 mismatch: got {L3}, expected {L3_EXPECTED}')

    family_checks=[]
    for fam, meta in FAMILIES.items():
        family_checks.append({
            'family': fam,
            'pair': list(meta['pair']),
            'center_seed_p_plus_1': meta['center_seed'],
            'eta': meta['eta'],
            'threshold': meta['threshold'],
            'center_collatz_orbit': collatz_orbit(meta['center_seed']),
            'center_orbit_length_to_1': ordinary_stopping_length(meta['center_seed']),
            'twin_prime_complementarity': twin_prime_complementarity(meta['pair']),
        })

    rows=[]
    for slot, s in SLOTS.items():
        coords = document_tau_driver(slot, s['tau_doc'], s['generation'], s['family'])
        row = {
            'slot': slot,
            'family': s['family'],
            'generation': s['generation'],
            'tau_doc': s['tau_doc'],
            'doc_origin': s['doc_origin'],
            'origin_class': s['origin_class'],
            **coords,
            'mass_prediction_claimed': False,
            'benchmark_performed': False,
            'observed_mass_input_used': False,
            'pdg_reference_input_used': False,
        }
        rows.append(row)

    # Separate ledger for document calculations that are useful historically but not allowed as clean closure.
    tainted_document_mass_calculations = [
        {'name':'charged_lepton_quadratic_vandermonde','document':'Formal_SM.pdf §3.1','reason':'exactly fit to three charged-lepton mass anchors', 'allowed_use':'historical clue only; not Debt 9 closure'},
        {'name':'heavy_quark_log_ols_power_law','document':'Formal_SM.pdf §3.2','reason':'OLS fit using c,b,t benchmark masses', 'allowed_use':'historical clue only; not Debt 9 closure'},
        {'name':'light_quark_required_Fi','document':'Formal_SM.pdf §3.3','reason':'correction factors computed as benchmark/model ratios', 'allowed_use':'do not import as prediction'},
        {'name':'neutrino_global_scale_s','document':'Formal_SM.pdf §5.2','reason':'calibration scale fixed by observed atmospheric splitting', 'allowed_use':'benchmark/calibration layer only'},
    ]

    payload = {
        'schema':'METATIME_DOCUMENT_COLLATZ_TWINPRIME_TAU_OPERATOR_TRACE_V4_5',
        'created_utc':'2026-06-20T00:00:00Z',
        'module':'45_debt9_document_collatz_twinprime_tau_v4_5',
        'status':'PASS_OPERATOR_TRACE_FROZEN_NOT_BENCHMARKED',
        'technical_status':'PASS',
        'formal_status':'PASS_WITH_SOURCE_TAINT_LEDGER',
        'substantive_status':'DOCUMENT_DERIVED_OPERATOR_TRACE_CREATED_NUMERIC_DEBT9_STILL_OPEN',
        'L3_base_collatz_length_of_3': L3,
        'collatz_orbit_3': collatz_orbit(3),
        'terminal_fragment':'4 -> 2 -> 1 -> 1/2 projective endpoint',
        'information_quantum_ln2_over_24pi': INFO_QUANTUM,
        'legacy_I0_approx': LEGACY_I0_APPROX,
        'relative_difference_info_quantum_vs_legacy_I0': (INFO_QUANTUM-LEGACY_I0_APPROX)/LEGACY_I0_APPROX,
        'phi': PHI,
        'family_checks': family_checks,
        'rows': rows,
        'tainted_document_mass_calculations': tainted_document_mass_calculations,
        'operator_policy': ledger['use_policy'],
        'mass_prediction_claimed': False,
        'benchmark_performed': False,
        'canon_allowed': False,
        'current_promotion':'DENY_CURRENT',
        'debt9_numeric_spectrum_status':'OPEN_PENDING_V4_6_SEALED_BENCHMARK_OR_FORMULA_SELECTION',
    }
    # Fingerprint only the frozen, benchmark-free operator trace rows and constants.
    fp_material = {
        'L3':L3,
        'INFO_QUANTUM':INFO_QUANTUM,
        'FAMILIES':FAMILIES,
        'SLOTS':SLOTS,
        'rows_no_mass':rows,
    }
    payload['operator_trace_sha256'] = hashlib.sha256(json.dumps(fp_material, sort_keys=True, separators=(',',':')).encode()).hexdigest()

    OUT.mkdir(exist_ok=True)
    (OUT/'document_collatz_twinprime_tau_trace_v4_5.json').write_text(json.dumps(payload, indent=2, sort_keys=True), encoding='utf-8')
    with (OUT/'document_collatz_twinprime_tau_trace_v4_5.csv').open('w', newline='', encoding='utf-8') as f:
        fieldnames=list(rows[0].keys())
        w=csv.DictWriter(f, fieldnames=fieldnames); w.writeheader(); w.writerows(rows)
    print(json.dumps({'status':payload['status'], 'trace_sha256':payload['operator_trace_sha256'], 'L3':L3, 'info_quantum':INFO_QUANTUM}, indent=2))

if __name__ == '__main__':
    main()
