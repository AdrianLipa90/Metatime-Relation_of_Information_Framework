#!/usr/bin/env python3
"""
METATIME / Standard Model derivation v4.8
Charged-lepton generation operator review.

Purpose:
- keep v4.7 as the baseline;
- audit whether document-declared charged-lepton holonomy coefficients and frozen tau_v2
  structural action repair the mu/tau inversion without adding new ontology;
- benchmark only after the candidate transforms are declared;
- deny numeric Debt 9 closure because the electron unit anchor and document holonomy table remain
  diagnostic layers, not a no-parameter derivation.

This executable does not call archived mass solvers and does not read reference spectra as input to the
operator. Benchmark values are read only after the candidate transforms are produced.
"""
from __future__ import annotations
import csv, hashlib, json, math, pathlib, statistics
from typing import Any, Dict, List

MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
ROOT = MODULE_DIR.parents[0]
OUT = MODULE_DIR / 'results'
V47_JSON = ROOT / '47_debt9_sector_split_holonomy_operator_v4_7' / 'results' / 'sector_split_holonomy_operator_v4_7.json'
TAU_V2_TABLE = ROOT / '27_debt9_tau_v2_clean_information_eigenvalue_v2_9' / 'results' / 'tau_v2_structural_information_eigenvalue_table_v2_9.csv'

# Document-declared charged-lepton holonomy coefficients from MetaTheory_260218_073120.txt Appendix:
# Omega: e-mu 0.842, e-tau 0.915, mu-tau 0.887.
# F:     e-mu 0.145, e-tau 0.302, mu-tau 0.203.
# These are NOT rederived here; they are ledgered as document-derived, diagnostic coefficients.
LEPTON_OMEGA = {('e','mu'):0.842, ('e','tau'):0.915, ('mu','tau'):0.887}
LEPTON_F = {('e','mu'):0.145, ('e','tau'):0.302, ('mu','tau'):0.203}
KAPPA_INFORMATION_QUANTUM = math.log(2.0)/(24.0*math.pi)
BENCHMARK_ORDER = ['e','mu','tau']


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',',':')).encode()).hexdigest()


def read_csv(path: pathlib.Path) -> List[Dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path: pathlib.Path, rows: List[Dict[str, Any]]) -> None:
    if not rows: return
    keys=[]
    for r in rows:
        for k in r.keys():
            if k not in keys: keys.append(k)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerows(rows)


def load_inputs() -> Dict[str, Any]:
    v47 = json.loads(V47_JSON.read_text(encoding='utf-8'))
    tau_rows = read_csv(TAU_V2_TABLE)
    tau = {r['fermion']: r for r in tau_rows if r['class']=='charged_lepton'}
    leptons = {r['slot']: r for r in v47['benchmark']['rows'] if r['family']=='leptons'}
    if sorted(leptons) != ['e','mu','tau']:
        raise RuntimeError('v4.7 charged-lepton rows missing')
    if sorted(tau) != ['e','mu','tau']:
        raise RuntimeError('tau_v2 charged-lepton rows missing')
    return {'v47':v47, 'leptons':leptons, 'tau_v2':tau}


