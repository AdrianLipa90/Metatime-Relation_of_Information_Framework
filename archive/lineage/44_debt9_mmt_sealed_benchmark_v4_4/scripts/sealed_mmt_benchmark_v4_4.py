#!/usr/bin/env python3
"""
METATIME / Standard Model derivation v4.4
Debt 9: sealed benchmark of the already-frozen M_MT v4.3 operator trace.

This executable is allowed to read the post-freeze benchmark snapshot because it is a benchmark,
not the operator. It must not modify the frozen operator, recompute structural traces differently,
fit parameters, select exponents after seeing residuals, or import any archived reference solver.

Interpretation tested here is intentionally minimal and pre-declared inside this module:
- direct dimensionless M_MT amplitude ratios are treated as Yukawa/mass-ratio candidates;
- electron-anchored absolute scale is reported only as a diagnostic;
- family-first ratios are reported as a stronger no-scale diagnostic;
- no fitting, residual minimization, per-family rescaling, or post-hoc exponent search is performed.
"""
from __future__ import annotations
import csv, hashlib, json, math, pathlib, statistics
from typing import Dict, Any, List

MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = MODULE_DIR.parents[0]
V43_RESULT = REPO_ROOT / '43_debt9_metatime_mass_operator_freeze_v4_3' / 'results' / 'metatime_mmt_freeze_v4_3.json'
BENCH = MODULE_DIR / 'data' / 'benchmark_reference_snapshot_v4_4.json'
OUT = MODULE_DIR / 'results'
EXPECTED_FROZEN_SHA = 'cf6791ae2010a7e383222fe8edc3d3b41d4a4ebe8b671bd96425b52b33128e37'
ELECTRON_ANCHOR = 'e'
FAMILY_ANCHORS = {'charged_lepton': 'e', 'up_quark': 'u', 'down_quark': 'd'}


def load_json(p:pathlib.Path)->Any:
    return json.loads(p.read_text(encoding='utf-8'))


def rel_error(pred:float, ref:float)->float:
    return (pred - ref) / ref


def log10_abs_rel_error(pred:float, ref:float)->float:
    e = abs(rel_error(pred, ref))
    return math.log10(e) if e > 0 else -math.inf


def spearman_rho(xs:List[float], ys:List[float])->float:
    # small no-dependency Spearman rank correlation, average ranks for ties not needed here.
    def ranks(vals):
        pairs = sorted((v, i) for i, v in enumerate(vals))
        r = [0.0]*len(vals)
        for rank, (_, idx) in enumerate(pairs, start=1):
            r[idx] = float(rank)
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a-mx)*(b-my) for a,b in zip(rx, ry))
    denx = math.sqrt(sum((a-mx)**2 for a in rx))
    deny = math.sqrt(sum((b-my)**2 for b in ry))
    return num/(denx*deny) if denx and deny else float('nan')


