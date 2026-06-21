#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metatime SM v3.1 — frozen sector projection operator.

Purpose:
- Convert the Debt 11 chiral representation table into a mass-blind sector
  projection operator before any new Debt 9 mass rescore.
- Merge the frozen projection with tau_v2 as a pre-mass surface only.
- Do not read observed masses or validation targets.
- Do not claim a mass result.
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from fractions import Fraction
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / 'results'
OUT.mkdir(parents=True, exist_ok=True)
KAPPA = math.log(2.0)/(24.0*math.pi)
REP_TABLE = ROOT/'28_debt11_chiral_representation_projection_v3_0/results/chiral_representation_table_v3_0.csv'
TAU_TABLE = ROOT/'27_debt9_tau_v2_clean_information_eigenvalue_v2_9/results/tau_v2_structural_information_eigenvalue_table_v2_9.csv'
ANCHOR = 'e'

SECTOR_CHANNELS = {
    'charged_lepton': ('e_L', 'e_R'),
    'down_quark': ('d_L', 'd_R'),
    'up_quark': ('u_L', 'u_R'),
}
HIGGS_GATE_ORIENTATION = {
    'barL_H_eR_allowed': 'ordinary_H',
    'barQ_H_dR_allowed': 'ordinary_H',
    'barQ_Htilde_uR_allowed': 'conjugate_Htilde',
}
CP1_ORIENTATION = {
    'charged_lepton': 'south_lower_pole_to_singlet',
    'down_quark': 'south_lower_pole_to_singlet',
    'up_quark': 'north_upper_pole_to_singlet_conjugate_gate',
}

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))

def parse_fraction(x: str) -> Fraction:
    x = str(x).strip()
    if '/' in x:
        a,b = x.split('/',1)
        return Fraction(int(a), int(b))
    return Fraction(x)

