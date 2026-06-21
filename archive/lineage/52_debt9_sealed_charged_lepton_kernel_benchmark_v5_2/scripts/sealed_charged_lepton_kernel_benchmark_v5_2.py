#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math, statistics
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
OUT = MODULE / 'results'

ORDER = ['e', 'mu', 'tau']


def load_json(path: Path):
    with path.open(encoding='utf-8') as f:
        return json.load(f)


def sha_obj(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()


def write_csv(path: Path, rows):
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def main():
    v48 = load_json(ROOT/'48_debt9_charged_lepton_generation_review_v4_8'/'results'/'charged_lepton_generation_review_v4_8.json')
    v49 = load_json(ROOT/'49_short_doc_charged_lepton_kernel_freeze_v4_9'/'results'/'short_doc_charged_lepton_kernel_freeze_v4_9.json')
    v51 = load_json(ROOT/'51_whitethread_quadratic_amplitude_map_v5_1'/'results'/'whitethread_quadratic_amplitude_map_v5_1.json')

    base = v48['base_rows']
    f_rows = {r['pair']: r for r in v51['rows']}
    derived_F = {
        'mu': f_rows['e_to_mu']['derived_quadratic_amplitude_gate'],
        'tau': f_rows['e_to_tau']['derived_quadratic_amplitude_gate'],
    }
    root_gate_fingerprint = v51['operator_candidate_fingerprint_sha256']
    short_kernel_fingerprint = v49['operator_fingerprint_sha256']

    # Frozen before scoring: electron unit carried from v4.7 units; mu screened by root gate; tau released by inverse root gate;
    # tau_v2 relative action enters at amplitude level from the existing half-action convention.
    frozen_formula = {
        'name': 'SealedChargedLeptonKernel_v5_2',
        'inputs': {
            'base_mass_units': 'v4.7/v4.8 charged-lepton baseline rows; electron unit anchor inherited, not a no-parameter claim',
            'root_gate': 'v5.1 White-Thread quadratic root-relative F(e,i)',
            'tau_action': 'v4.8 tau_v2 relative action, amplitude-level half action',
            'short_doc_kernel': 'v4.9 short-doc kernel retained as provenance; not used as a tunable multiplier in v5.2 benchmark formula',
        },
        'formula': {
            'e': 'm_e = baseline_e',
            'mu': 'm_mu = baseline_mu * F(e,mu)_v5.1 * exp(0.5*DeltaTauAction_mu)',
            'tau': 'm_tau = baseline_tau / F(e,tau)_v5.1 * exp(0.5*DeltaTauAction_tau)',
        },
        'status': 'sealed test formula; no post-result adjustment allowed',
    }
    pre_benchmark_fingerprint = sha_obj({
        'frozen_formula': frozen_formula,
        'root_gate_fingerprint': root_gate_fingerprint,
        'short_doc_kernel_fingerprint': short_kernel_fingerprint,
        'derived_F_values': derived_F,
        'base_pre_benchmark_inputs_without_measured_targets': {
            slot: {
                'baseline_predicted_mev': base[slot]['baseline_predicted_mev'],
                'tau_v2_relative_action': base[slot]['tau_v2_relative_action'],
                'tau_v2_relative_quanta': base[slot]['tau_v2_relative_quanta'],
            } for slot in ORDER
        },
    })

    predictions = {
        'e': base['e']['baseline_predicted_mev'],
        'mu': base['mu']['baseline_predicted_mev'] * derived_F['mu'] * math.exp(0.5 * base['mu']['tau_v2_relative_action']),
        'tau': base['tau']['baseline_predicted_mev'] / derived_F['tau'] * math.exp(0.5 * base['tau']['tau_v2_relative_action']),
    }

    rows = []
    errs_no_e = []
    for slot in ORDER:
        pred = predictions[slot]
        benchmark = base[slot]['benchmark_mev']
        ratio = pred / benchmark
        err = abs(ratio - 1.0)
        if slot != 'e':
            errs_no_e.append(err)
        rows.append({
            'slot': slot,
            'predicted_mev_sealed_formula': pred,
            'benchmark_mev_post_freeze_scoring_only': benchmark,
            'ratio_pred_over_benchmark': ratio,
            'absolute_relative_error': err,
            'baseline_predicted_mev_from_v47_v48': base[slot]['baseline_predicted_mev'],
            'tau_v2_relative_action': base[slot]['tau_v2_relative_action'],
            'tau_v2_relative_quanta': base[slot]['tau_v2_relative_quanta'],
            'derived_root_gate_used': 1.0 if slot == 'e' else derived_F[slot],
            'root_gate_role': 'unit' if slot == 'e' else ('screening_multiply' if slot == 'mu' else 'release_inverse'),
            'sealed_formula_fingerprint': pre_benchmark_fingerprint,
            'mass_closure_claimed': False,
            'canon_allowed': False,
        })

    metrics = {
        'median_absolute_relative_error_excluding_e_anchor': statistics.median(errs_no_e),
        'mean_absolute_relative_error_excluding_e_anchor': statistics.mean(errs_no_e),
        'max_absolute_relative_error_excluding_e_anchor': max(errs_no_e),
        'passes_numeric_debt9_closure_threshold': False,
        'closure_threshold_policy': 'Denied: errors remain order-one and electron unit is inherited from previous unit anchor.'
    }

    result = {
        'schema': 'METATIME_SEALED_CHARGED_LEPTON_KERNEL_BENCHMARK_V5_2',
        'module': '52_debt9_sealed_charged_lepton_kernel_benchmark_v5_2',
        'created_utc': '2026-06-21T00:00:00Z',
        'technical_status': 'PASS',
        'formal_status': 'PASS_SEALED_FORMULA_WITH_EXPLICIT_BOUNDARIES',
        'substantive_status': 'PARTIAL_IMPROVEMENT_FAIL_AS_DEBT9_NUMERIC_CLOSURE',
        'sealed_benchmark_performed': True,
        'mass_closure_claimed': False,
        'observed_targets_used_in_operator': False,
        'operator_adjusted_after_scoring': False,
        'old_solver_used': False,
        'table_replay_used': False,
        'frozen_formula': frozen_formula,
        'root_gate_candidate_fingerprint_v5_1': root_gate_fingerprint,
        'short_doc_kernel_fingerprint_v4_9': short_kernel_fingerprint,
        'sealed_formula_pre_benchmark_fingerprint_sha256': pre_benchmark_fingerprint,
        'rows': rows,
        'metrics': metrics,
        'comparison': {
            'v4_8_best_diagnostic_mean_error_excluding_e_anchor': 0.7894292410380577,
            'v5_2_sealed_mean_error_excluding_e_anchor': metrics['mean_absolute_relative_error_excluding_e_anchor'],
            'interpretation': 'Derived v5.1 root gates slightly improve the prior document-F diagnostic, but order-one mu/tau errors remain; this is not a mass-spectrum closure.'
        },
        'decision': {
            'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
            'canon_allowed': False,
            'current_promotion': 'DENY_CURRENT',
            'allowed_next_step': 'Analyze residual structure; do not tune the same operator after seeing errors. Next work should derive the missing generational exponent/normalization or reject this branch as insufficient.',
            'denied_next_step': 'Calling the charged-lepton spectrum derived or promoting v5.2 to canon/current.'
        },
        'taint_ledger': {
            'electron_unit_anchor': 'Inherited from v4.7/v4.8 unit convention; acceptable for diagnostic, not no-parameter closure.',
            'root_gate_selection': 'Candidate selected after v5.0 derivability audit; sealed for v5.2 scoring but not independent blind prediction.',
            'benchmark_targets': 'Used only after formula fingerprint; not solver inputs.',
            'full_all_pair_Fij': 'Not used; v5.1 failed all-pair derivation.',
        }
    }

    OUT.mkdir(exist_ok=True)
    (OUT/'sealed_charged_lepton_kernel_benchmark_v5_2.json').write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    write_csv(OUT/'sealed_charged_lepton_kernel_benchmark_v5_2.csv', rows)
    print(json.dumps({
        'status': 'PASS_SEALED_BENCHMARK_FAIL_AS_NUMERIC_CLOSURE',
        'sealed_formula_fingerprint': pre_benchmark_fingerprint,
        'mean_error_excluding_e_anchor': metrics['mean_absolute_relative_error_excluding_e_anchor'],
        'debt9_numeric_spectrum': result['decision']['debt9_numeric_spectrum'],
    }, indent=2))

if __name__ == '__main__':
    main()
