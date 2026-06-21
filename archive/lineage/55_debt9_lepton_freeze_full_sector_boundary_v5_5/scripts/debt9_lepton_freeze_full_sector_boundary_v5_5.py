#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math, statistics
from pathlib import Path
from datetime import datetime, timezone

MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
OUT = MODULE / 'results'
OIB = math.log(2.0)/(24.0*math.pi)
L3 = 7.0
LEPTON_ORDER = ['e','mu','tau']
ANCHOR_SLOTS = {'e','u','c'}


def load_json(path: Path):
    with path.open(encoding='utf-8') as f:
        return json.load(f)


def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows):
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def sha_obj(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()


def component_gate(tau_row, root_policy: str = 'generation1_identity'):
    gen = int(tau_row['generation'])
    R = float(tau_row['ramanujan_resonance_release_component'])
    E = float(tau_row['ramanujan_entropy_component'])
    if root_policy == 'generation1_identity' and gen == 1:
        return 1.0, 1.0, 1.0
    damping = math.exp(-R)
    release = math.exp(OIB * L3 * E)
    return damping*release, damping, release


def main():
    v54 = load_json(ROOT/'54_debt9_ramanujan_component_split_lepton_refinement_v5_4'/'results'/'ramanujan_component_split_lepton_refinement_v5_4.json')
    v47 = load_json(ROOT/'47_debt9_sector_split_holonomy_operator_v4_7'/'results'/'sector_split_holonomy_operator_v4_7.json')
    tau_rows_all = read_csv(ROOT/'27_debt9_tau_v2_clean_information_eigenvalue_v2_9'/'results'/'tau_v2_structural_information_eigenvalue_table_v2_9.csv')
    tau_by_slot = {r['fermion']: r for r in tau_rows_all}

    frozen_formula = {
        'name': 'Debt9LeptonFreezeFullSectorBoundary_v5_5',
        'status': 'FREEZE_OF_V5_4_LEPTON_FORMULA_NO_MODIFICATION',
        'scope': 'charged-lepton formula frozen; full charged-fermion extension tested only as boundary probe',
        'lepton_formula': v54['frozen_formula']['formula'],
        'lepton_source_components': v54['frozen_formula']['source_components'],
        'blind_full_sector_extension_probe': {
            'input': 'v4.7 sector-split predictions for charged fermions',
            'gate': 'C_i = exp(-R_i) * exp(OIB * L3 * E_i), generation-1 identity policy',
            'R_i': 'tau_v2 ramanujan_resonance_release_component',
            'E_i': 'tau_v2 ramanujan_entropy_component',
            'policy': 'diagnostic only; not promoted when it worsens mixed quark sector',
        },
        'constants': {
            'OIB': 'ln2/(24*pi)',
            'L3': 7,
        },
        'boundaries': {
            'new_free_parameter_added': False,
            'operator_modified_after_v5_4': False,
            'observed_masses_used_in_operator': False,
            'reference_values_used_for_scoring_only': True,
            'mass_closure_claimed': False,
            'canon_allowed': False,
        },
    }

    formula_fingerprint = sha_obj(frozen_formula)

    # Charged-lepton freeze pass: exactly restate v5.4 rows and metrics, no new formula changes.
    lepton_rows = []
    lepton_errs = []
    for r in v54['rows']:
        out = {
            'slot': r['slot'],
            'generation': r['generation'],
            'predicted_mev_v5_5_frozen_lepton': r['predicted_mev_v5_4_diagnostic'],
            'benchmark_mev_post_freeze_scoring_only': r['benchmark_mev_post_freeze_scoring_only'],
            'absolute_relative_error': r['absolute_relative_error'],
            'ratio_pred_over_benchmark': r['ratio_pred_over_benchmark'],
            'component_split_gate': r['component_split_gate'],
            'formula_fingerprint_sha256': formula_fingerprint,
            'operator_modified_after_v5_4': False,
            'mass_closure_claimed': False,
            'canon_allowed': False,
        }
        lepton_rows.append(out)
        if r['slot'] != 'e':
            lepton_errs.append(float(r['absolute_relative_error']))

    # Boundary probe: blind universal application of v5.4 component gate to v4.7 full charged-fermion rows.
    full_rows = []
    blind_errs_excl_anchors = []
    base_errs_excl_anchors = []
    for r in v47['benchmark']['rows']:
        slot = r['slot']
        tau = tau_by_slot[slot]
        gate, damping, release = component_gate(tau, root_policy='generation1_identity')
        pred_v47 = float(r['predicted_mev_diagnostic'])
        pred_blind = pred_v47 * gate
        bench = float(r['benchmark_mev'])
        err_blind = abs(pred_blind/bench - 1.0)
        err_base = float(r['absolute_relative_error'])
        if slot not in ANCHOR_SLOTS:
            blind_errs_excl_anchors.append(err_blind)
            base_errs_excl_anchors.append(err_base)
        full_rows.append({
            'slot': slot,
            'family': r['family'],
            'tau_v2_class': tau['class'],
            'tau_v2_generation': tau['generation'],
            'v4_7_predicted_mev_input': pred_v47,
            'benchmark_mev_post_freeze_scoring_only': bench,
            'v4_7_absolute_relative_error': err_base,
            'component_gate_blind_universal': gate,
            'resonance_damping_gate': damping,
            'entropy_release_gate': release,
            'blind_extended_prediction_mev': pred_blind,
            'blind_extended_absolute_relative_error': err_blind,
            'blind_extension_improved_this_slot': err_blind < err_base,
            'unit_anchor_slot': slot in ANCHOR_SLOTS,
            'formula_fingerprint_sha256': formula_fingerprint,
            'mass_closure_claimed': False,
            'canon_allowed': False,
        })

    metrics = {
        'charged_leptons_v5_5_freeze_mean_error_excluding_e_anchor': statistics.mean(lepton_errs),
        'charged_leptons_v5_5_freeze_median_error_excluding_e_anchor': statistics.median(lepton_errs),
        'charged_leptons_v5_5_freeze_max_error_excluding_e_anchor': max(lepton_errs),
        'charged_leptons_closure_allowed': False,
        'v47_full_sector_mean_error_excluding_e_u_c_anchors': statistics.mean(base_errs_excl_anchors),
        'blind_v54_gate_full_sector_mean_error_excluding_e_u_c_anchors': statistics.mean(blind_errs_excl_anchors),
        'blind_extension_delta_mean_error_vs_v47': statistics.mean(blind_errs_excl_anchors) - statistics.mean(base_errs_excl_anchors),
        'blind_extension_passes_full_sector': False,
        'boundary_interpretation': 'v5.4 lepton formula is not a universal charged-fermion gate; quark sectors require their own already-justified sector maps rather than lepton gate reuse.',
    }

    result = {
        'schema': 'METATIME_DEBT9_LEPTON_FREEZE_FULL_SECTOR_BOUNDARY_V5_5',
        'module': '55_debt9_lepton_freeze_full_sector_boundary_v5_5',
        'created_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),
        'technical_status': 'PASS',
        'formal_status': 'PASS_WITH_EXPLICIT_SCOPE_BOUNDARY',
        'substantive_status': 'LEPTON_FREEZE_STRONG_FULL_SECTOR_NAIVE_EXTENSION_FAIL',
        'mass_closure_claimed': False,
        'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
        'canon_allowed': False,
        'current_promotion': 'DENY_CURRENT',
        'formula_fingerprint_sha256': formula_fingerprint,
        'frozen_formula': frozen_formula,
        'charged_lepton_rows': lepton_rows,
        'blind_full_charged_fermion_boundary_probe_rows': full_rows,
        'metrics': metrics,
        'decision': {
            'freeze_v5_4_lepton_formula': 'ACCEPT_AS_FROZEN_DIAGNOSTIC',
            'charged_lepton_status': 'STRONG_BUT_NOT_CLOSURE_DUE_TO_ELECTRON_UNIT_ANCHOR_AND_POST_V5_3_ORIGIN',
            'blind_full_sector_extension': 'FAIL_AND_DENY_PROMOTION',
            'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
            'next_step': 'Derive sector-specific unit-scale / quark normalization and electron-unit anchor removal; do not reuse lepton component gate as universal fermion gate.',
        },
        'taint_ledger': {
            'electron_unit_anchor': 'Still inherited; blocks no-parameter closure for charged leptons.',
            'quark_unit_anchors': 'u and c anchors remain diagnostic in v4.7 rows; full-sector closure denied.',
            'post_v5_3_origin': 'The v5.4 component split was introduced after residual analysis; v5.5 freezes it but does not retroactively convert it into blind prediction.',
            'reference_values': 'Benchmark values appear only in post-freeze scoring columns.',
            'old_solvers': 'No NoParamSM execution/import in active module.',
        },
    }

    OUT.mkdir(exist_ok=True)
    (OUT/'debt9_lepton_freeze_full_sector_boundary_v5_5.json').write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    write_csv(OUT/'debt9_v5_5_charged_lepton_freeze.csv', lepton_rows)
    write_csv(OUT/'debt9_v5_5_blind_full_sector_boundary_probe.csv', full_rows)
    print(json.dumps({
        'status': result['substantive_status'],
        'fingerprint': formula_fingerprint,
        'lepton_mean_error_excluding_e': metrics['charged_leptons_v5_5_freeze_mean_error_excluding_e_anchor'],
        'v47_full_mean_error_excluding_anchors': metrics['v47_full_sector_mean_error_excluding_e_u_c_anchors'],
        'blind_full_mean_error_excluding_anchors': metrics['blind_v54_gate_full_sector_mean_error_excluding_e_u_c_anchors'],
        'debt9_numeric_spectrum': result['debt9_numeric_spectrum'],
    }, indent=2))

if __name__ == '__main__':
    main()