def frac_str(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

def main():
    rep_rows = {r['particle_id']: r for r in read_csv(REP_TABLE)}
    tau_rows = read_csv(TAU_TABLE)
    sectors = []
    for sector, (left_id, right_id) in SECTOR_CHANNELS.items():
        L, R = rep_rows[left_id], rep_rows[right_id]
        YL, YR = parse_fraction(L['hypercharge']), parse_fraction(R['hypercharge'])
        color = int(L['color_multiplicity'])
        hyp_norm = math.sqrt(float(YL*YL + YR*YR))
        color_norm = math.sqrt(float(color))
        # This is a frozen representation geometry norm, not a mass fit.
        rep_norm = hyp_norm * color_norm
        sectors.append({
            'sector': sector,
            'left_channel': left_id,
            'right_channel': right_id,
            'left_cp1_pole': L['cp1_pole'],
            'right_cp1_pole': R['cp1_pole'],
            'left_t3': L['t3'],
            'right_t3': R['t3'],
            'left_hypercharge': frac_str(YL),
            'right_hypercharge': frac_str(YR),
            'hypercharge_path_norm': hyp_norm,
            'color_multiplicity': color,
            'color_norm_sqrt_multiplicity': color_norm,
            'higgs_gate': R['higgs_gate'],
            'higgs_gate_orientation': HIGGS_GATE_ORIENTATION.get(R['higgs_gate'], 'unknown'),
            'cp1_transition_orientation': CP1_ORIENTATION[sector],
            'representation_projection_norm': rep_norm,
            'information_quantum': KAPPA,
            'information_operator_role': 'quantum_of_informational_preference_fluctuation',
            'zeta_axis_role': 'imaginary_zero_axis_constraints_CP1_pole_and_singlet_transition',
            'ramanujan_role': 'asymptotic_scaling_layer_not_fit_knob',
            'observed_masses_used': False,
            'mass_rescore_allowed_in_this_module': False,
        })
    anchor_norm = next(s for s in sectors if s['sector']=='charged_lepton')['representation_projection_norm']
    for s in sectors:
        s['representation_projection_relative_to_charged_lepton'] = s['representation_projection_norm']/anchor_norm
        # The logarithmic projection is recorded for later rescore, not applied to masses here.
        s['log_projection_relative_to_charged_lepton'] = math.log(s['representation_projection_relative_to_charged_lepton'])
    sector_map = {s['sector']: s for s in sectors}
    rows = []
    for r in tau_rows:
        sector = r['class']
        if sector not in sector_map:
            continue
        s = sector_map[sector]
        tau_quanta = float(r['tau_v2_preference_quanta'])
        tau_rel = float(r['tau_v2_relative_to_electron_quanta'])
        proj_rel = float(s['representation_projection_relative_to_charged_lepton'])
        log_proj = float(s['log_projection_relative_to_charged_lepton'])
        rows.append({
            'fermion': r['fermion'],
            'class': sector,
            'generation': int(r['generation']),
            'seed_p': r['seed_p'],
            'seed_q': r['seed_q'],
            'sector_projection_relative_to_charged_lepton': proj_rel,
            'sector_log_projection_relative_to_charged_lepton': log_proj,
            'tau_v2_preference_quanta': tau_quanta,
            'tau_v2_relative_to_electron_quanta': tau_rel,
            'projected_tau_v3_1_quanta': tau_quanta * proj_rel,
            'projected_tau_v3_1_relative_to_electron_quanta_pre_anchor_shift': tau_rel * proj_rel,
            'projected_information_action_v3_1': KAPPA * tau_quanta * proj_rel,
            'projected_relative_information_action_v3_1': KAPPA * tau_rel * proj_rel,
            'higgs_gate_orientation': s['higgs_gate_orientation'],
            'cp1_transition_orientation': s['cp1_transition_orientation'],
            'information_operator_role': 'quantum_of_informational_preference_fluctuation',
            'observed_masses_used': False,
            'old_tau_used': False,
            'mass_prediction_made': False,
        })
    anchor_projected = next(r for r in rows if r['fermion'] == ANCHOR)['projected_tau_v3_1_quanta']
    for r in rows:
        r['projected_tau_v3_1_relative_to_electron_quanta'] = r['projected_tau_v3_1_quanta'] - anchor_projected
    by_class = {}
    for cls in sorted({r['class'] for r in rows}):
        cr = sorted([r for r in rows if r['class']==cls], key=lambda x:x['generation'])
        vals = [r['projected_tau_v3_1_relative_to_electron_quanta'] for r in cr]
        by_class[cls] = {
            'projected_tau_relative_values': vals,
            'non_decreasing': all(vals[i] <= vals[i+1] for i in range(len(vals)-1)),
            'non_increasing': all(vals[i] >= vals[i+1] for i in range(len(vals)-1)),
        }
    dyn_vals = [r['projected_tau_v3_1_relative_to_electron_quanta'] for r in rows]
    summary = {
        'module': '29_debt9_debt11_frozen_sector_projection_operator_v3_1',
        'gate_class': 'PRE_MASS_PROJECTION_OPERATOR_PASS',
        'debt11_status': 'one_generation_chiral_table_extended_to_frozen_sector_projection_operator',
        'debt9_status': 'not_rescored_in_this_module',
        'observed_masses_used': False,
        'target_mass_csv_read': False,
        'old_tau_used': False,
        'mass_predictions_made': False,
        'anchor_for_relative_projection': ANCHOR,
        'kappa_information_quantum_ln2_over_24pi': KAPPA,
        'information_operator_role': 'quantum_of_informational_preference_fluctuation',
        'sector_count': len(sectors),
        'fermion_row_count': len(rows),
        'projected_tau_relative_min_quanta': min(dyn_vals),
        'projected_tau_relative_median_quanta': median(dyn_vals),
        'projected_tau_relative_max_quanta': max(dyn_vals),
        'projected_tau_relative_dynamic_range_quanta': max(dyn_vals)-min(dyn_vals),
        'generation_order_diagnostics_mass_blind': by_class,
        'allowed_next_step': 'one_anchor_mass_rescore_using_frozen_v3_1_projection_without_editing_operator',
        'do_not_claim': ['Debt 9 closed', 'masses derived', 'CKM/PMNS derived', 'sector projection validated by masses'],
    }
    with (OUT/'sector_projection_operator_v3_1.csv').open('w', newline='', encoding='utf-8') as fh:
        w=csv.DictWriter(fh, fieldnames=list(sectors[0].keys())); w.writeheader(); w.writerows(sectors)
    with (OUT/'fermion_projected_tau_surface_v3_1.csv').open('w', newline='', encoding='utf-8') as fh:
        w=csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with (OUT/'sector_projection_operator_summary_v3_1.json').open('w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))
if __name__ == '__main__':
    main()
