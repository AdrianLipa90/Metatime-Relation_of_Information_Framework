#!/usr/bin/env python3
"""
METATIME / Standard Model derivation v4.3
Debt 9 continuation: frozen PDG-free Metatime mass/flavour operator candidate.

This script DOES NOT benchmark against observed masses and DOES NOT predict physical masses.
It freezes a deterministic, dimensionless operator trace M_MT from structural inputs only,
so a later module can perform a single sealed benchmark without changing the operator.

Allowed ingredients in this active executable:
- integer fermion slot labels
- chirality/sector labels inherited from the SM skeleton
- information fluctuation quantum q_I = ln(2)/(24*pi)
- Collatz orbit diagnostics on structural integer seeds
- Ramanujan eta-product scale signature, evaluated as a q-series at q=exp(-2*pi)
- tetrahedral/triplet generation geometry markers

Forbidden in this active executable:
- observed particle masses or reference mass tables
- PDG tables or imports from archived reference-solvers
- CKM/PMNS numerical matrices
- post-hoc fitting or residual minimization
"""
from __future__ import annotations
import csv, json, math, pathlib
from typing import Dict, List, Tuple

OUT = pathlib.Path(__file__).resolve().parents[1] / 'results'

Q_INFO = math.log(2.0) / (24.0 * math.pi)
Q_RAM = math.exp(-2.0 * math.pi)  # Ramanujan/modular q scale; mathematical, not experimental.

# Minimal charged-fermion slots from SM Yukawa boundary. No observed masses here.
# hypercharge values are structural SM quantum numbers from the gauge/chiral layer, not masses.
FERMION_SLOTS = [
    {"slot":"e",   "family":"charged_lepton", "generation":1, "left_Y_num":-1, "left_Y_den":2, "right_Y_num":-1, "right_Y_den":1, "weak_doublet":1, "color_dim":1, "tetra_mode":1},
    {"slot":"mu",  "family":"charged_lepton", "generation":2, "left_Y_num":-1, "left_Y_den":2, "right_Y_num":-1, "right_Y_den":1, "weak_doublet":1, "color_dim":1, "tetra_mode":2},
    {"slot":"tau", "family":"charged_lepton", "generation":3, "left_Y_num":-1, "left_Y_den":2, "right_Y_num":-1, "right_Y_den":1, "weak_doublet":1, "color_dim":1, "tetra_mode":3},
    {"slot":"u",   "family":"up_quark",       "generation":1, "left_Y_num":1,  "left_Y_den":6, "right_Y_num":2,  "right_Y_den":3, "weak_doublet":1, "color_dim":3, "tetra_mode":1},
    {"slot":"c",   "family":"up_quark",       "generation":2, "left_Y_num":1,  "left_Y_den":6, "right_Y_num":2,  "right_Y_den":3, "weak_doublet":1, "color_dim":3, "tetra_mode":2},
    {"slot":"t",   "family":"up_quark",       "generation":3, "left_Y_num":1,  "left_Y_den":6, "right_Y_num":2,  "right_Y_den":3, "weak_doublet":1, "color_dim":3, "tetra_mode":3},
    {"slot":"d",   "family":"down_quark",     "generation":1, "left_Y_num":1,  "left_Y_den":6, "right_Y_num":-1, "right_Y_den":3, "weak_doublet":1, "color_dim":3, "tetra_mode":1},
    {"slot":"s",   "family":"down_quark",     "generation":2, "left_Y_num":1,  "left_Y_den":6, "right_Y_num":-1, "right_Y_den":3, "weak_doublet":1, "color_dim":3, "tetra_mode":2},
    {"slot":"b",   "family":"down_quark",     "generation":3, "left_Y_num":1,  "left_Y_den":6, "right_Y_num":-1, "right_Y_den":3, "weak_doublet":1, "color_dim":3, "tetra_mode":3},
]

FAMILY_INDEX = {"charged_lepton": 1, "down_quark": 2, "up_quark": 3}


def gcd(a:int,b:int)->int:
    while b:
        a,b=b,a%b
    return abs(a)


def rational_abs(num:int, den:int)->float:
    return abs(num) / abs(den)


def collatz_orbit(n:int, max_steps:int=512)->Tuple[int,int,int]:
    """Return (steps_to_1, max_value, odd_steps) for positive integer structural seed."""
    if n <= 0:
        raise ValueError('Collatz seed must be positive')
    x = n
    steps = 0
    odd_steps = 0
    mx = x
    while x != 1 and steps < max_steps:
        if x % 2:
            x = 3*x + 1
            odd_steps += 1
        else:
            x //= 2
        mx = max(mx, x)
        steps += 1
    if x != 1:
        raise RuntimeError('Collatz orbit did not close inside max_steps')
    return steps, mx, odd_steps