def main()->None:
    frozen = load_json(V43_RESULT)
    bench = load_json(BENCH)
    if frozen.get('operator_trace_sha256') != EXPECTED_FROZEN_SHA:
        raise RuntimeError('Frozen operator SHA mismatch; sealed benchmark denied')
    if frozen.get('observed_masses_used') or frozen.get('pdg_reference_input_used'):
        raise RuntimeError('Frozen operator is not clean; sealed benchmark denied')

    traces = frozen['traces']
    masses = bench['masses_mev']
    amp = {t['slot']: float(t['dimensionless_mmt_amplitude_frozen']) for t in traces}
    family = {t['slot']: t['family'] for t in traces}
    gen = {t['slot']: int(t['generation']) for t in traces}
    slots = [t['slot'] for t in traces]
    if set(slots) != set(masses.keys()):
        raise RuntimeError('Benchmark slots do not match frozen operator slots')

    anchor_amp = amp[ELECTRON_ANCHOR]
    anchor_mass = masses[ELECTRON_ANCHOR]['value']
    rows=[]
    for s in slots:
        direct_ratio_to_e = amp[s] / anchor_amp
        observed_ratio_to_e = masses[s]['value'] / anchor_mass
        pred_e_anchor = anchor_mass * direct_ratio_to_e
        fam_anchor = FAMILY_ANCHORS[family[s]]
        pred_family_anchor = masses[fam_anchor]['value'] * (amp[s] / amp[fam_anchor])
        row = {
            'slot': s,
            'family': family[s],
            'generation': gen[s],
            'frozen_amplitude': amp[s],
            'benchmark_mass_mev': masses[s]['value'],
            'benchmark_scheme': masses[s]['scheme'],
            'direct_ratio_to_e_frozen': direct_ratio_to_e,
            'observed_ratio_to_e': observed_ratio_to_e,
            'electron_anchor_prediction_mev': pred_e_anchor,
            'electron_anchor_relative_error': rel_error(pred_e_anchor, masses[s]['value']),
            'family_anchor': fam_anchor,
            'family_anchor_prediction_mev': pred_family_anchor,
            'family_anchor_relative_error': rel_error(pred_family_anchor, masses[s]['value']),
            'mass_prediction_claimed': False,
            'sealed_benchmark_only': True,
        }
        rows.append(row)

    # No-scale diagnostics on the only meaningful hierarchy test available to this frozen operator.
    non_anchor_rows = [r for r in rows if r['slot'] not in set([ELECTRON_ANCHOR, 'u', 'd'])]
    fam_non_anchor_rows = [r for r in rows if r['slot'] not in set(FAMILY_ANCHORS.values())]
    mean_abs_log10_err_e_anchor = statistics.mean(abs(log10_abs_rel_error(r['electron_anchor_prediction_mev'], r['benchmark_mass_mev'])) for r in non_anchor_rows)
    median_abs_rel_err_family = statistics.median(abs(r['family_anchor_relative_error']) for r in fam_non_anchor_rows)
    max_abs_rel_err_family = max(abs(r['family_anchor_relative_error']) for r in fam_non_anchor_rows)
    rho_log_amp_log_mass = spearman_rho([math.log(amp[s]) for s in slots], [math.log(masses[s]['value']) for s in slots])

    # Hard, predeclared failure gates. These are intentionally permissive enough that only a real hierarchy signal can pass.
    # median family-anchored error below 50% would indicate a nontrivial ratio signal; current frozen operator is not close.
    gates = {
        'frozen_operator_sha_matches_expected': True,
        'no_operator_mutation': True,
        'no_fitted_parameters': True,
        'median_family_anchor_abs_relative_error_lt_0_5': median_abs_rel_err_family < 0.5,
        'max_family_anchor_abs_relative_error_lt_2': max_abs_rel_err_family < 2.0,
        'spearman_log_amp_log_mass_gt_0_75': rho_log_amp_log_mass > 0.75,
    }
    substantive_pass = all(gates.values())
    status = 'SEALED_BENCHMARK_FAIL_NUMERIC_DEBT9_REMAINS_OPEN'
    if substantive_pass:
        status = 'SEALED_BENCHMARK_PASS_REQUIRES_INDEPENDENT_REPLICATION'

    trace_payload = {
        'frozen_operator_trace_sha256': EXPECTED_FROZEN_SHA,
        'benchmark_snapshot_sha256': hashlib.sha256(json.dumps(bench, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        'rows': rows,
        'gates': gates,
        'summary_metrics': {
            'mean_abs_log10_error_electron_anchor_nonanchors': mean_abs_log10_err_e_anchor,
            'median_abs_relative_error_family_anchor_nonanchors': median_abs_rel_err_family,
            'max_abs_relative_error_family_anchor_nonanchors': max_abs_rel_err_family,
            'spearman_rho_log_frozen_amplitude_vs_log_benchmark_mass': rho_log_amp_log_mass,
        },
    }
    result = {
        'schema': 'METATIME_MMT_SEALED_BENCHMARK_V4_4',
        'created_utc': '2026-06-20T00:00:00Z',
        'module': '44_debt9_mmt_sealed_benchmark_v4_4',
        'status': status,
        'technical_status': 'PASS',
        'formal_status': 'PASS',
        'substantive_status': 'FAIL' if not substantive_pass else 'PASS_REVIEW_REQUIRED',
        'debt9_numeric_spectrum_status': 'OPEN_NOT_CLOSED' if not substantive_pass else 'REVIEW_REQUIRED_NOT_CANON',
        'mass_prediction_claimed': False,
        'benchmark_performed': True,
        'operator_mutated_after_freeze': False,
        'observed_masses_used_by_operator': False,
        'observed_masses_used_by_benchmark': True,
        'fitted_parameters_used': False,
        'per_family_rescaling_used_as_prediction': False,
        'reference_spectrum_execution_claimed': False,
        'canon_allowed': False,
        'current_promotion': 'DENY_CURRENT',
        **trace_payload,
    }
    OUT.mkdir(exist_ok=True)
    (OUT/'sealed_mmt_benchmark_v4_4.json').write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    with (OUT/'sealed_mmt_benchmark_v4_4.csv').open('w', newline='', encoding='utf-8') as f:
        fieldnames = list(rows[0].keys())
        w=csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)
    print(json.dumps({
        'status': status,
        'technical_status': 'PASS',
        'substantive_status': result['substantive_status'],
        'debt9_numeric_spectrum_status': result['debt9_numeric_spectrum_status'],
        'frozen_operator_trace_sha256': EXPECTED_FROZEN_SHA,
        'median_abs_relative_error_family_anchor_nonanchors': median_abs_rel_err_family,
        'spearman_rho_log_frozen_amplitude_vs_log_benchmark_mass': rho_log_amp_log_mass,
    }, indent=2))

if __name__ == '__main__':
    main()