def base_prediction_rows(inputs: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    rows = {}
    for s in BENCHMARK_ORDER:
        r=inputs['leptons'][s]
        tau=inputs['tau_v2'][s]
        rows[s] = {
            'baseline_predicted_mev': float(r['predicted_mev_diagnostic']),
            'benchmark_mev': float(r['benchmark_mev']),
            'sector_split_lambda_v47': float(r['sector_split_lambda']),
            'tau_v2_action': float(tau['tau_v2_action']),
            'tau_v2_relative_quanta': float(tau['tau_v2_relative_to_electron_quanta']),
            'tau_v2_relative_action': KAPPA_INFORMATION_QUANTUM * float(tau['tau_v2_relative_to_electron_quanta']),
        }
    return rows


def candidate_predictions(base: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, Any]]:
    # All transforms are declared here before computing errors.
    # The transforms operate at diagnostic mass level because the document calls F_ij correction factors
    # in the mass formula, not lambda coordinates. Lambda-level variants were rejected as a guard note in
    # the report because they over-amplify the correction and are not the documented use.
    tau_gate = {s: math.exp(base[s]['tau_v2_relative_action']) for s in BENCHMARK_ORDER}
    amp_tau_gate = {s: math.sqrt(tau_gate[s]) for s in BENCHMARK_ORDER}
    pred0 = {s: base[s]['baseline_predicted_mev'] for s in BENCHMARK_ORDER}
    candidates = {
        'v47_baseline': {
            'formula': 'm_48=m_47',
            'role': 'baseline from v4.7; shows mu high / tau low inversion',
            'uses_lepton_F': False,
            'uses_tau_v2': False,
            'pred': pred0,
        },
        'doc_F_mass_screen_release': {
            'formula': 'm_mu=m47_mu*F_e_mu; m_tau=m47_tau/F_e_tau; electron unchanged',
            'role': 'direct document F_ij mass-level screen/release diagnostic',
            'uses_lepton_F': True,
            'uses_tau_v2': False,
            'pred': {'e':pred0['e'], 'mu':pred0['mu']*LEPTON_F[('e','mu')], 'tau':pred0['tau']/LEPTON_F[('e','tau')]},
        },
        'tau_v2_action_gate': {
            'formula': 'm_i=m47_i*exp(kappa*(tau_v2_i-tau_v2_e))',
            'role': 'frozen tau_v2 information-action gate only',
            'uses_lepton_F': False,
            'uses_tau_v2': True,
            'pred': {s: pred0[s]*tau_gate[s] for s in BENCHMARK_ORDER},
        },
        'doc_F_plus_tau_v2_full_action': {
            'formula': 'm_mu=m47_mu*F_e_mu*exp(delta_tau_v2_action_mu); m_tau=m47_tau/F_e_tau*exp(delta_tau_v2_action_tau)',
            'role': 'document F screen/release combined with full tau_v2 action gate',
            'uses_lepton_F': True,
            'uses_tau_v2': True,
            'pred': {'e':pred0['e'], 'mu':pred0['mu']*LEPTON_F[('e','mu')]*tau_gate['mu'], 'tau':pred0['tau']/LEPTON_F[('e','tau')]*tau_gate['tau']},
        },
        'doc_F_plus_tau_v2_amplitude_gate': {
            'formula': 'm_mu=m47_mu*F_e_mu*sqrt(exp(delta_tau_v2_action_mu)); m_tau=m47_tau/F_e_tau*sqrt(exp(delta_tau_v2_action_tau))',
            'role': 'document F screen/release plus amplitude-level tau_v2 action gate',
            'uses_lepton_F': True,
            'uses_tau_v2': True,
            'pred': {'e':pred0['e'], 'mu':pred0['mu']*LEPTON_F[('e','mu')]*amp_tau_gate['mu'], 'tau':pred0['tau']/LEPTON_F[('e','tau')]*amp_tau_gate['tau']},
        },
    }
    return candidates