def eta_product_log(q:float, terms:int=64)->float:
    """Log of eta-like product prod_n (1-q^n), truncated. Ramanujan modular scale component."""
    s = 0.0
    for n in range(1, terms+1):
        s += math.log1p(-(q**n))
    return s


def ramanujan_generation_scale(g:int)->float:
    """Frozen non-fitted modular generation scale using eta-product phase depth."""
    # q^g plus eta-product log creates a deterministic monotone structural scale.
    eta_log = eta_product_log(Q_RAM, terms=64)
    return math.exp(-g * math.pi / 3.0) * math.exp((g/3.0) * eta_log)


def structural_seed(slot:dict)->int:
    """Integer-only seed from generation, family, color and hypercharge denominators."""
    g = slot['generation']
    fam = FAMILY_INDEX[slot['family']]
    color = slot['color_dim']
    den_mix = slot['left_Y_den'] * slot['right_Y_den']
    num_mix = abs(slot['left_Y_num']) + abs(slot['right_Y_num']) + 1
    # Deterministic structural seed. No mass values or experimental constants.
    return int((6*g + 5*fam + 2*color + den_mix) * num_mix)


def mmt_trace(slot:dict)->dict:
    seed = structural_seed(slot)
    steps, mx, odd = collatz_orbit(seed)
    g = slot['generation']
    yL = rational_abs(slot['left_Y_num'], slot['left_Y_den'])
    yR = rational_abs(slot['right_Y_num'], slot['right_Y_den'])
    chirality_gap = abs(yR - yL)
    hypercharge_sum = yL + yR
    color_pressure = math.log1p(slot['color_dim'])
    tetra_depth = math.sqrt(slot['tetra_mode'] / 3.0)
    collatz_depth = math.log1p(steps + odd) / math.log1p(mx)
    ram_scale = ramanujan_generation_scale(g)
    family_phase = FAMILY_INDEX[slot['family']] / 3.0
    # Frozen log-yukawa-like structural trace. This is dimensionless and uncalibrated.
    # It is NOT a physical mass and NOT a benchmark result.
    log_yukawa_trace = (
        - (g * math.pi) * ram_scale
        - (steps * Q_INFO)
        + math.log1p(hypercharge_sum + chirality_gap)
        + 0.5 * color_pressure
        - tetra_depth
        + family_phase * Q_INFO
        - collatz_depth
    )
    amplitude = math.exp(log_yukawa_trace)
    return {
        **slot,
        "structural_seed": seed,
        "collatz_steps": steps,
        "collatz_max": mx,
        "collatz_odd_steps": odd,
        "q_info_ln2_over_24pi": Q_INFO,
        "q_ram_exp_minus_2pi": Q_RAM,
        "ramanujan_generation_scale": ram_scale,
        "hypercharge_sum_abs": hypercharge_sum,
        "chirality_gap_abs": chirality_gap,
        "color_pressure_log1p": color_pressure,
        "tetra_depth": tetra_depth,
        "collatz_depth": collatz_depth,
        "log_yukawa_trace_frozen": log_yukawa_trace,
        "dimensionless_mmt_amplitude_frozen": amplitude,
        "physical_mass_prediction_claimed": False,
        "benchmark_allowed_in_this_module": False,
        "pdg_reference_input_used": False,
    }


def main()->None:
    traces = [mmt_trace(s) for s in FERMION_SLOTS]
    # A sealed fingerprint binds the operator trace before any future benchmark.
    trace_json = json.dumps(traces, sort_keys=True, separators=(',', ':'))
    import hashlib
    fingerprint = hashlib.sha256(trace_json.encode('utf-8')).hexdigest()
    result = {
        "schema": "METATIME_MMT_FREEZE_V4_3",
        "created_utc": "2026-06-20T00:00:00Z",
        "status": "FROZEN_OPERATOR_CANDIDATE_NOT_BENCHMARKED",
        "operator_name": "M_MT_frozen_candidate_v4_3",
        "debt9_numeric_spectrum_status": "OPEN_PENDING_SINGLE_SEALED_BENCHMARK",
        "mass_prediction_claimed": False,
        "pdg_reference_input_used": False,
        "observed_masses_used": False,
        "fitted_parameters_used": False,
        "single_future_benchmark_required": True,
        "constants": {
            "information_quantum_qI": Q_INFO,
            "ramanujan_q": Q_RAM,
            "pi_source": "python_math_constant",
            "ln2_source": "python_math_log",
        },
        "operator_trace_sha256": fingerprint,
        "traces": traces,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / 'metatime_mmt_freeze_v4_3.json').write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    with (OUT / 'metatime_mmt_freeze_v4_3.csv').open('w', newline='', encoding='utf-8') as f:
        fields = list(traces[0].keys())
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(traces)
    print(json.dumps({
        "status": result['status'],
        "slots": len(traces),
        "operator_trace_sha256": fingerprint,
        "mass_prediction_claimed": False,
    }, indent=2))

if __name__ == '__main__':
    main()
