#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metatime SM v3.3 — sector-basis / White-Thread operator skeleton.

Purpose:
- Recover the old-document sectorality without importing old fitted constants.
- Build a mass-blind operator interface between representation and mass action.
- Separate charged leptons, neutrinos, light quarks, and heavy quarks.
- Define CKM as a relative up/down basis rotation skeleton, not as PDG numbers.
- Define White-Thread as an open-path pair operator shape, not calibrated values.

No observed masses are read. No mass predictions are made.
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / 'results'
OUT.mkdir(parents=True, exist_ok=True)
KAPPA = math.log(2.0)/(24.0*math.pi)

# These are structural seed-channel assignments mined from old documents and
# rewritten in v2/v3 language. They are not mass inputs and not old fitted masses.
SECTORS = [
    {
        'sector_id': 'charged_lepton',
        'basis_family': 'lepton_basis',
        'seed_channel': '(3,5)',
        'old_document_status': 'recovered_channel_shape_not_fit_values',
        'operator_role': 'lepton_CP1_chiral_projection_channel',
        'color_channel': 'none',
        'heavy_resonance_channel': False,
        'white_thread_role': 'intra_lepton_phase_correlation_candidate',
        'ramanujan_role': 'sector_asymptotic_normalization',
        'information_operator_role': 'quantum_of_informational_preference_fluctuation',
        'fit_quarantine': False,
        'mass_prediction_allowed': False,
    },
    {
        'sector_id': 'neutrino',
        'basis_family': 'neutrino_pair_basis',
        'seed_channel': '(5,7)',
        'old_document_status': 'quarantined_PMNS_inputs_removed',
        'operator_role': 'pairwise_coherence_channel_for_later_PMNS',
        'color_channel': 'none',
        'heavy_resonance_channel': False,
        'white_thread_role': 'pairwise_neutrino_coherence_operator_shape_only',
        'ramanujan_role': 'suppression_and_pair_scale_guard',
        'information_operator_role': 'quantum_of_informational_preference_fluctuation',
        'fit_quarantine': True,
        'mass_prediction_allowed': False,
    },
    {
        'sector_id': 'light_quark',
        'basis_family': 'light_quark_basis',
        'seed_channel': '(11,13)',
        'old_document_status': 'recovered_channel_shape_QCD_scale_quarantined',
        'operator_role': 'light_color_tetrahedral_projection_channel',
        'color_channel': 'tetrahedral_color_triplet',
        'heavy_resonance_channel': False,
        'white_thread_role': 'light_quark_cycle_overlap_candidate',
        'ramanujan_role': 'color_asymptotic_scaling_not_fit_knob',
        'information_operator_role': 'quantum_of_informational_preference_fluctuation',
        'fit_quarantine': False,
        'mass_prediction_allowed': False,
    },
    {
        'sector_id': 'heavy_quark',
        'basis_family': 'heavy_quark_basis',
        'seed_channel': '(101,103)',
        'old_document_status': 'heavy_resonance_shape_recovered_old_scale_quarantined',
        'operator_role': 'deep_seed_heavy_resonance_channel',
        'color_channel': 'tetrahedral_color_triplet',
        'heavy_resonance_channel': True,
        'white_thread_role': 'heavy_cycle_open_path_holonomy_shape_only',
        'ramanujan_role': 'heavy_seed_asymptotic_gate_not_fit_knob',
        'information_operator_role': 'quantum_of_informational_preference_fluctuation',
        'fit_quarantine': True,
        'mass_prediction_allowed': False,
    },
]

