#!/usr/bin/env python3
"""
Debt 9 information-quantum dynamic-range bridge v2.7.

Purpose:
- treat kappa = ln(2)/(24*pi) as the quantum of informational preference fluctuation;
- audit the old Metatime tau/eigenvalue layer as a dynamic-range candidate;
- keep the old tau layer quarantined because old sources colocate tau with observed masses/fits;
- compute the missing preference-quanta required by the v2.6 one-anchor pilot.

This is not a numerical mass derivation. It is a bridge/audit module.
"""
from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(parents=True, exist_ok=True)

KAPPA = math.log(2.0) / (24.0 * math.pi)
ANCHOR = "e"
OLD_SOLVER = ROOT / "00_original_metatime/Metatime-main/simulations/Standard Model/full solver.py"
V26_PRED = ROOT / "24_debt9_one_anchor_mass_scaling_v2_6/results/one_anchor_mass_scaling_predictions_v2_6.csv"
ZH_CSV = ROOT / "18_preference_zeta_heisenberg_fluctuation_v2_0/results/preference_zeta_heisenberg_seed_diagnostics_v2_0.csv"
RAM_CSV = ROOT / "19_debt5_ramanujan_seed_suppression_v2_1/results/ramanujan_seed_suppression_table_v2_1.csv"


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs)/n; my = sum(ys)/n
    vx = sum((x-mx)**2 for x in xs); vy = sum((y-my)**2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys)) / math.sqrt(vx*vy)


def parse_old_solver():
    text = OLD_SOLVER.read_text(encoding="utf-8")
    oi_match = re.search(r"O_I\s*=\s*([0-9.]+)\s*#", text)
    old_oi = float(oi_match.group(1)) if oi_match else None
    pat = re.compile(r"'(?P<p>e|mu|tau|u|d|s|c|b|t)'\s*:\s*\{\s*'mass'\s*:\s*(?P<m>[0-9.eE+-]+),\s*'tau'\s*:\s*(?P<t>[0-9.eE+-]+)\s*\}")
    particles = {}
    for m in pat.finditer(text):
        particles[m.group('p')] = {
            'old_mass_value_mev_context': float(m.group('m')),
            'old_tau_eigenvalue': float(m.group('t')),
        }
    return old_oi, particles


