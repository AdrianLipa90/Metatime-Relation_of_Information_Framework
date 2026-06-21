#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math, statistics
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
OUT = MODULE / 'results'
ORDER = ['e','mu','tau']
KAPPA = math.log(2.0)/(24.0*math.pi)

def load_json(p: Path):
    with p.open(encoding='utf-8') as f: return json.load(f)

def read_csv(p: Path):
    with p.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))

def write_csv(p: Path, rows):
    if not rows:
        p.write_text('', encoding='utf-8'); return
    with p.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def sha_obj(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()

def main():
    v52 = load_json(ROOT/'52_debt9_sealed_charged_lepton_kernel_benchmark_v5_2'/'results'/'sealed_charged_lepton_kernel_benchmark_v5_2.json')
    tau_rows = read_csv(ROOT/'27_debt9_tau_v2_clean_information_eigenvalue_v2_9'/'results'/'tau_v2_structural_information_eigenvalue_table_v2_9.csv')
    ram_rows = {r['fermion']: r for r in tau_rows if r['class']=='charged_lepton'}

    e_action = float(ram_rows['e']['ramanujan_scaled_action'])
    e_visibility = float(ram_rows['e']['ramanujan_visibility'])
    e_generation = int(ram_rows['e']['generation'])

    frozen_formula = {
        'name': 'RamanujanOIPathNormalizer_v5_3',
        'role': 'root-relative charged-lepton generation normalizer applied to the already sealed v5.2 kernel',
        'source': {
            'ramanujan_layer': 'v2.1/v2.9 seed suppression and tau_v2 table',
            'information_operator': 'OIB = ln2/(24*pi), used as the quantum of informational preference fluctuation',
            'path_rule': 'spinor half-action divided by generation-path duration from e to target',
        },
        'formula': {
            'ramanujan_visibility': 'V_i = exp(-A_R_i/OIB)',
            'path_normalizer': 'R_ei = exp(-(A_R_i - A_R_e)/(2*OIB*DeltaGeneration)) = (V_i/V_e)^(1/(2*DeltaGeneration))',
            'mass_diagnostic': 'm_i(v5.3) = m_i(v5.2 sealed) * R_ei; m_e unchanged',
        },
        'boundaries': {
            'post_v5_2_correction': True,
            'new_free_parameter_added': False,
            'observed_masses_used_in_operator': False,
            'benchmark_targets_used_only_after_fingerprint': True,
            'closure_claimed': False,
        }
    }

    # Pre-benchmark payload deliberately excludes benchmark targets and residuals.
    pre_rows = []
    v52_rows = {r['slot']: r for r in v52['rows']}
    for slot in ORDER:
        dg = max(0, int(ram_rows[slot]['generation']) - e_generation)
        if slot == 'e':
            R = 1.0
        else:
            a = float(ram_rows[slot]['ramanujan_scaled_action'])
            R = math.exp(-(a - e_action)/(2.0*KAPPA*dg))
        pre_rows.append({
            'slot': slot,
            'generation': int(ram_rows[slot]['generation']),
            'ramanujan_scaled_action': float(ram_rows[slot]['ramanujan_scaled_action']),
            'ramanujan_visibility': float(ram_rows[slot]['ramanujan_visibility']),
            'delta_generation_from_e': dg,
            'OIB_ln2_over_24pi': KAPPA,
            'ramanujan_oi_path_normalizer': R,
            'v5_2_sealed_prediction_input_mev': float(v52_rows[slot]['predicted_mev_sealed_formula']),
        })
    fingerprint = sha_obj({'formula': frozen_formula, 'pre_benchmark_rows': pre_rows})

    rows=[]; errs_no_e=[]
    for pr in pre_rows:
        slot=pr['slot']
        pred = pr['v5_2_sealed_prediction_input_mev'] * pr['ramanujan_oi_path_normalizer']
        benchmark = float(v52_rows[slot]['benchmark_mev_post_freeze_scoring_only'])
        ratio = pred / benchmark
        err = abs(ratio-1.0)
        if slot!='e': errs_no_e.append(err)
        rows.append({
            **pr,
            'predicted_mev_v5_3_diagnostic': pred,
            'benchmark_mev_post_freeze_scoring_only': benchmark,
            'ratio_pred_over_benchmark': ratio,
            'absolute_relative_error': err,
            'formula_fingerprint_sha256': fingerprint,
            'mass_closure_claimed': False,
            'canon_allowed': False,
        })

    metrics = {
        'mean_absolute_relative_error_excluding_e_anchor': statistics.mean(errs_no_e),
        'median_absolute_relative_error_excluding_e_anchor': statistics.median(errs_no_e),
        'max_absolute_relative_error_excluding_e_anchor': max(errs_no_e),
        'v5_2_mean_absolute_relative_error_excluding_e_anchor': v52['metrics']['mean_absolute_relative_error_excluding_e_anchor'],
        'improvement_vs_v5_2_mean_error': v52['metrics']['mean_absolute_relative_error_excluding_e_anchor'] - statistics.mean(errs_no_e),
        'passes_numeric_debt9_closure_threshold': False,
        'closure_threshold_policy': 'Denied: electron is still unit anchor; formula was introduced after v5.2 diagnosis; muon error remains large enough to block canon closure.',
    }
    result={
        'schema': 'METATIME_RAMANUJAN_OI_LEPTON_NORMALIZER_V5_3',
        'module': '53_debt9_ramanujan_oi_lepton_normalizer_v5_3',
        'created_utc': '2026-06-21T00:00:00Z',
        'technical_status': 'PASS',
        'formal_status': 'PASS_WITH_EXPLICIT_RAMANUJAN_OI_SOURCE_LEDGER',
        'substantive_status': 'PARTIAL_IMPROVEMENT_FAIL_AS_DEBT9_NUMERIC_CLOSURE',
        'mass_closure_claimed': False,
        'observed_targets_used_in_operator': False,
        'operator_adjusted_after_scoring': False,
        'old_solver_used': False,
        'table_replay_used': False,
        'frozen_formula': frozen_formula,
        'formula_pre_benchmark_fingerprint_sha256': fingerprint,
        'rows': rows,
        'metrics': metrics,
        'decision': {
            'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
            'canon_allowed': False,
            'current_promotion': 'DENY_CURRENT',
            'allowed_next_step': 'Use Ramanujan-OI path normalizer as a strong clue; next freeze must derive a true no-anchor scale or a muon-specific generation channel from existing non-mass sources.',
            'denied_next_step': 'Claiming charged-lepton masses derived or declaring Debt 9 closed.',
        },
        'taint_ledger': {
            'electron_unit_anchor': 'Still inherited from prior unit convention; blocks no-parameter closure.',
            'post_v5_2_formula_selection': 'This normalizer was installed after noticing the missing Ramanujan/OI layer; useful diagnostic, not independent blind prediction.',
            'benchmark_targets': 'Used only after formula fingerprint for scoring.',
            'observed_masses_as_inputs': 'Not used.',
        },
        'source_assertions': {
            'ramanujan_visibility_definition': 'visibility = exp(-ramanujan_scaled_action / OIB) from v2.1 script/results.',
            'information_operator_role': 'OIB=ln2/(24*pi) as quantum of informational preference fluctuation from v2.9 and step-docs.',
            'spinor_half_path_rule': 'half-action amplitude over root-relative generation path, consistent with short-doc half-phase/lifted closure convention.',
        }
    }
    OUT.mkdir(exist_ok=True)
    (OUT/'ramanujan_oi_lepton_normalizer_v5_3.json').write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    write_csv(OUT/'ramanujan_oi_lepton_normalizer_v5_3.csv', rows)
    print(json.dumps({
        'status':'PASS_PARTIAL_IMPROVEMENT_NOT_CLOSURE',
        'fingerprint': fingerprint,
        'mean_error_excluding_e_anchor': metrics['mean_absolute_relative_error_excluding_e_anchor'],
        'improvement_vs_v5_2_mean_error': metrics['improvement_vs_v5_2_mean_error'],
        'debt9_numeric_spectrum': result['decision']['debt9_numeric_spectrum'],
    }, indent=2))

if __name__=='__main__':
    main()
