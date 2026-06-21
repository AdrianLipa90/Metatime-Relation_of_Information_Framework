#!/usr/bin/env python3
"""v6.1 Planck information-action ledger.

This module continues v6.0B. It does not claim a mass derivation. It tests a
clean dimensional normalizer candidate:

    E_i = E_P * exp(-S_i / OI)

where E_P is Planck energy from non-mass physical constants and OI=ln2/(24*pi).
It converts reference energies into required information actions S_i and action
release gaps. These are target ledgers for later derivation, not inputs to a
predictive mass formula.
"""
from __future__ import annotations
import csv, hashlib, json, math
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULE = Path(__file__).resolve().parents[1]
OUT = MODULE/'results'
OUT.mkdir(exist_ok=True)

# Exact defined constants where applicable; G is measured and used only for Planck-scale diagnostic.
c = 299_792_458.0
h = 6.626_070_15e-34
hbar = h/(2.0*math.pi)
G = 6.67430e-11
kB = 1.380649e-23
eV_J = 1.602176634e-19
OI = math.log(2.0)/(24.0*math.pi)
L3 = 7.0
f0 = 7.83

E_PLANCK_J = math.sqrt(hbar*c**5/G)
E_PLANCK_EV = E_PLANCK_J/eV_J
E_PLANCK_MEV = E_PLANCK_EV/1e6
m_PLANCK_KG = math.sqrt(hbar*c/G)

# Reference energies are scoring/ledger targets only; not used to fit E_P or OI.
TARGETS_MEV = {
    'electron': {'sector':'charged_lepton', 'energy_mev':0.51099895},
    'muon': {'sector':'charged_lepton', 'energy_mev':105.6583755},
    'tau': {'sector':'charged_lepton', 'energy_mev':1776.86},
    'proton': {'sector':'hadron_baryon', 'energy_mev':938.2720813},
    'neutron': {'sector':'hadron_baryon', 'energy_mev':939.5654133},
}

# Existing tau_v2 structural table is optional context. It is not used to define targets.
tau_context = {}
tau_path = ROOT/'27_debt9_tau_v2_clean_information_eigenvalue_v2_9/results/tau_v2_structural_information_eigenvalue_table_v2_9.csv'
if tau_path.exists():
    with tau_path.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['fermion'] in {'e','mu','tau'}:
                tau_context[row['fermion']] = {
                    'generation': int(row['generation']),
                    'eb_action_kappa_v16': float(row['eb_action_kappa_v16']),
                    'ramanujan_scaled_action': float(row['ramanujan_scaled_action']),
                    'tau_v2_action': float(row['tau_v2_action']),
                    'tau_v2_preference_quanta': float(row['tau_v2_preference_quanta']),
                }

alias = {'electron':'e','muon':'mu','tau':'tau'}
rows=[]
for name, payload in TARGETS_MEV.items():
    E = float(payload['energy_mev'])
    ratio_to_planck = E/E_PLANCK_MEV
    S_required = -OI*math.log(ratio_to_planck)
    N_linear_planck_oi = E/(E_PLANCK_MEV*OI)
    rows.append({
        'target': name,
        'sector': payload['sector'],
        'reference_energy_mev_scoring_only': E,
        'planck_energy_mev': E_PLANCK_MEV,
        'ratio_E_over_Eplanck': ratio_to_planck,
        'required_information_action_S_for_Ep_exp_gate': S_required,
        'linear_N_eff_if_E_equals_Ep_OI_N': N_linear_planck_oi,
        'linear_planck_mode_status': 'fractional_micro_occupancy_not_preferred_as_count' if N_linear_planck_oi < 1 else 'large_count',
        'action_gate_status': 'dimensionally_valid_target_action_not_derived',
        'tau_v2_context': tau_context.get(alias.get(name,''), None),
        'mass_prediction_claimed': False,
        'debt9_closure_claimed': False,
    })

# Action release ledger: S_a - S_b = OI*ln(E_b/E_a). Positive release means b is less Planck-suppressed than a.
row_by_name = {r['target']: r for r in rows}
pairs=[]
for a,b in [('electron','muon'),('electron','tau'),('muon','tau'),('electron','proton'),('proton','neutron')]:
    Sa = row_by_name[a]['required_information_action_S_for_Ep_exp_gate']
    Sb = row_by_name[b]['required_information_action_S_for_Ep_exp_gate']
    Ea = row_by_name[a]['reference_energy_mev_scoring_only']
    Eb = row_by_name[b]['reference_energy_mev_scoring_only']
    release = Sa - Sb
    pairs.append({
        'pair': f'{a}->{b}',
        'E_ratio_b_over_a': Eb/Ea,
        'action_release_Sa_minus_Sb': release,
        'OI_log_energy_ratio': OI*math.log(Eb/Ea),
        'interpretation': 'required release in information action under E=E_P exp(-S/OI)',
        'mass_prediction_claimed': False,
    })

# Compare release gaps to existing context only as diagnostic proximity, not validation.
comparisons=[]
if tau_context:
    e_mu_release = next(p['action_release_Sa_minus_Sb'] for p in pairs if p['pair']=='electron->muon')
    e_tau_release = next(p['action_release_Sa_minus_Sb'] for p in pairs if p['pair']=='electron->tau')
    for label, value in [('electron_to_muon_release', e_mu_release), ('electron_to_tau_release', e_tau_release)]:
        comps=[]
        for f, ctx in tau_context.items():
            comps.append({
                'tau_context_fermion': f,
                'context_quantity': 'eb_action_kappa_v16',
                'context_value': ctx['eb_action_kappa_v16'],
                'absolute_difference': abs(value-ctx['eb_action_kappa_v16']),
                'relative_difference_vs_release': abs(value-ctx['eb_action_kappa_v16'])/abs(value) if value else None,
            })
        comps.sort(key=lambda x: x['absolute_difference'])
        comparisons.append({'release_label':label, 'release_value':value, 'nearest_existing_contexts': comps[:3]})

