#!/usr/bin/env python3
"""
METATIME / Standard Model Derivation v3.8
PDG-free gauge-chiral skeleton and hypercharge anomaly derivation.

This script deliberately uses only representation multiplicities, anomaly equations,
Yukawa gauge-invariance equations, and an external normalization convention.
It imports no PDG table, no masses, no CKM/PMNS values, and no observed spectrum.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

CREATED_UTC = "2026-06-20T13:30:00Z"
SCHEMA = "METATIME_SM_PDG_FREE_GAUGE_CHIRAL_SKELETON_V3_8"

@dataclass(frozen=True)
class Field:
    name: str
    color_dim: int
    weak_dim: int
    su3_rep: str
    su2_rep: str
    hypercharge: Fraction
    chirality_convention: str

    @property
    def multiplicity(self) -> int:
        return self.color_dim * self.weak_dim


def derive_hypercharges(normalize_YH: Fraction = Fraction(1, 2)) -> Dict[str, Fraction]:
    """Derive the one-generation SM hypercharges up to Higgs normalization.

    Unknowns use left-handed Weyl convention:
      Q, u_c, d_c, L, e_c, H.

    Constraints:
      SU(2)^2 U(1): 3 Y_Q + Y_L = 0
      Yukawa up:      Y_Q + Y_H + Y_u = 0
      Yukawa down:    Y_Q - Y_H + Y_d = 0
      Yukawa charged: Y_L - Y_H + Y_e = 0
      grav-U(1):      6Y_Q + 3Y_u + 3Y_d + 2Y_L + Y_e = 0

    These imply Y_H = 3Y_Q; choosing Y_H = 1/2 gives the usual normalization.
    """
    YH = normalize_YH
    YQ = YH / 3
    YL = -3 * YQ
    Yu = -YQ - YH
    Yd = -YQ + YH
    Ye = YH - YL
    return {"Q": YQ, "u_c": Yu, "d_c": Yd, "L": YL, "e_c": Ye, "H": YH}


def fields_from_hypercharges(Y: Dict[str, Fraction]) -> List[Field]:
    return [
        Field("Q", 3, 2, "3", "2", Y["Q"], "left-handed Weyl doublet"),
        Field("u_c", 3, 1, "anti-3", "1", Y["u_c"], "left-handed conjugate of right up"),
        Field("d_c", 3, 1, "anti-3", "1", Y["d_c"], "left-handed conjugate of right down"),
        Field("L", 1, 2, "1", "2", Y["L"], "left-handed lepton doublet"),
        Field("e_c", 1, 1, "1", "1", Y["e_c"], "left-handed conjugate of right charged lepton"),
        Field("H", 1, 2, "1", "2", Y["H"], "scalar Higgs doublet / normalization object"),
    ]


def anomaly_checks(Y: Dict[str, Fraction]) -> Dict[str, str]:
    # Fermions only except Yukawa checks include H.
    checks = {
        "SU3_SU3_U1__2YQ_plus_Yu_plus_Yd": 2 * Y["Q"] + Y["u_c"] + Y["d_c"],
        "SU2_SU2_U1__3YQ_plus_YL": 3 * Y["Q"] + Y["L"],
        "grav_grav_U1__sum_multiplicity_Y": 6 * Y["Q"] + 3 * Y["u_c"] + 3 * Y["d_c"] + 2 * Y["L"] + Y["e_c"],
        "U1_cubed__sum_multiplicity_Y3": 6 * Y["Q"]**3 + 3 * Y["u_c"]**3 + 3 * Y["d_c"]**3 + 2 * Y["L"]**3 + Y["e_c"]**3,
        "yukawa_up__YQ_plus_YH_plus_Yu": Y["Q"] + Y["H"] + Y["u_c"],
        "yukawa_down__YQ_minus_YH_plus_Yd": Y["Q"] - Y["H"] + Y["d_c"],
        "yukawa_charged__YL_minus_YH_plus_Ye": Y["L"] - Y["H"] + Y["e_c"],
    }
    return {k: str(v) for k, v in checks.items()}


def electric_charges(Y: Dict[str, Fraction]) -> Dict[str, str]:
    # Q_em = T3 + Y. Doublets have T3 = +/- 1/2. Singlets/conjugates have T3 = 0.
    charges = {
        "u_L_in_Q": Fraction(1, 2) + Y["Q"],
        "d_L_in_Q": Fraction(-1, 2) + Y["Q"],
        "u_c_left_charge": Y["u_c"],
        "d_c_left_charge": Y["d_c"],
        "nu_L_in_L": Fraction(1, 2) + Y["L"],
        "e_L_in_L": Fraction(-1, 2) + Y["L"],
        "e_c_left_charge": Y["e_c"],
        "H_plus_component": Fraction(1, 2) + Y["H"],
        "H_neutral_component": Fraction(-1, 2) + Y["H"],
    }
    return {k: str(v) for k, v in charges.items()}


def main() -> None:
    out_dir = Path(__file__).resolve().parents[1] / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    Y = derive_hypercharges(Fraction(1, 2))
    fields = fields_from_hypercharges(Y)
    checks = anomaly_checks(Y)
    all_zero = all(Fraction(v) == 0 for v in checks.values())
    payload = {
        "schema": SCHEMA,
        "created_utc": CREATED_UTC,
        "status": "PASS" if all_zero else "FAIL",
        "scope": "one-generation gauge-chiral hypercharge skeleton; no mass derivation claimed",
        "input_policy": {
            "PDG_masses": "FORBIDDEN",
            "observed_fermion_masses": "FORBIDDEN",
            "CKM_PMNS": "FORBIDDEN",
            "normalization": "Y_H = 1/2 convention only; hypercharge ratios derived before mass comparison",
        },
        "derived_hypercharges": {k: str(v) for k, v in Y.items()},
        "fermion_and_higgs_fields": [
            {**asdict(f), "hypercharge": str(f.hypercharge), "multiplicity": f.multiplicity}
            for f in fields
        ],
        "anomaly_and_yukawa_checks": checks,
        "all_checks_zero": all_zero,
        "electric_charge_checks": electric_charges(Y),
        "doctor_verdict": "CONTINUE_RESEARCH__PDG_FREE_GAUGE_CHIRAL_SKELETON_PASS" if all_zero else "STOP_CRITICAL",
    }
    (out_dir / "sm_hypercharge_anomaly_derivation_v3_8.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
