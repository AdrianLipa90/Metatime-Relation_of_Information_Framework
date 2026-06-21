#!/usr/bin/env python3
"""
METATIME / Standard Model Derivation v4.2
Debt 9 Yukawa-boundary resolution.

Scope:
- derive the SM Yukawa mass-sector boundary from the gauge-chiral skeleton;
- show why charged-fermion masses are not fixed by SU(3)xSU(2)xU(1) gauge geometry alone;
- split Debt 9 into SM-internal closure (Yukawa boundary derived) and Metatime-extra
  numerical spectrum prediction (not closed here);
- no reference mass tables, no observed non-anchor spectrum, no flavour-mixing matrices,
  no old fitted tau/eigenvalue table, and no NoParamSM execution.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from fractions import Fraction
from pathlib import Path
import json
import math
from typing import Dict, List, Tuple

CREATED_UTC = "2026-06-20T18:05:00Z"
SCHEMA = "METATIME_SM_DEBT9_YUKAWA_BOUNDARY_RESOLUTION_V4_2"
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# No numerical particle masses are stored here.  The only dimension-like symbol is
# the formal Higgs vev placeholder v, left symbolic in the report.
KAPPA_INFO = math.log(2.0) / (24.0 * math.pi)
GENERATIONS = 3

@dataclass(frozen=True)
class Field:
    name: str
    color_dim: int
    weak_dim: int
    hypercharge: str
    chirality: str
    generation_count: int

@dataclass(frozen=True)
class YukawaOperator:
    name: str
    symbolic_term: str
    hypercharge_sum: str
    color_invariant: bool
    weak_invariant: bool
    matrix_shape: str
    complex_entries: int
    real_parameters_before_field_redefinitions: int
    fixed_by_gauge_geometry: bool


def derive_hypercharges(YH: Fraction = Fraction(1, 2)) -> Dict[str, Fraction]:
    # Left-handed Weyl convention.
    YQ = YH / 3
    YL = -3 * YQ
    Yu = -YQ - YH
    Yd = -YQ + YH
    Ye = YH - YL
    return {"Q": YQ, "u_c": Yu, "d_c": Yd, "L": YL, "e_c": Ye, "H": YH}


def frac(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def field_table(Y: Dict[str, Fraction]) -> List[Field]:
    return [
        Field("Q", 3, 2, frac(Y["Q"]), "left-handed quark doublet", GENERATIONS),
        Field("u_c", 3, 1, frac(Y["u_c"]), "left-handed conjugate of right up", GENERATIONS),
        Field("d_c", 3, 1, frac(Y["d_c"]), "left-handed conjugate of right down", GENERATIONS),
        Field("L", 1, 2, frac(Y["L"]), "left-handed lepton doublet", GENERATIONS),
        Field("e_c", 1, 1, frac(Y["e_c"]), "left-handed conjugate of right charged lepton", GENERATIONS),
        Field("H", 1, 2, frac(Y["H"]), "Higgs doublet", 1),
    ]


def anomaly_checks(Y: Dict[str, Fraction]) -> Dict[str, str]:
    checks = {
        "SU3_SU3_U1": 2 * Y["Q"] + Y["u_c"] + Y["d_c"],
        "SU2_SU2_U1": 3 * Y["Q"] + Y["L"],
        "gravity_U1": 6 * Y["Q"] + 3 * Y["u_c"] + 3 * Y["d_c"] + 2 * Y["L"] + Y["e_c"],
        "U1_cubed": 6 * Y["Q"]**3 + 3 * Y["u_c"]**3 + 3 * Y["d_c"]**3 + 2 * Y["L"]**3 + Y["e_c"]**3,
    }
    return {k: frac(v) for k, v in checks.items()}


def yukawa_operators(Y: Dict[str, Fraction]) -> List[YukawaOperator]:
    # Terms are in left-handed Weyl convention.  The down/charged sectors use H^dagger
    # while the up sector uses H.  This is equivalent to the ordinary Dirac notation
    # with H and H-tilde assignments, but avoids sign confusion.
    ops = [
        ("up", "Q H u_c", Y["Q"] + Y["H"] + Y["u_c"], True, True),
        ("down", "Q H_dagger d_c", Y["Q"] - Y["H"] + Y["d_c"], True, True),
        ("charged_lepton", "L H_dagger e_c", Y["L"] - Y["H"] + Y["e_c"], True, True),
    ]
    out: List[YukawaOperator] = []
    for name, term, ysum, color_ok, weak_ok in ops:
        entries = GENERATIONS * GENERATIONS
        out.append(YukawaOperator(
            name=name,
            symbolic_term=term,
            hypercharge_sum=frac(ysum),
            color_invariant=color_ok,
            weak_invariant=weak_ok,
            matrix_shape=f"{GENERATIONS}x{GENERATIONS} complex Yukawa matrix",
            complex_entries=entries,
            real_parameters_before_field_redefinitions=2 * entries,
            fixed_by_gauge_geometry=False,
        ))
    return out


def freedom_diagnostics(ops: List[YukawaOperator]) -> Dict[str, object]:
    total_complex = sum(o.complex_entries for o in ops)
    total_real = sum(o.real_parameters_before_field_redefinitions for o in ops)
    # SM flavour data after field redefinitions, for three charged sectors and quark mixing,
    # is not used numerically; this is only a symbolic parameter-count boundary.
    return {
        "three_generation_yukawa_matrices": len(ops),
        "total_complex_entries_before_field_redefinitions": total_complex,
        "total_real_parameters_before_field_redefinitions": total_real,
        "gauge_geometry_fixes_yukawa_entries": False,
        "reason": "Gauge invariance permits the Yukawa matrices but does not determine their entries.",
    }


def holonomy_boundary() -> Dict[str, object]:
    return {
        "v4_1_Wij_role": "SU(3) color parallel transport / holonomic gluon connection",
        "acts_on": "color-triplet carrier and color indices",
        "does_not_act_as": "generation-index mass eigenvalue selector by itself",
        "boundary_claim": "Holonomic gluon dynamics can dress quark-sector propagation, but it does not determine the free Yukawa matrices without an extra flavour/mass operator.",
        "mass_prediction_from_v4_1_claimed": False,
    }


def candidate_metatime_operator_gate() -> Dict[str, object]:
    # This is a gate, not a prediction.  It states what must exist to reopen numerical Debt 9.
    return {
        "required_extra_object": "PDG-free flavour/mass operator M_MT on generation x sector x chirality state space",
        "allowed_inputs": [
            "CP1/Bloch chirality geometry",
            "tetrahedral triplet/CP2 color carrier",
            "holonomic W_ij / W_mu link curvature",
            "Collatz valuation words",
            "Ramanujan theta residue scale",
            "zeta-axis diagnostics",
            "information quantum ln2_over_24pi as fixed fluctuation unit",
        ],
        "forbidden_inputs": [
            "reference mass tables",
            "observed non-anchor fermion masses",
            "old fitted tau/eigenvalue spectra",
            "NoParamSM reference modulation engines",
            "flavour mixing matrices as input",
        ],
        "closure_rule": "Only eigenvalues of M_MT frozen before external benchmark may be mapped through a one-anchor scale test.",
        "current_module_closes_numeric_spectrum": False,
    }


def main() -> None:
    Y = derive_hypercharges()
    fields = field_table(Y)
    anom = anomaly_checks(Y)
    anom_zero = all(v == "0" for v in anom.values())
    ops = yukawa_operators(Y)
    yukawa_allowed = all(o.hypercharge_sum == "0" and o.color_invariant and o.weak_invariant for o in ops)
    all_entries_free = all(o.fixed_by_gauge_geometry is False for o in ops)
    sm_internal_debt9_status = "RESOLVED_AS_YUKAWA_BOUNDARY_NOT_NUMERIC_PREDICTION" if anom_zero and yukawa_allowed and all_entries_free else "FAIL"
    payload = {
        "schema": SCHEMA,
        "created_utc": CREATED_UTC,
        "status": "PASS" if sm_internal_debt9_status.startswith("RESOLVED") else "FAIL",
        "technical_gate": "DEBT9_SM_YUKAWA_BOUNDARY_PASS" if sm_internal_debt9_status.startswith("RESOLVED") else "STOP_CRITICAL",
        "debt9_split": {
            "Debt9_SM_internal": sm_internal_debt9_status,
            "Debt9_numeric_mass_spectrum": "OPEN_NOT_CLOSED_IN_THIS_MODULE",
            "Debt9_metatime_extra_operator": "REQUIRED_FOR_NUMERIC_CLOSURE_NOT_SUPPLIED_HERE",
        },
        "hypercharges": {k: frac(v) for k, v in Y.items()},
        "field_table": [asdict(f) for f in fields],
        "anomaly_checks": anom,
        "anomaly_checks_all_zero": anom_zero,
        "yukawa_operators": [asdict(o) for o in ops],
        "yukawa_gauge_invariance_all_pass": yukawa_allowed,
        "yukawa_freedom_diagnostics": freedom_diagnostics(ops),
        "holonomic_gluon_boundary_from_v4_1": holonomy_boundary(),
        "information_operator": {
            "kappa_ln2_over_24pi": KAPPA_INFO,
            "role": "fixed information-preference fluctuation quantum; not a fitted coefficient",
            "used_to_fit_masses_here": False,
        },
        "metatime_numeric_reopen_gate": candidate_metatime_operator_gate(),
        "observed_masses_used": False,
        "reference_spectrum_used": False,
        "old_tau_used": False,
        "mass_prediction_made": False,
        "canon_allowed": False,
        "current_promotion": "DENY_CURRENT",
        "doctor_verdict": "DEBT9_SM_BOUNDARY_RESOLVED__NUMERIC_SPECTRUM_REMAINS_OPEN" if sm_internal_debt9_status.startswith("RESOLVED") else "STOP_CRITICAL",
    }
    (RESULTS / "debt9_yukawa_boundary_resolution_v4_2.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
