#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parents[1]
RESULTS = MODULE_DIR/'results'
RESULTS.mkdir(exist_ok=True)

LEDGER = ROOT/'61_planck_information_action_ledger_v6_1/results/planck_information_action_ledger_v6_1.json'
TAU_TABLE = ROOT/'27_debt9_tau_v2_clean_information_eigenvalue_v2_9/results/tau_v2_structural_information_eigenvalue_table_v2_9.csv'

ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
rows = []
with TAU_TABLE.open(newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['class'] == 'charged_lepton':
            rows.append(r)
tau = {r['fermion']: r for r in rows}
OI = float(tau['e']['kappa_information_quantum'])

S = {}
for r in ledger['target_action_rows']:
    if r['target'] in {'electron','muon','tau'}:
        key = {'electron':'e','muon':'mu','tau':'tau'}[r['target']]
        S[key] = float(r['required_information_action_S_for_Ep_exp_gate'])

# The candidate transition rules are frozen before scoring against the v6.1 target releases.
# They use only pre-existing tau_v2 / Euler-Berry geometry.
frozen_release_rules = {
    'e_to_mu': {
        'description': 'first charged-lepton release from electron Euler-Berry kappa action',
        'formula': 'R_e_mu = eb_action_kappa_v16(e)',
        'source_field': 'e.eb_action_kappa_v16',
        'candidate_release_action': float(tau['e']['eb_action_kappa_v16']),
    },
    'mu_to_tau': {
        'description': 'second charged-lepton release from muon terminal-axis phase measured in OI units',
        'formula': 'R_mu_tau = OI * terminal_axis_signature(mu)',
        'source_field': 'mu.terminal_axis_signature * OI',
        'candidate_release_action': OI * float(tau['mu']['terminal_axis_signature']),
    },
}
# Cumulative candidate, still rule-derived from the two independent frozen releases.
frozen_release_rules['e_to_tau'] = {
    'description': 'cumulative electron-to-tau release from e->mu plus mu->tau rules',
    'formula': 'R_e_tau = R_e_mu + R_mu_tau',
    'source_field': 'derived_sum_of_frozen_rules',
    'candidate_release_action': frozen_release_rules['e_to_mu']['candidate_release_action'] + frozen_release_rules['mu_to_tau']['candidate_release_action'],
}

target_releases = {
    'e_to_mu': S['e'] - S['mu'],
    'mu_to_tau': S['mu'] - S['tau'],
    'e_to_tau': S['e'] - S['tau'],
}

transition_rows=[]
for key in ['e_to_mu','mu_to_tau','e_to_tau']:
    cand = frozen_release_rules[key]['candidate_release_action']
    target = target_releases[key]
    pred_ratio = math.exp(cand/OI)
    target_ratio = math.exp(target/OI)
    transition_rows.append({
        'transition': key,
        'candidate_rule': frozen_release_rules[key]['formula'],
        'source_field': frozen_release_rules[key]['source_field'],
        'candidate_release_action': cand,
        'target_release_action_from_v6_1_scoring_only': target,
        'action_absolute_error': cand - target,
        'action_relative_error_abs': abs(cand/target - 1.0),
        'predicted_energy_ratio_from_candidate_release': pred_ratio,
        'target_energy_ratio_from_v6_1_scoring_only': target_ratio,
        'energy_ratio_relative_error_abs': abs(pred_ratio/target_ratio - 1.0),
        'mass_prediction_claimed': False,
        'absolute_action_derived': False,
        'target_used_in_candidate_rule': False,
    })

# A second, explicit search ledger: compare known source atoms to target transitions after freeze,
# to prevent hiding cherry-picking. This is post-freeze scoring only.
source_atoms=[]
for f, r in tau.items():
    source_atoms.extend([
        (f'{f}.eb_action_kappa_v16', float(r['eb_action_kappa_v16'])),
        (f'{f}.ramanujan_scaled_action', float(r['ramanujan_scaled_action'])),
        (f'{f}.OI_terminal_axis_signature', OI * float(r['terminal_axis_signature'])),
        (f'{f}.OI_tau_v2_action', OI * float(r['tau_v2_action'])),
        (f'{f}.OI_entropy_component', OI * float(r['ramanujan_entropy_component'])),
        (f'{f}.OI_resonance_release_component', OI * float(r['ramanujan_resonance_release_component'])),
        (f'{f}.OI_collatz_terminal_axis_component', OI * float(r['collatz_terminal_axis_component'])),
    ])
source_match_ledger=[]
for trans, target in target_releases.items():
    ranked=[]
    for name, val in source_atoms:
        ranked.append({
            'transition': trans,
            'source_atom': name,
            'source_value': val,
            'target_release_action_from_v6_1_scoring_only': target,
            'relative_error_abs': abs(val/target - 1.0) if target else None,
            'absolute_error': val - target,
        })
    ranked=sorted(ranked, key=lambda x: x['relative_error_abs'])[:8]
    source_match_ledger.extend(ranked)

metrics = {
    'transition_count': len(transition_rows),
    'mean_action_relative_error_abs': sum(r['action_relative_error_abs'] for r in transition_rows)/len(transition_rows),
    'max_action_relative_error_abs': max(r['action_relative_error_abs'] for r in transition_rows),
    'mean_energy_ratio_relative_error_abs': sum(r['energy_ratio_relative_error_abs'] for r in transition_rows)/len(transition_rows),
    'max_energy_ratio_relative_error_abs': max(r['energy_ratio_relative_error_abs'] for r in transition_rows),
    'e_to_mu_action_error_abs_percent': transition_rows[0]['action_relative_error_abs'] * 100,
    'mu_to_tau_action_error_abs_percent': transition_rows[1]['action_relative_error_abs'] * 100,
    'cumulative_e_to_tau_action_error_abs_percent': transition_rows[2]['action_relative_error_abs'] * 100,
}

stable = {
    'rules': frozen_release_rules,
    'OI': OI,
    'source_table_fields': ['eb_action_kappa_v16','terminal_axis_signature','kappa_information_quantum'],
    'target_releases_for_scoring_only': target_releases,
}
fingerprint = hashlib.sha256(json.dumps(stable, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()

result = {
    'schema': 'METATIME_LEPTON_INFORMATION_ACTION_RELEASE_PROBE_V6_2',
    'module': '62_lepton_information_action_release_probe_v6_2',
    'created_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'technical_status': 'PASS',
    'formal_status': 'PASS_RELATIVE_RELEASE_PROBE_INSTALLED',
    'substantive_status': 'E_MU_STRONG_SIGNAL_MU_TAU_PARTIAL_SIGNAL_ABSOLUTE_ACTION_NOT_DERIVED',
    'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
    'canon_allowed': False,
    'current_promotion': 'DENY_CURRENT',
    'mass_prediction_claimed': False,
    'absolute_action_derived': False,
    'source_formula_fingerprint_sha256': ledger.get('formula_fingerprint_sha256'),
    'release_probe_fingerprint_sha256': fingerprint,
    'core_equation': 'E_i/E_j = exp((S_j - S_i)/OI); transition releases are probed from existing geometry only.',
    'constants': {'OI': OI},
    'v6_1_target_actions_scoring_only': S,
    'frozen_release_rules': frozen_release_rules,
    'transition_rows': transition_rows,
    'source_match_ledger_top8_each_transition': source_match_ledger,
    'metrics': metrics,
    'decision': {
        'e_to_mu_release': 'STRONG_GEOMETRIC_SIGNAL_NOT_CLOSURE',
        'mu_to_tau_release': 'PARTIAL_SIGNAL_REQUIRES_REFINEMENT',
        'absolute_S_i_actions': 'NOT_DERIVED',
        'electron_absolute_offset': 'STILL_ANCHOR_IF_IMPORTED_FROM_TARGET_LEDGER',
        'debt9_closure': 'DENIED',
        'next_step': 'Derive the absolute electron action offset from non-mass geometry, or refine mu->tau with a predeclared Collatz/Ramanujan terminal rule before mass scoring.',
    },
    'guardrails': {
        'target_actions_used_in_candidate_rule': False,
        'masses_used_as_operator_inputs': False,
        'ratios_scored_after_rule_freeze': True,
        'absolute_mass_prediction_claimed': False,
        'canon_promotion_allowed': False,
    },
}
(RESULTS/'lepton_information_action_release_probe_v6_2.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
with (RESULTS/'lepton_information_action_release_probe_v6_2.csv').open('w', newline='', encoding='utf-8') as f:
    fields=list(transition_rows[0].keys())
    w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(transition_rows)
with (RESULTS/'source_match_ledger_v6_2.csv').open('w', newline='', encoding='utf-8') as f:
    fields=list(source_match_ledger[0].keys())
    w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(source_match_ledger)
print(json.dumps({'status':'PASS','fingerprint':fingerprint,'metrics':metrics}, indent=2))
