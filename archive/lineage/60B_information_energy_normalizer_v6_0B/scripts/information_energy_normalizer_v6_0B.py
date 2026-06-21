#!/usr/bin/env python3
"""
v6.0B: Information-energy normalizer.

This module formalizes the bridge:
    Einstein: E = m c^2
    Metatime candidate: m = M[I]
    therefore: E[I] = c^2 M[I]

It does not claim that information alone creates joules. Pure information is
normally dimensionless; a dimensional normalizer E0 is required.
"""
from __future__ import annotations
import csv, json, math, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parents[1]
OUT = MODULE_DIR/'results'
OUT.mkdir(parents=True, exist_ok=True)

# Exact SI constants where exact by definition.
c = 299_792_458.0                      # m/s
h = 6.626_070_15e-34                   # J*s
hbar = h/(2*math.pi)
kB = 1.380_649e-23                     # J/K
eV_J = 1.602_176_634e-19               # J
MeV_J = 1e6 * eV_J

# Project constants.
OI = math.log(2)/(24*math.pi)
f0 = 7.83
omega0 = 2*math.pi*f0
L3 = 7.0

# Reference masses are used only to measure required information count for known particles,
# not to set formula parameters.
reference_energies = {
    'electron_rest_energy': 0.510_998_95,   # MeV, scoring-only diagnostic
    'muon_rest_energy': 105.658_3755,
    'tau_rest_energy': 1776.86,
    'proton_rest_energy': 938.272_0813,
}

scales = []

def add_scale(name, energy_j, role, source_formula, status):
    scales.append({
        'scale_name': name,
        'energy_j': energy_j,
        'energy_ev': energy_j/eV_J,
        'energy_mev': energy_j/MeV_J,
        'mass_equivalent_kg': energy_j/(c*c),
        'role': role,
        'source_formula': source_formula,
        'status': status,
    })

# Pure OI is dimensionless: no J without E0.
add_scale('oscillator_quantum_h_f0', h*f0, 'candidate microscopic clock quantum', 'E0 = h * 7.83 Hz', 'dimensionally valid but far below SM scales')
add_scale('oscillator_quantum_hbar_omega0', hbar*omega0, 'same as h*f0', 'E0 = hbar * 2*pi*7.83 Hz', 'dimensionally valid but far below SM scales')
add_scale('landauer_bit_300K', kB*300.0*math.log(2), 'thermal information bit floor at 300 K', 'E_bit = kB*T*ln2', 'dimensionally valid environment-dependent scale')
add_scale('landauer_bit_2p725K', kB*2.725*math.log(2), 'thermal information bit floor at CMB-like temperature', 'E_bit = kB*T*ln2', 'dimensionally valid environment-dependent scale')
add_scale('OI_weighted_landauer_300K', kB*300.0*math.log(2)*OI, 'project OI-weighted thermal bit', 'E0 = kB*T*ln2*OI', 'dimensionally valid but T-dependent')
add_scale('OI_weighted_oscillator_h_f0', h*f0*OI, 'project OI-weighted oscillator quantum', 'E0 = h*f0*OI', 'dimensionally valid but tiny')

rows = []
for scale in scales:
    for label, mev in reference_energies.items():
        E = mev * MeV_J
        N_linear = E / scale['energy_j'] if scale['energy_j'] else None
        N_OI = E / (scale['energy_j'] * OI) if scale['energy_j'] else None
        rows.append({
            'scale_name': scale['scale_name'],
            'reference_label_scoring_only': label,
            'reference_energy_mev_scoring_only': mev,
            'scale_energy_mev': scale['energy_mev'],
            'required_N_if_E_equals_E0_times_N': N_linear,
            'required_N_if_E_equals_E0_times_OI_times_N': N_OI,
        })

formulae = {
    'minimal_bridge': 'E[I] = c^2 * M[I]',
    'linear_information_count': 'E[I] = E0 * OI * N_eff(I)',
    'action_gate': 'E_i = E0 * exp(-S_I(i)/OI)',
    'mass_from_information': 'm_i = (E0/c^2) * Phi(I_i)',
    'dimensional_obstruction': 'Pure dimensionless information cannot produce joules without E0, h*f, kB*T, field vacuum scale, or another dimensional normalizer.',
}

stable = {
    'formulae': formulae,
    'constants': {'c': c, 'h': h, 'kB': kB, 'OI': OI, 'f0': f0, 'omega0': omega0, 'L3': L3},
    'scales': scales,
    'diagnostic_rows': rows,
}
fingerprint = hashlib.sha256(json.dumps(stable, sort_keys=True).encode()).hexdigest()

result = {
    'schema': 'METATIME_INFORMATION_ENERGY_NORMALIZER_V6_0B',
    'module': '60B_information_energy_normalizer_v6_0B',
    'created_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'technical_status': 'PASS',
    'formal_status': 'PASS_DIMENSIONAL_BRIDGE_INSTALLED',
    'substantive_status': 'INFORMATION_ENERGY_FORMALISM_DEFINED_ABSOLUTE_E0_NOT_DERIVED',
    'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
    'canon_allowed': False,
    'current_promotion': 'DENY_CURRENT',
    'mass_prediction_claimed': False,
    'absolute_E0_derived': False,
    'formula_fingerprint_sha256': fingerprint,
    'core_statement': {
        'einstein': 'E = m c^2',
        'metatime_extension': 'm = M[I]',
        'combined': 'E[I] = c^2 M[I]',
        'recommended_candidate': 'E_i = E0 * exp(-S_I(i)/OI), with OI = ln2/(24*pi)',
    },
    'formulae': formulae,
    'constants': stable['constants'],
    'candidate_scales': scales,
    'diagnostic_required_information_counts': rows,
    'decision': {
        'information_to_energy_bridge': 'FORMALIZED',
        'pure_information_without_E0': 'DENIED_BY_DIMENSIONAL_ANALYSIS',
        'oscillator_7p83Hz_scale': 'VALID_BUT_TOO_SMALL_FOR_SM_WITHOUT_HUGE_N_eff',
        'landauer_scale': 'VALID_BUT_ENVIRONMENT_DEPENDENT',
        'absolute_SM_mass_scale': 'NOT_DERIVED',
        'next_step': 'Derive E0 from a non-mass physical/informational normalizer or define a sector-specific E0 ledger before using the formula for Debt 9.',
    },
    'guardrails': {
        'no_particle_mass_fit': True,
        'no_debt9_closure': True,
        'reference_energies_scoring_only': True,
        'no_claim_that_dimensionless_information_alone_has_units': True,
    },
}

(OUT/'information_energy_normalizer_v6_0B.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
with (OUT/'information_energy_required_counts_v6_0B.csv').open('w', newline='', encoding='utf-8') as f:
    fieldnames = list(rows[0].keys())
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader(); w.writerows(rows)
with (OUT/'information_energy_scales_v6_0B.csv').open('w', newline='', encoding='utf-8') as f:
    fieldnames = list(scales[0].keys())
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader(); w.writerows(scales)
print(json.dumps({'status':'PASS','fingerprint':fingerprint,'rows':len(rows)}, indent=2))
