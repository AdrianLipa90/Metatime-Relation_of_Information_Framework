#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debt 9 / v2.9: clean tau_v2 informational eigenvalue layer.

Build a frozen structural tau_v2 table from v2.x primitives before any
non-anchor mass re-scoring. This is not a mass derivation and it does not use
observed fermion masses.
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / 'results'
OUT.mkdir(parents=True, exist_ok=True)
KAPPA_I = math.log(2.0) / (24.0 * math.pi)
ANCHOR = 'e'
ACTION_CSV = ROOT / '14_debt3_debt6_zeta_polar_eb_action_v1_6/results/charged_fermion_eb_action_debt6_v1_6.csv'
ZH_CSV = ROOT / '18_preference_zeta_heisenberg_fluctuation_v2_0/results/preference_zeta_heisenberg_seed_diagnostics_v2_0.csv'
RAM_CSV = ROOT / '19_debt5_ramanujan_seed_suppression_v2_1/results/ramanujan_seed_suppression_table_v2_1.csv'
CLASS_RANK = {'charged_lepton': 1.0, 'down_quark': 2.0, 'up_quark': 3.0}

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))

def ffloat(row, key):
    return float(row[key])

def seed_pair(row):
    return (int(float(row['seed_p'])), int(float(row['seed_q'])))

def collatz(n: int) -> int:
    return n // 2 if n % 2 == 0 else 3*n + 1

def collatz_orbit(n: int, max_steps: int = 512):
    out = [n]
    while out[-1] != 1 and len(out) < max_steps:
        out.append(collatz(out[-1]))
    return out

def terminal_axis_signature(pair):
    p, q = pair
    op, oq = collatz_orbit(p), collatz_orbit(q)
    step = 0.5 * (len(op) + len(oq))
    peak = math.log1p(max(max(op), max(oq)))
    terminal_credit = math.log(4.0) + math.log(2.0) + math.log(1.0 + 0.5)
    return math.log1p(step + peak + terminal_credit)

def safe_norm(values, x):
    lo, hi = min(values), max(values)
    if hi == lo:
        return 0.0
    return (x - lo) / (hi - lo)

