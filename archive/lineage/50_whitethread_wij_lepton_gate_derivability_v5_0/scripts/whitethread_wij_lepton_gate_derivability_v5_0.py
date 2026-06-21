#!/usr/bin/env python3
"""
Module 50 / v5.0: White-Thread W_ij charged-lepton gate derivability audit.

This executable does not predict masses and does not use observed mass tables.
It tests whether the strong charged-lepton screen/release factors reported in earlier
document diagnostics can be derived from the short-document White-Thread / W_ij layer.
"""
from __future__ import annotations
import csv, hashlib, json, math
from pathlib import Path

OIB = math.log(2.0)/(24.0*math.pi)
THETA = {'e': math.pi/6.0, 'mu': math.pi/4.0, 'tau': math.pi/3.0}
# Strict short-document kernel: F_ij = exp(OIB*(theta_j-theta_i)).
# Large document diagnostic table imported from v4.8 only as a target-to-derive, not as an input to a mass solver.
DOCUMENT_DIAGNOSTIC_F = {'e_to_mu': 0.145, 'e_to_tau': 0.302, 'mu_to_tau': 0.203}


def f_short(i: str, j: str) -> float:
    return math.exp(OIB*(THETA[j]-THETA[i]))


def required_oib_action_for_factor(factor: float) -> float:
    return math.log(factor)/OIB


def beta_required_for_factor(factor: float, delta_theta: float) -> float:
    if abs(delta_theta) < 1e-15:
        return float('nan')
    return math.log(factor)/(OIB*delta_theta)


def canonical_payload(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def main():
    outdir = Path(__file__).resolve().parents[1] / 'results'
    rows = []
    for pair, target in DOCUMENT_DIAGNOSTIC_F.items():
        i, _, j = pair.partition('_to_')
        dtheta = THETA[j] - THETA[i]
        strict = f_short(i, j)
        rows.append({
            'pair': pair,
            'theta_i_rad': THETA[i],
            'theta_j_rad': THETA[j],
            'delta_theta_rad': dtheta,
            'strict_short_doc_F': strict,
            'document_diagnostic_F_to_derive': target,
            'ratio_document_to_strict': target/strict,
            'required_OIB_action_quanta_for_document_F': required_oib_action_for_factor(target),
            'required_beta_in_exp_beta_OIB_delta_theta': beta_required_for_factor(target, dtheta),
            'short_doc_derives_document_F': False,
            'reason': 'strict W_ij/OIB short-doc layer is phase/promille-scale; strong diagnostic F requires extra path-integral/topological amplitude not specified by available short docs',
        })

    # General short-doc range if phase separation is bounded by 2π on a torus.
    max_short_amplification_2pi = math.exp(OIB * 2.0 * math.pi)
    max_short_suppression_2pi = math.exp(-OIB * 2.0 * math.pi)
    max_short_amplification_pi = math.exp(OIB * math.pi)
    max_short_suppression_pi = math.exp(-OIB * math.pi)

    result = {
        'schema': 'METATIME_WHITETHREAD_WIJ_LEPTON_GATE_DERIVABILITY_V5_0',
        'module': '50_whitethread_wij_lepton_gate_derivability_v5_0',
        'created_utc': '2026-06-21T00:00:00Z',
        'technical_status': 'PASS',
        'formal_status': 'PASS_WITH_STRICT_SOURCE_LEDGER',
        'substantive_status': 'NO_GO_FOR_STRONG_CHARGED_LEPTON_F_PROMOTION',
        'mass_prediction_claimed': False,
        'benchmark_performed': False,
        'observed_mass_input_used': False,
        'reference_spectrum_input_used': False,
        'constants': {'OIB_ln2_over_24pi': OIB, 'theta_assignments_rad': THETA},
        'white_thread_source_summary': {
            'W_ij_form': 'W_ij = exp(i integral_gamma_ij A)',
            'modulus_of_pure_phase_Wij': 1.0,
            'H_WT_form': 'Hermitian correlation-space Hamiltonian with Omega_ij |i><j| + h.c.',
            'Omega_ij_status': 'Omega_ij = Omega0 * f(|W_ij|, delta_arg_W_ij, ...); f is bounded but not explicitly derived in the available short docs',
            'consequence': 'unitary/open-path holonomy gives phase memory; a strong amplitude gate requires an additional explicit map f or path-integral evaluation',
        },
        'strict_short_doc_range': {
            'F_for_delta_theta_pi': {'min': max_short_suppression_pi, 'max': max_short_amplification_pi},
            'F_for_delta_theta_2pi': {'min': max_short_suppression_2pi, 'max': max_short_amplification_2pi},
            'interpretation': 'Short-doc OIB phase layer can produce only few-percent amplitude variation even across a full torus turn if used directly.'
        },
        'rows': rows,
        'decision': {
            'large_document_F_table_promoted': False,
            'strong_F_derivable_from_available_short_docs': False,
            'allowed_next_step': 'derive explicit White-Thread path-integral/amplitude map f before any charged-lepton benchmark or closure claim',
            'denied_next_step': 'using the large F table as a mass solver input or declaring it first-principles without reproducing the integration',
        },
        'taint_ledger': {
            'large_document_F_table': 'DIAGNOSTIC_TARGET_ONLY_NOT_PROMOTED',
            'global_beta_calibration': 'DENIED_AS_CLOSURE_IF_FITTED_TO_REFERENCE_DATA',
            'charged_lepton_polynomial': 'DENIED_AS_INPUT',
            'mass_tables': 'NOT_USED',
        },
        'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
        'canon_allowed': False,
        'current_promotion': 'DENY_CURRENT',
    }
    payload_for_hash = {k:v for k,v in result.items() if k != 'operator_audit_fingerprint_sha256'}
    result['operator_audit_fingerprint_sha256'] = hashlib.sha256(canonical_payload(payload_for_hash).encode('utf-8')).hexdigest()

    out_json = outdir / 'whitethread_wij_lepton_gate_derivability_v5_0.json'
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    out_csv = outdir / 'whitethread_wij_lepton_gate_derivability_v5_0.csv'
    with out_csv.open('w', newline='', encoding='utf-8') as f:
        fieldnames = list(rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)
    print(json.dumps({'status':'PASS','fingerprint':result['operator_audit_fingerprint_sha256']}, indent=2))

if __name__ == '__main__':
    main()