# Scale ladder from v6.0B plus Planck. No target fitting here.
scale_ladder = [
    {'scale_name':'schumann_clock_quantum_h_f0', 'energy_mev': h*f0/eV_J/1e6, 'type':'clock_quantum'},
    {'scale_name':'landauer_300K_bit', 'energy_mev': kB*300.0*math.log(2.0)/eV_J/1e6, 'type':'environment_dependent'},
    {'scale_name':'OI_weighted_landauer_300K', 'energy_mev': OI*kB*300.0*math.log(2.0)/eV_J/1e6, 'type':'environment_dependent_OI_weighted'},
    {'scale_name':'planck_energy', 'energy_mev': E_PLANCK_MEV, 'type':'non_mass_dimensional_normalizer'},
    {'scale_name':'OI_weighted_planck_energy', 'energy_mev': OI*E_PLANCK_MEV, 'type':'non_mass_dimensional_normalizer_OI_weighted'},
]
for sc in scale_ladder:
    sc['electron_Neff_linear_for_E_equals_scale_times_OI_N'] = TARGETS_MEV['electron']['energy_mev']/(sc['energy_mev']*OI) if sc['energy_mev'] else None
    sc['electron_action_S_for_E_equals_scale_exp_minus_S_over_OI'] = -OI*math.log(TARGETS_MEV['electron']['energy_mev']/sc['energy_mev']) if sc['energy_mev']>0 else None

stable_payload = {
    'equation':'E_i = E_P * exp(-S_i/OI)',
    'constants': {'c':c, 'h':h, 'hbar':hbar, 'G':G, 'eV_J':eV_J, 'OI':OI, 'L3':L3, 'f0':f0},
    'planck_energy_mev': E_PLANCK_MEV,
    'rows': rows,
    'pairs': pairs,
    'comparisons': comparisons,
}
fingerprint = hashlib.sha256(json.dumps(stable_payload, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()

result = {
    'schema':'METATIME_PLANCK_INFORMATION_ACTION_LEDGER_V6_1',
    'module':'61_planck_information_action_ledger_v6_1',
    'created_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),
    'technical_status':'PASS',
    'formal_status':'PASS_PLANCK_E0_LEDGER_INSTALLED',
    'substantive_status':'PLANCK_E0_IS_DIMENSIONALLY_STRONG_ACTION_TARGETS_NOT_DERIVED',
    'debt9_numeric_spectrum':'OPEN_NOT_CLOSED',
    'canon_allowed': False,
    'current_promotion':'DENY_CURRENT',
    'mass_prediction_claimed': False,
    'absolute_E0_derived': 'CANDIDATE_PLANCK_E0_DEFINED_NOT_PROVEN_AS_METATIME_E0',
    'formula_fingerprint_sha256': fingerprint,
    'core_equation': 'E_i = E_P * exp(-S_I(i)/OI); m_i = E_i/c^2',
    'constants': stable_payload['constants'],
    'planck_scale': {'E_planck_j':E_PLANCK_J, 'E_planck_ev':E_PLANCK_EV, 'E_planck_mev':E_PLANCK_MEV, 'm_planck_kg':m_PLANCK_KG},
    'target_action_rows': rows,
    'action_release_pairs': pairs,
    'existing_context_comparisons': comparisons,
    'scale_ladder': scale_ladder,
    'decision': {
        'planck_E0_candidate':'PROMOTE_TO_PRIMARY_DIMENSIONAL_CANDIDATE',
        'schumann_and_landauer_scales':'VALID_BUT_TOO_SMALL_OR_ENVIRONMENT_DEPENDENT_FOR_SM_E0',
        'linear_Neff_model_from_planck':'NOT_PREFERRED_AS_COUNT_BECAUSE_TARGETS_REQUIRE_FRACTIONAL_MICRO_OCCUPANCY',
        'exponential_action_gate_model':'PREFERRED_FOR_NEXT_DERIVATION_ATTEMPT',
        'debt9_closure':'DENIED',
        'next_step':'Derive S_I(i) from Collatz/Ramanujan/OI geometry and compare to this target ledger without using masses as input.'
    },
    'guardrails': {
        'reference_masses_used_only_as_target_ledger': True,
        'NoParamSM_used': False,
        'mass_prediction_claimed': False,
        'absolute_mass_scale_fit_to_targets': False,
        'canon_allowed': False,
    }
}
(OUT/'planck_information_action_ledger_v6_1.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
with (OUT/'planck_information_action_targets_v6_1.csv').open('w', newline='', encoding='utf-8') as f:
    fieldnames=['target','sector','reference_energy_mev_scoring_only','planck_energy_mev','ratio_E_over_Eplanck','required_information_action_S_for_Ep_exp_gate','linear_N_eff_if_E_equals_Ep_OI_N','linear_planck_mode_status','action_gate_status','mass_prediction_claimed','debt9_closure_claimed']
    w=csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
    for r in rows: w.writerow({k:r[k] for k in fieldnames})
with (OUT/'planck_information_action_releases_v6_1.csv').open('w', newline='', encoding='utf-8') as f:
    fieldnames=['pair','E_ratio_b_over_a','action_release_Sa_minus_Sb','OI_log_energy_ratio','interpretation','mass_prediction_claimed']
    w=csv.DictWriter(f, fieldnames=fieldnames); w.writeheader(); w.writerows(pairs)
print(json.dumps({'status':'PASS','fingerprint':fingerprint,'E_planck_mev':E_PLANCK_MEV}, indent=2))