def main():
    action = read_csv(ACTION_CSV)
    zh = {seed_pair(r): r for r in read_csv(ZH_CSV)}
    ram = {seed_pair(r): r for r in read_csv(RAM_CSV)}
    merged = []
    for r in action:
        pair = seed_pair(r)
        if pair not in zh or pair not in ram:
            continue
        z = zh[pair]; rr = ram[pair]
        cls = r['class']
        merged.append({
            'fermion': r['fermion'], 'class': cls, 'generation': int(r['generation']),
            'seed_p': pair[0], 'seed_q': pair[1], 'seed_product': pair[0]*pair[1],
            'eb_action_unit_v16': ffloat(r, 'eb_action_unit_v16'),
            'eb_action_kappa_v16': ffloat(r, 'eb_action_kappa_v16'),
            'zeta_spacing_norm': ffloat(z, 'spacing_norm'),
            'zeta_phase_uncertainty': ffloat(z, 'phase_uncertainty'),
            'zeta_preference_width': ffloat(z, 'preference_width'),
            'ramanujan_entropy_norm': ffloat(rr, 'hardy_ramanujan_entropy_norm'),
            'ramanujan_resonance': ffloat(rr, 'ramanujan_resonance'),
            'ramanujan_scaled_action': ffloat(rr, 'ramanujan_scaled_action'),
            'ramanujan_visibility': ffloat(rr, 'visibility'),
            'class_rank_structural': CLASS_RANK[cls],
            'terminal_axis_signature': terminal_axis_signature(pair),
            'observed_mass_used': False, 'old_tau_used': False,
        })
    eb_vals = [r['eb_action_unit_v16'] for r in merged]
    ent_vals = [r['ramanujan_entropy_norm'] for r in merged]
    res_vals = [r['ramanujan_resonance'] for r in merged]
    sig_vals = [r['terminal_axis_signature'] for r in merged]
    spacing_vals = [r['zeta_spacing_norm'] for r in merged]
    width_vals = [r['zeta_preference_width'] for r in merged]
    class_vals = [r['class_rank_structural'] for r in merged]
    rows = []
    for r in merged:
        killing_eb_component = safe_norm(eb_vals, r['eb_action_unit_v16'])
        ramanujan_entropy_component = safe_norm(ent_vals, r['ramanujan_entropy_norm'])
        ramanujan_resonance_component = 1.0 - safe_norm(res_vals, r['ramanujan_resonance'])
        collatz_terminal_component = safe_norm(sig_vals, r['terminal_axis_signature'])
        zeta_spacing_component = safe_norm(spacing_vals, r['zeta_spacing_norm'])
        zeta_width_component = safe_norm(width_vals, r['zeta_preference_width'])
        representation_component = safe_norm(class_vals, r['class_rank_structural'])
        raw = (killing_eb_component + ramanujan_entropy_component + ramanujan_resonance_component +
               collatz_terminal_component + 0.5*zeta_spacing_component + 0.5*zeta_width_component +
               representation_component)
        rows.append({**r,
            'kappa_information_quantum': KAPPA_I,
            'killing_eb_component': killing_eb_component,
            'ramanujan_entropy_component': ramanujan_entropy_component,
            'ramanujan_resonance_release_component': ramanujan_resonance_component,
            'collatz_terminal_axis_component': collatz_terminal_component,
            'zeta_spacing_component': zeta_spacing_component,
            'zeta_width_component': zeta_width_component,
            'representation_component': representation_component,
            'tau_v2_action': raw,
            'tau_v2_preference_quanta': raw / KAPPA_I,
            'formula_frozen_before_mass_rescore': True,
            'observed_mass_used': False,
            'old_tau_used': False})
    anchor_tau = next(r for r in rows if r['fermion'] == ANCHOR)['tau_v2_preference_quanta']
    for r in rows:
        r['tau_v2_relative_to_electron_quanta'] = r['tau_v2_preference_quanta'] - anchor_tau
    tau_vals = [r['tau_v2_preference_quanta'] for r in rows]
    by_class = {}
    for cls in sorted({r['class'] for r in rows}):
        cr = sorted([r for r in rows if r['class'] == cls], key=lambda x: x['generation'])
        rels = [r['tau_v2_relative_to_electron_quanta'] for r in cr]
        by_class[cls] = {'generation_order_non_decreasing': all(rels[i] <= rels[i+1] for i in range(len(rels)-1)), 'tau_v2_relative_values': rels}
    summary = {
        'module': 'debt9_tau_v2_clean_information_eigenvalue_v2_9',
        'gate_class': 'PRE_MASS_RESCORING_STRUCTURAL_PASS',
        'debt9_status': 'dynamic_range_layer_frozen_but_not_mass_validated',
        'kappa_information_quantum_ln2_over_24pi': KAPPA_I,
        'information_operator_role': 'quantum_of_informational_preference_fluctuation',
        'observed_masses_used': False,
        'old_tau_used': False,
        'formula_frozen_before_mass_rescore': True,
        'tau_v2_min_quanta': min(tau_vals), 'tau_v2_median_quanta': median(tau_vals),
        'tau_v2_max_quanta': max(tau_vals), 'tau_v2_dynamic_range_quanta': max(tau_vals)-min(tau_vals),
        'class_generation_order_diagnostics': by_class,
        'next_allowed_step': 'rerun_one_anchor_mass_scaling_with_tau_v2_as_frozen_structural_layer_without_changing_tau_formula',
        'do_not_claim': ['Debt 9 numerically closed','charged fermion masses derived','tau_v2 validated against observed masses','old tau table promoted'],
    }
    with (OUT/'tau_v2_structural_information_eigenvalue_table_v2_9.csv').open('w', newline='', encoding='utf-8') as fh:
        w=csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with (OUT/'tau_v2_structural_information_eigenvalue_summary_v2_9.json').open('w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2)
    with (OUT/'tau_v2_structural_information_eigenvalue_summary_v2_9.csv').open('w', newline='', encoding='utf-8') as fh:
        w=csv.DictWriter(fh, fieldnames=list(summary.keys())); w.writeheader(); w.writerow(summary)
    print(json.dumps(summary, indent=2))
if __name__ == '__main__': main()
