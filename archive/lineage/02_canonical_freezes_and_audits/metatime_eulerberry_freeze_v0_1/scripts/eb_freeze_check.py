#!/usr/bin/env python3
"""
Euler--Berry canonical freeze v0.1 numerical sanity check.
No internet, no external packages required.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(parents=True, exist_ok=True)

# Frozen information constant
kappa = math.log(2.0) / (24.0 * math.pi)

# Cosmology sanity check, Planck-like values used in previous hard-math audit
Omega_Lambda = 0.685
D_lambda_disk = 1.5 * Omega_Lambda

# Explicit SI check: Lambda = 3 Omega_Lambda H0^2/c^2; RH = c/H0; D = Lambda RH^2/2
c = 299_792_458.0
H0_km_s_Mpc = 67.4
Mpc_m = 3.0856775814913673e22
H0 = H0_km_s_Mpc * 1000.0 / Mpc_m
R_H = c / H0
Lambda = 3.0 * Omega_Lambda * H0 * H0 / (c*c)
D_lambda_explicit = Lambda * R_H * R_H / 2.0

# Neutrino epsilon: epsilon = 1.267/pi * dm2 * L/E for dm2 eV^2, L km, E GeV.
# Examples near common oscillation-baseline regimes.
nu_cases = [
    {"name": "DUNE_like_atmospheric", "dm2": 2.513e-3, "L_km": 1300.0, "E_GeV": 2.5},
    {"name": "T2K_like_atmospheric", "dm2": 2.513e-3, "L_km": 295.0, "E_GeV": 0.6},
    {"name": "NOvA_like_atmospheric", "dm2": 2.513e-3, "L_km": 810.0, "E_GeV": 2.0},
    {"name": "JUNO_like_solar", "dm2": 7.49e-5, "L_km": 53.0, "E_GeV": 0.003},
]

for row in nu_cases:
    eps = (1.267 / math.pi) * row["dm2"] * row["L_km"] / row["E_GeV"]
    row["epsilon_nu"] = eps
    rhs = D_lambda_disk + eps
    row["D_lambda_plus_epsilon"] = rhs
    row["nearest_integer"] = round(rhs)
    row["residual_to_nearest_integer"] = rhs - round(rhs)

# First maximum check: probability phase = pi/2 => epsilon = 1/2
first_max_epsilon = 0.5

result = {
    "schema": "EB_FREEZE_CHECK_V0_1",
    "kappa_ln2_over_24pi": kappa,
    "Omega_Lambda_used": Omega_Lambda,
    "D_lambda_disk_formula": "D_Lambda=(3/2)*Omega_Lambda",
    "D_lambda_disk": D_lambda_disk,
    "SI_cross_check": {
        "H0_km_s_Mpc": H0_km_s_Mpc,
        "H0_s_inv": H0,
        "R_H_m": R_H,
        "Lambda_m_inv_2": Lambda,
        "D_lambda_explicit": D_lambda_explicit,
        "absolute_difference_disk_vs_explicit": abs(D_lambda_disk - D_lambda_explicit),
    },
    "epsilon_nu_formula_experimental_units": "epsilon=(1.267/pi)*Delta_m2[eV^2]*L[km]/E[GeV]",
    "first_oscillation_maximum_epsilon": first_max_epsilon,
    "neutrino_cases": nu_cases,
}

(OUT / "eb_freeze_numbers.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
