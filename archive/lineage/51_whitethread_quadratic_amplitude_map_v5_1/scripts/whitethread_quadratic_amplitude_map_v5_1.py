#!/usr/bin/env python3
"""
Module 51 / v5.1: White-Thread quadratic amplitude map candidate.

Purpose:
    Build an explicit amplitude map candidate for strong charged-lepton W_ij gates
    from existing Metatime ingredients only: OIB = ln2/(24*pi), L3 = 7,
    and the already-frozen tau_v2 preference-quanta separation.

Boundary:
    This executable does not predict particle masses, does not use observed mass
    tables, and does not import old solvers. Document F entries are diagnostic
    targets-to-explain only, not solver inputs.
"""
from __future__ import annotations
import csv, hashlib, json, math
from pathlib import Path

OIB = math.log(2.0)/(24.0*math.pi)
L3 = 7.0
GEN = {'e': 1, 'mu': 2, 'tau': 3}
# From tau_v2 clean information eigenvalue layer v2.9: relative preference quanta to electron.
TAU_V2_RELATIVE_QUANTA = {'e': 0.0, 'mu': -54.463282428505806, 'tau': 59.35421399867016}
# Diagnostic F table from document/v4.8/v5.0 audit. These are targets-to-explain only.
DOCUMENT_DIAGNOSTIC_F = {'e_to_mu': 0.145, 'e_to_tau': 0.302, 'mu_to_tau': 0.203}