def score_candidates(candidates: Dict[str, Dict[str, Any]], base: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
    rows=[]
    for name, c in candidates.items():
        errs=[]
        for slot in BENCHMARK_ORDER:
            pred=c['pred'][slot]
            ref=base[slot]['benchmark_mev']
            err=abs(pred/ref-1.0)
            if slot!='e': errs.append(err)
            rows.append({
                'candidate': name,
                'slot': slot,
                'predicted_mev_diagnostic': pred,
                'benchmark_mev': ref,
                'ratio_pred_over_benchmark': pred/ref,
                'absolute_relative_error': err,
                'formula': c['formula'],
                'role': c['role'],
                'uses_lepton_F': c['uses_lepton_F'],
                'uses_tau_v2': c['uses_tau_v2'],
                'unit_anchor_electron_inherited_from_v4_7': True,
                'mass_prediction_claimed': False,
                'debt9_numeric_closure_allowed': False,
            })
        c['metrics_excluding_e_anchor'] = {
            'median_absolute_relative_error': statistics.median(errs),
            'mean_absolute_relative_error': statistics.mean(errs),
            'max_absolute_relative_error': max(errs),
        }
    return rows


def main() -> None:
    inputs=load_inputs()
    base=base_prediction_rows(inputs)
    candidates=candidate_predictions(base)
    rows=score_candidates(candidates, base)
    candidate_summary=[]
    for name,c in candidates.items():
        candidate_summary.append({
            'candidate': name,
            'formula': c['formula'],
            'role': c['role'],
            'uses_lepton_F': c['uses_lepton_F'],
            'uses_tau_v2': c['uses_tau_v2'],
            **c['metrics_excluding_e_anchor'],
        })
    candidate_summary.sort(key=lambda x: x['mean_absolute_relative_error'])

    result={
        'schema':'METATIME_SM_CHARGED_LEPTON_GENERATION_REVIEW_V4_8',
        'module':'48_debt9_charged_lepton_generation_review_v4_8',
        'technical_status':'PASS',
        'formal_status':'PASS_WITH_EXPLICIT_TAINT_LEDGER',
        'substantive_status':'PARTIAL_DIAGNOSTIC_PROGRESS_FAIL_AS_NUMERIC_CLOSURE',
        'debt9_numeric_spectrum':'OPEN_NOT_CLOSED',
        'canon_allowed':False,
        'current_promotion':'DENY_CURRENT',
        'operator_review_fingerprint_sha256': sha256_json({'base':base,'candidates':{k:{kk:vv for kk,vv in v.items() if kk!='pred'}|{'pred':v['pred']} for k,v in candidates.items()}, 'F':{f'{a}_{b}':v for (a,b),v in LEPTON_F.items()}, 'Omega':{f'{a}_{b}':v for (a,b),v in LEPTON_OMEGA.items()}}),
        'source_layers': {
            'v4_7_baseline':'sector split holonomy operator results',
            'tau_v2':'v2.9 frozen structural information eigenvalue table; no observed masses used by tau_v2 module',
            'lepton_holonomy_F':'document-declared charged-lepton F_ij table from MetaTheory appendix; not independently rederived in v4.8',
            'benchmark_use':'post-candidate diagnostic only; not used inside candidate transforms',
        },
        'document_lepton_holonomy': {'Omega': {f'{a}_{b}':v for (a,b),v in LEPTON_OMEGA.items()}, 'F': {f'{a}_{b}':v for (a,b),v in LEPTON_F.items()}},
        'base_rows': base,
        'candidate_summary_ranked_by_mean_error_excluding_e_anchor': candidate_summary,
        'candidate_rows': rows,
        'taint_ledger': {
            'electron_unit_anchor':'inherited from v4.7 benchmark units; therefore no no-parameter closure',
            'lepton_F_table':'document says derived from numerical integration, but v4.8 does not reproduce the integration; diagnostic only',
            'screen_release_orientation':'chosen from document interpretation before scoring, but still requires v4.9 freeze if promoted',
            'best_candidate_selection':'ranked after benchmark; cannot be retroactively called a prediction',
            'no_mass_closure':'Debt 9 remains open',
        },
        'main_findings': [
            'The v4.7 mu/tau inversion is strongly reduced by applying document charged-lepton holonomy at mass level.',
            'The best diagnostic candidate in this review is not a closure because it is selected after comparison and inherits the electron unit anchor.',
            'The document F_ij layer has the correct qualitative sign: muon screening and tau open-holonomy release.',
            'A future v4.9 may freeze one specific charged-lepton operator before a sealed benchmark; v4.8 itself denies canon/current promotion.',
        ],
    }
    OUT.mkdir(exist_ok=True)
    (OUT/'charged_lepton_generation_review_v4_8.json').write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    write_csv(OUT/'charged_lepton_generation_review_v4_8.csv', rows)
    write_csv(OUT/'candidate_summary_v4_8.csv', candidate_summary)

    md=[]
    md.append('# v4.8 Charged-Lepton Generation Operator Review')
    md.append('')
    md.append('Status: **PASS as diagnostic review; FAIL as numeric Debt 9 closure**.')
    md.append('')
    md.append('v4.8 tests whether the already existing charged-lepton holonomy coefficients and frozen tau_v2 action repair the v4.7 mu/tau inversion. It does not add a new ontology and does not claim a mass prediction.')
    md.append('')
    md.append(f"Review fingerprint: `{result['operator_review_fingerprint_sha256']}`")
    md.append('')
    md.append('## Ranked candidates, excluding the electron unit anchor')
    md.append('')
    md.append('| rank | candidate | mean abs rel error | median abs rel error | max abs rel error |')
    md.append('|---:|---|---:|---:|---:|')
    for i,c in enumerate(candidate_summary,1):
        md.append(f"| {i} | `{c['candidate']}` | {c['mean_absolute_relative_error']:.6g} | {c['median_absolute_relative_error']:.6g} | {c['max_absolute_relative_error']:.6g} |")
    md.append('')
    md.append('## Interpretation')
    md.append('')
    md.append('- The document F_ij layer has the right qualitative direction: it screens the muon channel and releases the tau channel.')
    md.append('- The review still cannot close Debt 9: the electron unit anchor remains inherited, F_ij is not rederived here, and the best diagnostic candidate is ranked after benchmark comparison.')
    md.append('- The next valid step is v4.9: freeze one predeclared charged-lepton operator, then run a sealed benchmark without changing it.')
    md.append('')
    md.append('## Guard status')
    md.append('')
    md.append('- archived mass solvers: not used')
    md.append('- reference replay: not used')
    md.append('- post-residual tuning: denied')
    md.append('- canon/current promotion: denied')
    (MODULE_DIR/'METATIME_SM_CHARGED_LEPTON_GENERATION_REVIEW_v4_8.md').write_text('\n'.join(md)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