# Fermion assignments are structural. The mode labels are from old-document hints
# but kept as candidate labels, not as fitted eigenvalues.
FERMIONS = [
    {'fermion':'e','generation':1,'sm_class':'charged_lepton','sector_id':'charged_lepton','basis_axis':'lepton_basis','basis_mode':'charged_lepton_first_harmonic_candidate','seed_channel':'(3,5)','mass_anchor_eligible':True,'mass_value_used_here':False},
    {'fermion':'mu','generation':2,'sm_class':'charged_lepton','sector_id':'charged_lepton','basis_axis':'lepton_basis','basis_mode':'charged_lepton_base_mode_candidate','seed_channel':'(3,5)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'tau','generation':3,'sm_class':'charged_lepton','sector_id':'charged_lepton','basis_axis':'lepton_basis','basis_mode':'charged_lepton_high_mode_candidate','seed_channel':'(3,5)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'nu1','generation':1,'sm_class':'neutrino','sector_id':'neutrino','basis_axis':'neutrino_pair_basis','basis_mode':'pairwise_coherence_mode_candidate','seed_channel':'(5,7)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'nu2','generation':2,'sm_class':'neutrino','sector_id':'neutrino','basis_axis':'neutrino_pair_basis','basis_mode':'pairwise_coherence_mode_candidate','seed_channel':'(5,7)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'nu3','generation':3,'sm_class':'neutrino','sector_id':'neutrino','basis_axis':'neutrino_pair_basis','basis_mode':'pairwise_coherence_mode_candidate','seed_channel':'(5,7)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'u','generation':1,'sm_class':'up_quark','sector_id':'light_quark','basis_axis':'up_light_basis','basis_mode':'light_up_cycle_candidate','seed_channel':'(11,13)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'d','generation':1,'sm_class':'down_quark','sector_id':'light_quark','basis_axis':'down_light_basis','basis_mode':'light_down_cycle_candidate','seed_channel':'(11,13)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'s','generation':2,'sm_class':'down_quark','sector_id':'light_quark','basis_axis':'down_light_basis','basis_mode':'light_strange_beta_resonance_candidate_quarantined','seed_channel':'(11,13)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'c','generation':2,'sm_class':'up_quark','sector_id':'heavy_quark','basis_axis':'up_heavy_basis','basis_mode':'heavy_charm_cycle_candidate','seed_channel':'(101,103)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'b','generation':3,'sm_class':'down_quark','sector_id':'heavy_quark','basis_axis':'down_heavy_basis','basis_mode':'heavy_bottom_cycle_candidate','seed_channel':'(101,103)','mass_anchor_eligible':False,'mass_value_used_here':False},
    {'fermion':'t','generation':3,'sm_class':'up_quark','sector_id':'heavy_quark','basis_axis':'up_heavy_basis','basis_mode':'heavy_top_resonant_cycle_candidate','seed_channel':'(101,103)','mass_anchor_eligible':False,'mass_value_used_here':False},
]

# CKM skeleton: pairwise basis relations only. No angles, no PDG values.
CKM_PAIRS = []
up = [f for f in FERMIONS if f['sm_class']=='up_quark']
down = [f for f in FERMIONS if f['sm_class']=='down_quark']
for u in up:
    for d in down:
        same_generation = u['generation'] == d['generation']
        same_sector = u['sector_id'] == d['sector_id']
        heavy_bridge = (u['sector_id'] == 'heavy_quark') or (d['sector_id'] == 'heavy_quark')
        CKM_PAIRS.append({
            'up_fermion': u['fermion'],
            'down_fermion': d['fermion'],
            'up_basis_axis': u['basis_axis'],
            'down_basis_axis': d['basis_axis'],
            'same_generation': same_generation,
            'same_sector_family': same_sector,
            'heavy_bridge': heavy_bridge,
            'basis_relation_type': 'relative_Berry_phase_rotation_skeleton',
            'white_thread_required': (not same_sector) or heavy_bridge,
            'ckm_numeric_value_allowed_here': False,
            'pdg_input_used': False,
        })

# White-Thread skeleton: formal pair operator shape, no calibrated F_ij.
WHITE_THREAD = []
for a in FERMIONS:
    for b in FERMIONS:
        if a['fermion'] >= b['fermion']:
            continue
        same_sector = a['sector_id'] == b['sector_id']
        cross_basis = a['basis_axis'] != b['basis_axis']
        if same_sector or cross_basis:
            WHITE_THREAD.append({
                'left': a['fermion'],
                'right': b['fermion'],
                'left_sector': a['sector_id'],
                'right_sector': b['sector_id'],
                'same_sector': same_sector,
                'cross_basis': cross_basis,
                'operator_shape': 'open_path_holonomy_correlation_kernel',
                'information_quantum': KAPPA,
                'information_role': 'quantum_of_informational_preference_fluctuation',
                'numeric_coupling_value_allowed_here': False,
                'fit_quarantine': True,
            })

def write_csv(path, rows):
    if not rows:
        return
    keys = list(rows[0].keys())
    with Path(path).open('w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader(); w.writerows(rows)

write_csv(OUT/'sector_basis_table_v3_3.csv', SECTORS)
write_csv(OUT/'fermion_sector_basis_assignment_v3_3.csv', FERMIONS)
write_csv(OUT/'ckm_relative_basis_skeleton_v3_3.csv', CKM_PAIRS)
write_csv(OUT/'white_thread_operator_skeleton_v3_3.csv', WHITE_THREAD)

summary = {
    'module':'31_debt9_sector_basis_white_thread_operator_v3_3',
    'gate_class':'PRE_MASS_SECTOR_BASIS_OPERATOR_PASS',
    'debt9_status':'not_rescored_in_this_module',
    'debt10_status':'ckm_pmns_operator_shapes_only_no_numeric_claim',
    'debt11_status':'sector_basis_operator_added_partial_advance',
    'observed_masses_used': False,
    'mass_predictions_made': False,
    'old_fit_values_imported': False,
    'old_document_structure_recovered': True,
    'sector_count': len(SECTORS),
    'fermion_assignment_count': len(FERMIONS),
    'ckm_pair_skeleton_count': len(CKM_PAIRS),
    'white_thread_pair_skeleton_count': len(WHITE_THREAD),
    'information_operator_role':'quantum_of_informational_preference_fluctuation',
    'information_quantum_ln2_over_24pi': KAPPA,
    'ramanujan_role':'sector_asymptotic_scaling_and_suppression_guard_not_fit_knob',
    'must_not_do_next':'do_not_rescore_masses_by_tuning_sector_constants',
    'allowed_next_step':'derive orientation/projection law for sector-basis operator OR run a strictly marked structural diagnostic with no masses',
    'do_not_claim':['Debt 9 closed','charged fermion masses derived','CKM numeric matrix derived','PMNS derived','White-Thread numerical couplings derived']
}
(OUT/'sector_basis_operator_summary_v3_3.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