def canonical_payload(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def quadratic_open_action(i: str, j: str) -> float:
    """White-Thread candidate: diffusion-like open holonomy action.

    S_ij = (Delta tau_v2_quanta)^2 / (2 * L3 * Delta generation)

    Rationale: quadratic FS/diffusion action across an open generational path;
    L3 is the base Collatz clock; Delta generation is the path duration.
    """
    dg = abs(GEN[j] - GEN[i])
    if dg == 0:
        return 0.0
    dq = TAU_V2_RELATIVE_QUANTA[j] - TAU_V2_RELATIVE_QUANTA[i]
    return (dq * dq) / (2.0 * L3 * dg)


def amplitude_gate(i: str, j: str) -> float:
    return math.exp(-OIB * quadratic_open_action(i, j))


def main():
    outdir = Path(__file__).resolve().parents[1] / 'results'
    outdir.mkdir(exist_ok=True)

    rows = []
    for pair, target in DOCUMENT_DIAGNOSTIC_F.items():
        i, _, j = pair.partition('_to_')
        dq = TAU_V2_RELATIVE_QUANTA[j] - TAU_V2_RELATIVE_QUANTA[i]
        dg = abs(GEN[j] - GEN[i])
        action = quadratic_open_action(i, j)
        gate = amplitude_gate(i, j)
        rows.append({
            'pair': pair,
            'from': i,
            'to': j,
            'delta_generation': dg,
            'delta_tau_v2_preference_quanta': dq,
            'L3_base_collatz_clock': L3,
            'OIB_ln2_over_24pi': OIB,
            'quadratic_open_holonomy_action_quanta': action,
            'derived_quadratic_amplitude_gate': gate,
            'document_diagnostic_F_target_to_explain': target,
            'relative_difference_to_document_F_target': abs(gate - target) / target,
            'document_F_used_as_solver_input': False,
            'mass_prediction_claimed': False,
        })

    root_rows = [r for r in rows if r['from'] == 'e']
    all_pair_rows = rows
    root_mean_rel = sum(r['relative_difference_to_document_F_target'] for r in root_rows) / len(root_rows)
    all_mean_rel = sum(r['relative_difference_to_document_F_target'] for r in all_pair_rows) / len(all_pair_rows)

    # Non-compositionality diagnostic: if W paths are open, root gates need not compose like a closed group map.
    f_em = amplitude_gate('e', 'mu')
    f_et = amplitude_gate('e', 'tau')
    f_mt = amplitude_gate('mu', 'tau')
    comp_ratio = (f_em * f_mt) / f_et if f_et else float('nan')

    result = {
        'schema': 'METATIME_WHITETHREAD_QUADRATIC_AMPLITUDE_MAP_V5_1',
        'module': '51_whitethread_quadratic_amplitude_map_v5_1',
        'created_utc': '2026-06-21T00:00:00Z',
        'technical_status': 'PASS',
        'formal_status': 'PASS_WITH_CANDIDATE_STATUS',
        'substantive_status': 'PARTIAL_DERIVATION_CANDIDATE_ROOT_GATES_PASS_ALLPAIR_FAIL',
        'mass_prediction_claimed': False,
        'benchmark_performed': False,
        'observed_mass_input_used': False,
        'reference_spectrum_input_used': False,
        'old_solver_used': False,
        'formula': {
            'name': 'WhiteThreadQuadraticAmplitudeMap_v5_1',
            'action': 'S_ij = (Delta tau_v2_preference_quanta)^2 / (2 * L3 * DeltaGeneration)',
            'gate': 'F_ij = exp(-OIB * S_ij)',
            'OIB': 'ln2/(24*pi)',
            'L3': 'base Collatz clock from orbit length of 3',
            'status': 'candidate derived after v5.0 derivability audit; not canon and not a mass-spectrum closure',
        },
        'constants': {
            'OIB_ln2_over_24pi': OIB,
            'L3_base_collatz_clock': L3,
            'tau_v2_relative_preference_quanta': TAU_V2_RELATIVE_QUANTA,
        },
        'rows': rows,
        'diagnostics': {
            'root_relative_difference_mean_to_document_F_targets': root_mean_rel,
            'all_pair_relative_difference_mean_to_document_F_targets': all_mean_rel,
            'root_gates_close_to_large_document_F': root_mean_rel < 0.05,
            'all_pair_gate_derivation_passes': all_mean_rel < 0.10,
            'mu_to_tau_allpair_failure': True,
            'open_path_noncompositionality_ratio_Fem_Fmt_over_Fet': comp_ratio,
            'interpretation': 'The quadratic open-holonomy action explains the two e-root screen/release gates at few-percent level, but it does not derive the full all-pair F table. This suggests a root-relative open path gate rather than a compositional all-pair metric.',
        },
        'decision': {
            'strong_root_F_candidate_promoted_to_next_freeze': True,
            'large_F_table_promoted_as_first_principles': False,
            'full_charged_lepton_mass_closure': False,
            'allowed_next_step': 'Freeze this root-relative quadratic amplitude map and test it in a single sealed charged-lepton kernel pass, with explicit non-canon status because the map was selected after the v5.0 target audit.',
            'denied_next_step': 'Declaring full all-pair F_ij derived or using the large F table as solver input.',
        },
        'taint_ledger': {
            'document_F_targets': 'DIAGNOSTIC_TARGETS_ONLY_NOT_SOLVER_INPUTS',
            'quadratic_action_rule': 'CANDIDATE_BUILT_FROM_EXISTING_L3_AND_TAU_V2_AFTER_V5_0_AUDIT',
            'observed_mass_tables': 'NOT_USED',
            'old_solvers': 'NOT_USED',
        },
        'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
        'canon_allowed': False,
        'current_promotion': 'DENY_CURRENT',
    }
    result['operator_candidate_fingerprint_sha256'] = hashlib.sha256(canonical_payload({
        'formula': result['formula'],
        'constants': result['constants'],
        'rows_without_targets': [
            {k: v for k, v in row.items() if k not in ('document_diagnostic_F_target_to_explain', 'relative_difference_to_document_F_target')}
            for row in rows
        ],
    }).encode('utf-8')).hexdigest()

    (outdir/'whitethread_quadratic_amplitude_map_v5_1.json').write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    with (outdir/'whitethread_quadratic_amplitude_map_v5_1.csv').open('w', newline='', encoding='utf-8') as f:
        fieldnames = list(rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(json.dumps({
        'status': 'PASS_CANDIDATE_FROZEN_NOT_BENCHMARKED',
        'fingerprint': result['operator_candidate_fingerprint_sha256'],
        'root_mean_relative_difference_to_document_F': root_mean_rel,
        'all_pair_mean_relative_difference_to_document_F': all_mean_rel,
        'debt9_numeric_spectrum': result['debt9_numeric_spectrum'],
    }, indent=2))


if __name__ == '__main__':
    main()
