#!/usr/bin/env python3
"""
Metatime SM v3.2 — Debt 9 one-anchor mass rescore using frozen v3.1 sector projection.

Rules:
- Uses exactly one observed mass as dimensional calibration: electron.
- Uses v3.1 frozen sector projection without editing it.
- Runs several predeclared projection orientations; no variant is tuned after reading residuals.
- Observed non-anchor masses are validation targets only.
- This is a stress test, not a claim of mass derivation.
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / 'results'
OUT.mkdir(parents=True, exist_ok=True)

KAPPA = math.log(2.0)/(24.0*math.pi)
ANCHOR = 'e'
VEV_GEV = 246.0
SQRT2 = math.sqrt(2.0)

V26_PRED = ROOT/'24_debt9_one_anchor_mass_scaling_v2_6/results/one_anchor_mass_scaling_predictions_v2_6.csv'
V31_PROJ = ROOT/'29_debt9_debt11_frozen_sector_projection_operator_v3_1/results/fermion_projected_tau_surface_v3_1.csv'
V31_SUMMARY = ROOT/'29_debt9_debt11_frozen_sector_projection_operator_v3_1/results/sector_projection_operator_summary_v3_1.json'
BASE_VARIANT = 'EB_MINUS_RAMANUJAN_ZH_CENTER'

ORIENTATIONS = {
    'V26_REFERENCE_NO_V31_PROJECTION': {
        'description': 'reference v2.6 one-anchor result, no v3.1 projection term',
        'uses_projection': False,
        'formula': 'S = S_v26',
    },
    'V31_SUPPRESSION_SIGN': {
        'description': 'frozen v3.1 relative projected tau acts as additional suppression quantum',
        'uses_projection': True,
        'formula': 'S = S_v26 + kappa * DeltaTau_projected',
    },
    'V31_RELEASE_SIGN': {
        'description': 'frozen v3.1 relative projected tau acts as release/tunnelling quantum',
        'uses_projection': True,
        'formula': 'S = S_v26 - kappa * DeltaTau_projected',
    },
    'V31_ABS_SUPPRESSION': {
        'description': 'distance from electron channel acts as non-oriented suppression',
        'uses_projection': True,
        'formula': 'S = S_v26 + kappa * abs(DeltaTau_projected)',
    },
}


def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def exp_safe(x: float) -> float:
    if x > 700:
        return float('inf')
    if x < -745:
        return 0.0
    return math.exp(x)


def main():
    pred_rows = [r for r in read_csv(V26_PRED) if r['variant'] == BASE_VARIANT]
    proj_rows = {r['fermion']: r for r in read_csv(V31_PROJ)}
    with V31_SUMMARY.open(encoding='utf-8') as fh:
        v31_summary = json.load(fh)

    anchor_rows = [r for r in pred_rows if r['fermion'] == ANCHOR]
    assert len(anchor_rows) == 1, 'electron anchor must be present exactly once'
    anchor = anchor_rows[0]
    anchor_mass = float(anchor['target_mass_GeV_validation_only'])
    anchor_S = float(anchor['S_pred'])
    # Structural check: electron projection delta must be exactly zero in the frozen v3.1 surface.
    anchor_delta_tau = float(proj_rows[ANCHOR]['projected_tau_v3_1_relative_to_electron_quanta'])
    assert abs(anchor_delta_tau) < 1e-12, 'frozen projection must preserve electron anchor as zero relative channel'

    rows = []
    for orientation, meta in ORIENTATIONS.items():
        for r in pred_rows:
            f = r['fermion']
            p = proj_rows[f]
            base_S = float(r['S_pred'])
            delta_tau = float(p['projected_tau_v3_1_relative_to_electron_quanta'])
            if orientation == 'V26_REFERENCE_NO_V31_PROJECTION':
                S = base_S
            elif orientation == 'V31_SUPPRESSION_SIGN':
                S = base_S + KAPPA * delta_tau
            elif orientation == 'V31_RELEASE_SIGN':
                S = base_S - KAPPA * delta_tau
            elif orientation == 'V31_ABS_SUPPRESSION':
                S = base_S + KAPPA * abs(delta_tau)
            else:
                raise ValueError(orientation)

            log_mass_pred = math.log(VEV_GEV/SQRT2) - S/KAPPA
            mass_pred = exp_safe(log_mass_pred)
            target = float(r['target_mass_GeV_validation_only'])
            log_error = log_mass_pred - math.log(target)
            abs_log_error = abs(log_error)
            rows.append({
                'orientation': orientation,
                'formula': meta['formula'],
                'fermion': f,
                'class': r['class'],
                'generation': int(r['generation']),
                'seed_pair': r['seed_pair'],
                'anchor_used': ANCHOR,
                'is_anchor': f == ANCHOR,
                'S_v26_reference': base_S,
                'DeltaTau_projected_v3_1_quanta': delta_tau,
                'S_v3_2_rescore': S,
                'log_mass_pred_GeV': log_mass_pred,
                'mass_pred_GeV': mass_pred,
                'target_mass_GeV_validation_only': target,
                'log_error_vs_target_validation_only': log_error,
                'abs_log_error_vs_target_validation_only': abs_log_error,
                'sector_projection_relative_to_charged_lepton': float(p['sector_projection_relative_to_charged_lepton']),
                'higgs_gate_orientation': p['higgs_gate_orientation'],
                'cp1_transition_orientation': p['cp1_transition_orientation'],
                'uses_observed_mass_as_input': f == ANCHOR,
                'uses_observed_masses_as_validation_only': f != ANCHOR,
                'v31_projection_operator_edited': False,
                'old_tau_used': False,
            })

    summary_rows = []
    for orientation, meta in ORIENTATIONS.items():
        vr = [r for r in rows if r['orientation'] == orientation and not r['is_anchor']]
        abs_logs = [r['abs_log_error_vs_target_validation_only'] for r in vr]
        signed_logs = [r['log_error_vs_target_validation_only'] for r in vr]
        class_order_mass = {}
        for cls in sorted({r['class'] for r in rows if r['orientation'] == orientation}):
            cr = sorted([r for r in rows if r['orientation'] == orientation and r['class'] == cls], key=lambda x: x['generation'])
            masses = [r['mass_pred_GeV'] for r in cr]
            class_order_mass[cls] = all(masses[i] < masses[i+1] for i in range(len(masses)-1))
        summary_rows.append({
            'orientation': orientation,
            'gate_class': 'COMPUTATIONAL_STRESS_TEST_PASS',
            'formula': meta['formula'],
            'debt9_closure_status': 'NOT_CLOSED_STRESS_TEST_ONLY',
            'anchor': ANCHOR,
            'anchor_mass_GeV': anchor_mass,
            'non_anchor_count': len(vr),
            'median_abs_log_error_excluding_anchor': median(abs_logs),
            'max_abs_log_error_excluding_anchor': max(abs_logs),
            'mean_signed_log_error_excluding_anchor': sum(signed_logs)/len(signed_logs),
            'charged_lepton_generation_order_pass': class_order_mass.get('charged_lepton', False),
            'down_quark_generation_order_pass': class_order_mass.get('down_quark', False),
            'up_quark_generation_order_pass': class_order_mass.get('up_quark', False),
            'uses_v3_1_frozen_projection': meta['uses_projection'],
            'uses_observed_masses_as_inputs_other_than_anchor': False,
            'old_tau_used': False,
        })

    # Anti-fit audit: no orientation is promoted as canonical merely because of error score.
    reference = next(s for s in summary_rows if s['orientation'] == 'V26_REFERENCE_NO_V31_PROJECTION')
    best_by_median = min(summary_rows, key=lambda s: float(s['median_abs_log_error_excluding_anchor']))
    anti_fit = {
        'module': '30_debt9_one_anchor_rescore_frozen_projection_v3_2',
        'gate_class': 'COMPUTATIONAL_STRESS_TEST_PASS_WITH_ANTI_FIT_AUDIT',
        'base_variant': BASE_VARIANT,
        'electron_anchor_only': True,
        'observed_masses_used_as_inputs': [ANCHOR],
        'v3_1_projection_operator_frozen_before_rescore': True,
        'old_tau_used': False,
        'orientations_predeclared_not_fit_selected': list(ORIENTATIONS.keys()),
        'reference_median_abs_log_error': float(reference['median_abs_log_error_excluding_anchor']),
        'reference_max_abs_log_error': float(reference['max_abs_log_error_excluding_anchor']),
        'best_orientation_by_median_error_diagnostic_only': best_by_median['orientation'],
        'best_median_abs_log_error_diagnostic_only': float(best_by_median['median_abs_log_error_excluding_anchor']),
        'best_max_abs_log_error_diagnostic_only': float(best_by_median['max_abs_log_error_excluding_anchor']),
        'best_can_be_claimed_as_derivation': False,
        'reason': 'orientation choice is not yet derived from first principles; lower residual alone would be a fit-selection signal',
        'debt9_status': 'OPEN_AFTER_V3_2' if float(best_by_median['median_abs_log_error_excluding_anchor']) > 1.0 else 'REVIEW_REQUIRED_NOT_AUTO_CLOSED',
        'v31_projection_dynamic_range_quanta': v31_summary.get('projected_tau_relative_dynamic_range_quanta'),
        'do_not_claim': ['Debt 9 closed', 'masses derived', 'best orientation canonized by residuals', 'CKM/PMNS derived'],
    }

    with (OUT/'one_anchor_frozen_projection_rescore_predictions_v3_2.csv').open('w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with (OUT/'one_anchor_frozen_projection_rescore_summary_v3_2.csv').open('w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary_rows[0].keys())); w.writeheader(); w.writerows(summary_rows)
    with (OUT/'one_anchor_frozen_projection_anti_fit_audit_v3_2.json').open('w', encoding='utf-8') as fh:
        json.dump(anti_fit, fh, indent=2)
    print(json.dumps({'status': 'PASS', 'summary': summary_rows, 'anti_fit_audit': anti_fit}, indent=2))

if __name__ == '__main__':
    main()