def main():
    old_oi, old_particles = parse_old_solver()
    v26 = [r for r in read_csv(V26_PRED) if r['variant'] == 'EB_MINUS_RAMANUJAN_ZH_CENTER']
    zh = read_csv(ZH_CSV)
    ram = read_csv(RAM_CSV)

    anchor_row = next(r for r in v26 if r['fermion'] == ANCHOR)
    anchor_mass_pred = float(anchor_row['mass_pred_GeV'])
    anchor_target = float(anchor_row['target_mass_GeV_validation_only'])
    anchor_tau_old = old_particles[ANCHOR]['old_tau_eigenvalue']

    phase_uncertainties = [float(r['phase_uncertainty']) for r in zh]
    preference_widths = [float(r['preference_width']) for r in zh]
    ram_actions = [float(r['ramanujan_scaled_action']) for r in ram]

    rows = []
    for r in v26:
        f = r['fermion']
        tau_old = old_particles[f]['old_tau_eigenvalue']
        pred = float(r['mass_pred_GeV'])
        target = float(r['target_mass_GeV_validation_only'])
        required_log_release = math.log(target / pred)
        tau_log_relative = math.log(tau_old / anchor_tau_old)
        tau_log_abs = math.log(tau_old)
        # Express release demand in information-preference units. Because kappa is the quantum
        # in S, the exponent S/kappa is literally a count of preference quanta.
        required_action_shift = KAPPA * required_log_release
        tau_bridge_action_shift = KAPPA * tau_log_relative
        rows.append({
            'fermion': f,
            'class': r['class'],
            'generation': int(r['generation']),
            'seed_pair': r['seed_pair'],
            'old_tau_eigenvalue': tau_old,
            'old_tau_log_relative_to_electron': tau_log_relative,
            'old_tau_log_abs': tau_log_abs,
            'v26_pred_mass_GeV': pred,
            'target_mass_GeV_validation_only': target,
            'required_log_release_target_over_v26_pred_validation_only': required_log_release,
            'required_action_shift_kappa_units_validation_only': required_action_shift,
            'old_tau_bridge_action_shift_kappa_units': tau_bridge_action_shift,
            'old_tau_bridge_residual_quanta_validation_only': required_log_release - tau_log_relative,
            'anchor_used': ANCHOR,
            'uses_observed_mass_as_input': f == ANCHOR,
            'old_tau_promoted_to_model_input': False,
            'quarantine_reason': 'old tau table is colocated with observed masses/fitted old solvers; use as bridge candidate only',
        })

    non_anchor = [r for r in rows if r['fermion'] != ANCHOR]
    required = [float(r['required_log_release_target_over_v26_pred_validation_only']) for r in non_anchor]
    tau_rel = [float(r['old_tau_log_relative_to_electron']) for r in non_anchor]
    abs_res = [abs(float(r['old_tau_bridge_residual_quanta_validation_only'])) for r in non_anchor]

    old_tau_values = [r['old_tau_eigenvalue'] for r in old_particles.values()]
    target_values = [float(r['target_mass_GeV_validation_only']) for r in v26]
    pred_values = [float(r['mass_pred_GeV']) for r in v26]

    summary = {
        'module': 'debt9_information_quantum_dynamic_range_bridge_v2_7',
        'gate_class': 'AUDIT_BRIDGE_PASS',
        'debt9_closure_status': 'NOT_CLOSED_DYNAMIC_RANGE_BRIDGE_ONLY',
        'information_operator_status': 'kappa_ln2_over_24pi_is_preference_fluctuation_quantum',
        'kappa_ln2_over_24pi': KAPPA,
        'old_solver_O_I_literal': old_oi,
        'old_O_I_over_kappa': old_oi / KAPPA if old_oi else None,
        'relative_difference_old_O_I_vs_kappa': abs(old_oi-KAPPA)/KAPPA if old_oi else None,
        'zeta_heisenberg_phase_uncertainty_min': min(phase_uncertainties),
        'zeta_heisenberg_phase_uncertainty_median': median(phase_uncertainties),
        'zeta_heisenberg_phase_uncertainty_max': max(phase_uncertainties),
        'zeta_heisenberg_phase_uncertainty_in_kappa_units_median': median(phase_uncertainties)/KAPPA,
        'preference_width_median': median(preference_widths),
        'ramanujan_action_range': max(ram_actions) - min(ram_actions),
        'old_tau_dynamic_range': max(old_tau_values) / min(old_tau_values),
        'old_tau_log_dynamic_range': math.log(max(old_tau_values) / min(old_tau_values)),
        'target_mass_log_dynamic_range_validation_only': math.log(max(target_values) / min(target_values)),
        'v26_pred_mass_log_dynamic_range': math.log(max(pred_values) / min(pred_values)),
        'non_anchor_required_release_quanta_median_abs': median(abs(x) for x in required),
        'old_tau_bridge_residual_quanta_median_abs_validation_only': median(abs_res),
        'old_tau_required_release_pearson_non_anchor': pearson(tau_rel, required),
        'observed_masses_used_as_inputs': [ANCHOR],
        'old_tau_used_as_model_input': False,
        'conclusion': 'Old tau/eigenvalue has useful dynamic range but cannot be canonically imported until derived from v2.x CP1/Collatz/zeta/Ramanujan primitives without observed masses.',
    }

    with (OUT / 'old_tau_eigenvalue_bridge_audit_v2_7.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    with (OUT / 'information_quantum_dynamic_range_summary_v2_7.json').open('w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    # concise CSV summary for spreadsheet-free inspection
    with (OUT / 'information_quantum_dynamic_range_summary_v2_7.csv').open('w', newline='', encoding='utf-8') as f:
        keys = list(summary.keys())
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerow(summary)

    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
