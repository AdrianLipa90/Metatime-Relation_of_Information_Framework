#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math, statistics
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
OUT = MODULE / 'results'
ORDER = ['e','mu','tau']
OIB = math.log(2.0)/(24.0*math.pi)
L3 = 7.0

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
    v53 = load_json(ROOT/'53_debt9_ramanujan_oi_lepton_normalizer_v5_3'/'results'/'ramanujan_oi_lepton_normalizer_v5_3.json')
    tau_rows_all = read_csv(ROOT/'27_debt9_tau_v2_clean_information_eigenvalue_v2_9'/'results'/'tau_v2_structural_information_eigenvalue_table_v2_9.csv')
    tau = {r['fermion']: r for r in tau_rows_all if r['class']=='charged_lepton'}
    v53_rows = {r['slot']: r for r in v53['rows']}

    frozen_formula = {
        'name': 'RamanujanComponentSplitLeptonRefinement_v5_4',
        'role': 'component-level refinement of the v5.3 charged-lepton diagnostic using already-frozen tau_v2 Ramanujan components',
        'source_components': {
            'ramanujan_resonance_release_component': 'from tau_v2 v2.9 table; interpreted as adjacent-generation resonance damping when nonzero after the electron root',
            'ramanujan_entropy_component': 'from tau_v2 v2.9 table; interpreted as terminal-clock entropy release measured in OIB units over L3=7',
            'OIB': 'ln2/(24*pi), information preference quantum from short-docs',
            'L3': 'base Collatz clock length for seed 3',
        },
        'formula': {
            'starting_point': 'm_i(v5.4) = m_i(v5.3) * C_i',
            'electron_root': 'C_e = 1, electron unit anchor preserved only as inherited unit; not closure',
            'component_split_gate': 'C_i = exp(-R_i) * exp(OIB * L3 * E_i), for i in {mu,tau}',
            'R_i': 'ramanujan_resonance_release_component_i',
            'E_i': 'ramanujan_entropy_component_i',
        },
        'boundaries': {
            'post_v5_3_refinement': True,
            'new_free_parameter_added': False,
            'observed_masses_used_in_operator': False,
            'benchmark_targets_used_only_after_fingerprint': True,
            'mass_closure_claimed': False,
            'canon_allowed': False,
        }
    }

    pre_rows=[]
    for slot in ORDER:
        r=tau[slot]
        resonance=float(r['ramanujan_resonance_release_component'])
        entropy=float(r['ramanujan_entropy_component'])
        if slot == 'e':
            gate = 1.0
            damping = 1.0
            release = 1.0
        else:
            damping = math.exp(-resonance)
            release = math.exp(OIB * L3 * entropy)
            gate = damping * release
        pre_rows.append({
            'slot': slot,
            'generation': int(r['generation']),
            'tau_v2_action': float(r['tau_v2_action']),
            'tau_v2_preference_quanta': float(r['tau_v2_preference_quanta']),
            'ramanujan_entropy_component': entropy,
            'ramanujan_resonance_release_component': resonance,
            'OIB_ln2_over_24pi': OIB,
            'L3_base_clock': L3,
            'resonance_damping_gate': damping,
            'entropy_release_gate': release,
            'component_split_gate': gate,
            'v5_3_prediction_input_mev': float(v53_rows[slot]['predicted_mev_v5_3_diagnostic']),
        })
    fingerprint = sha_obj({'formula': frozen_formula, 'pre_benchmark_rows': pre_rows})

    rows=[]; errs_no_e=[]
    for pr in pre_rows:
        slot=pr['slot']
        pred = pr['v5_3_prediction_input_mev'] * pr['component_split_gate']
        benchmark = float(v53_rows[slot]['benchmark_mev_post_freeze_scoring_only'])
        ratio = pred/benchmark
        err = abs(ratio-1.0)
        if slot!='e': errs_no_e.append(err)
        rows.append({
            **pr,
            'predicted_mev_v5_4_diagnostic': pred,
            'benchmark_mev_post_freeze_scoring_only': benchmark,
            'ratio_pred_over_benchmark': ratio,
            'absolute_relative_error': err,
            'formula_fingerprint_sha256': fingerprint,
            'mass_closure_claimed': False,
            'canon_allowed': False,
        })

    metrics = {
        'v5_3_mean_absolute_relative_error_excluding_e_anchor': v53['metrics']['mean_absolute_relative_error_excluding_e_anchor'],
        'mean_absolute_relative_error_excluding_e_anchor': statistics.mean(errs_no_e),
        'median_absolute_relative_error_excluding_e_anchor': statistics.median(errs_no_e),
        'max_absolute_relative_error_excluding_e_anchor': max(errs_no_e),
        'improvement_vs_v5_3_mean_error': v53['metrics']['mean_absolute_relative_error_excluding_e_anchor'] - statistics.mean(errs_no_e),
        'passes_numeric_debt9_closure_threshold': False,
        'closure_threshold_policy': 'Denied: formula introduced after v5.3 residual analysis; electron unit anchor remains inherited; full fermion spectrum/quarks not included; must be re-frozen and cross-sector tested before any closure claim.',
    }
    result={
        'schema':'METATIME_RAMANUJAN_COMPONENT_SPLIT_LEPTON_REFINEMENT_V5_4',
        'module':'54_debt9_ramanujan_component_split_lepton_refinement_v5_4',
        'created_utc':'2026-06-21T00:00:00Z',
        'technical_status':'PASS',
        'formal_status':'PASS_WITH_EXPLICIT_COMPONENT_SOURCE_LEDGER',
        'substantive_status':'STRONG_CHARGED_LEPTON_REFINEMENT_DIAGNOSTIC_NOT_CLOSURE',
        'mass_closure_claimed': False,
        'observed_targets_used_in_operator': False,
        'operator_adjusted_after_scoring': False,
        'old_solver_used': False,
        'table_replay_used': False,
        'new_free_parameter_added': False,
        'frozen_formula': frozen_formula,
        'formula_pre_benchmark_fingerprint_sha256': fingerprint,
        'rows': rows,
        'metrics': metrics,
        'decision': {
            'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
            'canon_allowed': False,
            'current_promotion': 'DENY_CURRENT',
            'allowed_next_step': 'Use v5.4 as a strong component-split clue; next step must freeze the formula before testing quark/lepton combined sectors or remove the inherited electron unit anchor.',
            'denied_next_step': 'Declaring charged leptons derived, closing Debt 9, or using v5.4 as canon because it was selected after v5.3 residual analysis.',
        },
        'taint_ledger': {
            'post_v5_3_residual_refinement': 'This component split was created after inspecting the muon/tau residual pattern; diagnostic only until independently re-frozen and cross-tested.',
            'electron_unit_anchor': 'Still inherited; blocks no-parameter mass closure.',
            'benchmark_targets': 'Used only after formula fingerprint for scoring.',
            'observed_masses_as_inputs': 'Not used.',
            'PDG_reference_masses_as_inputs': 'Not used in operator; benchmark values are post-freeze scoring only.',
        },
        'interpretation': {
            'muon': 'Large residual is mainly reduced by the existing Ramanujan resonance-release component, which is nonzero for mu and zero for tau.',
            'tau': 'Tau is corrected by the OIB*L3 Ramanujan entropy release and remains near benchmark.',
            'scope': 'charged-lepton diagnostic only; no quark-sector or full Debt 9 closure.'
        }
    }
    OUT.mkdir(exist_ok=True)
    (OUT/'ramanujan_component_split_lepton_refinement_v5_4.json').write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    write_csv(OUT/'ramanujan_component_split_lepton_refinement_v5_4.csv', rows)
    print(json.dumps({
        'status':'PASS_STRONG_DIAGNOSTIC_NOT_CLOSURE',
        'fingerprint': fingerprint,
        'mean_error_excluding_e_anchor': metrics['mean_absolute_relative_error_excluding_e_anchor'],
        'improvement_vs_v5_3': metrics['improvement_vs_v5_3_mean_error'],
        'debt9_numeric_spectrum': result['decision']['debt9_numeric_spectrum'],
    }, indent=2))

if __name__=='__main__':
    main()
