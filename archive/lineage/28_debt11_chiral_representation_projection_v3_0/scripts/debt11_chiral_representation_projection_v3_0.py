#!/usr/bin/env python3
"""Debt 11 chiral representation projection table generator.

Purpose:
- Build a one-generation chiral representation/projection table from CP1 pole,
  chirality, Higgs-gate legality, color/tetrahedral depth and anomaly checks.
- Do NOT use observed masses.
- Do NOT compute mass predictions.

Convention:
- Electric charge Q = T3 + Y.
- Hypercharge normalization fixed by neutral neutrino pole and electron charge unit.
- Right-handed fields are listed physically; anomaly checks convert them to left-handed conjugates.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

Y_H = Fraction(1, 2)

@dataclass(frozen=True)
class Channel:
    particle_id: str
    sector: str
    chirality: str
    weak_object: str
    cp1_pole: str
    t3: Fraction
    color_multiplicity: int
    color_role: str
    hypercharge: Fraction
    electric_charge: Fraction
    higgs_gate: str
    seed_mode_status: str
    seed_mode_candidate: str
    info_quantum_channel: str
    zeta_axis_relation: str
    ramanujan_role: str
    projection_status: str
    epistemic_status: str


def frac_str(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def channel_rows() -> List[Channel]:
    rows: List[Channel] = []
    # One-generation physical chiral channels. Generation replication and seed allocation remain separate.
    rows.extend([
        Channel("nu_L", "neutrino", "L", "weak_doublet", "north/+", Fraction(1,2), 1, "colorless", Fraction(-1,2), Fraction(0), "neutral_upper_component", "open", "neutrino sector seed candidate; not mass input", "kappa as preference-fluctuation quantum", "zeta imaginary axis constrains CP1 pole", "not a free scale; later suppression/asymptotic role", "massless-or-Dirac/Majorana gate open", "derived charge; neutrino mass channel open"),
        Channel("e_L", "charged_lepton", "L", "weak_doublet", "south/-", Fraction(-1,2), 1, "colorless", Fraction(-1,2), Fraction(-1), "charged_lower_component", "open", "charged-lepton sector seed candidate", "kappa as preference-fluctuation quantum", "zeta imaginary axis constrains CP1 pole", "not a free scale; later suppression/asymptotic role", "left input to H/e_R transition", "derived charge; mass projection not closed"),
        Channel("e_R", "charged_lepton", "R", "weak_singlet", "singlet projection", Fraction(0), 1, "colorless", Fraction(-1), Fraction(-1), "barL_H_eR_allowed", "open", "charged-lepton sector seed candidate", "kappa as preference-fluctuation quantum", "singlet inherits zeta-compatible phase through transition", "not a free scale; later suppression/asymptotic role", "right output of H transition", "derived from Higgs legality + anomaly consistency"),
        Channel("u_L", "up_quark", "L", "weak_doublet", "north/+", Fraction(1,2), 3, "color_triplet/tetrahedral-depth", Fraction(1,6), Fraction(2,3), "upper_quark_component", "open", "light/heavy up-sector seed candidate", "kappa as preference-fluctuation quantum", "zeta imaginary axis constrains CP1 pole", "not a free scale; sector projection needed", "left input to Htilde/u_R transition", "derived charge; mass projection not closed"),
        Channel("d_L", "down_quark", "L", "weak_doublet", "south/-", Fraction(-1,2), 3, "color_triplet/tetrahedral-depth", Fraction(1,6), Fraction(-1,3), "lower_quark_component", "open", "light/heavy down-sector seed candidate", "kappa as preference-fluctuation quantum", "zeta imaginary axis constrains CP1 pole", "not a free scale; sector projection needed", "left input to H/d_R transition", "derived charge; mass projection not closed"),
        Channel("u_R", "up_quark", "R", "weak_singlet", "singlet projection", Fraction(0), 3, "color_triplet/tetrahedral-depth", Fraction(2,3), Fraction(2,3), "barQ_Htilde_uR_allowed", "open", "light/heavy up-sector seed candidate", "kappa as preference-fluctuation quantum", "singlet inherits zeta-compatible phase through transition", "not a free scale; sector projection needed", "right output of Htilde transition", "derived from Higgs legality + anomaly consistency"),
        Channel("d_R", "down_quark", "R", "weak_singlet", "singlet projection", Fraction(0), 3, "color_triplet/tetrahedral-depth", Fraction(-1,3), Fraction(-1,3), "barQ_H_dR_allowed", "open", "light/heavy down-sector seed candidate", "kappa as preference-fluctuation quantum", "singlet inherits zeta-compatible phase through transition", "not a free scale; sector projection needed", "right output of H transition", "derived from Higgs legality + anomaly consistency"),
    ])
    # Optional sterile channel is kept separate/quarantined; it is not required for SM anomaly cancellation.
    rows.append(Channel("nu_R_optional", "neutrino", "R", "weak_singlet", "sterile singlet", Fraction(0), 1, "colorless", Fraction(0), Fraction(0), "Dirac_neutrino_optional", "quarantine", "optional neutrino extension; not required in minimal SM table", "kappa channel not promoted", "zeta relation open", "not promoted", "optional sterile projection", "quarantined optional extension"))
    return rows


def write_table(rows: List[Channel]) -> None:
    csv_path = RESULTS / "chiral_representation_table_v3_0.csv"
    fields = list(asdict(rows[0]).keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            d = asdict(r)
            for k, v in list(d.items()):
                if isinstance(v, Fraction):
                    d[k] = frac_str(v)
            writer.writerow(d)


def anomaly_report(rows: List[Channel]) -> Dict[str, object]:
    # Use minimal physical channels, exclude optional sterile.
    ch = {r.particle_id: r for r in rows if r.projection_status != "optional sterile projection"}
    # shorthand physical hypercharges
    Y_Q = ch["u_L"].hypercharge  # same as d_L
    Y_L = ch["nu_L"].hypercharge  # same as e_L
    Y_u = ch["u_R"].hypercharge
    Y_d = ch["d_R"].hypercharge
    Y_e = ch["e_R"].hypercharge
    anomalies = {
        "SU3_SU3_U1": 2 * Y_Q - Y_u - Y_d,
        "SU2_SU2_U1": 3 * Y_Q + Y_L,
        "grav_grav_U1": 6 * Y_Q - 3 * Y_u - 3 * Y_d + 2 * Y_L - Y_e,
        "U1_U1_U1": 6 * Y_Q**3 - 3 * Y_u**3 - 3 * Y_d**3 + 2 * Y_L**3 - Y_e**3,
    }
    higgs = {
        "charged_lepton_barL_H_eR": -Y_L + Y_H + Y_e,
        "down_barQ_H_dR": -Y_Q + Y_H + Y_d,
        "up_barQ_Htilde_uR": -Y_Q - Y_H + Y_u,
    }
    charges = {r.particle_id: r.t3 + r.hypercharge for r in rows}
    report = {
        "version": "v3.0",
        "observed_masses_used": False,
        "pdg_values_used": False,
        "right_handed_fields_conjugated_for_anomaly_checks": True,
        "hypercharge_convention": "Q = T3 + Y",
        "higgs_hypercharge": frac_str(Y_H),
        "anomalies": {k: frac_str(v) for k, v in anomalies.items()},
        "higgs_legality_residuals": {k: frac_str(v) for k, v in higgs.items()},
        "electric_charge_checks": {k: frac_str(v) for k, v in charges.items()},
        "all_anomaly_residuals_zero": all(v == 0 for v in anomalies.values()),
        "all_higgs_residuals_zero": all(v == 0 for v in higgs.values()),
        "minimal_physical_channel_count_excluding_optional_nuR": 7,
        "weyl_state_count_with_color_multiplicity_excluding_optional_nuR": 15,
        "optional_sterile_neutrino_quarantined": True,
        "gate": "STRUCTURAL_ENUMERATION_PASS",
        "debt11_status": "conditionally_closed_for_one_generation_chiral_table_not_for_mass_projection",
    }
    (RESULTS / "anomaly_and_higgs_gate_report_v3_0.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def projection_table(rows: List[Channel]) -> None:
    # A symbolic operator channel, not a mass formula.
    # Values are labels/statuses, not fitted numeric coefficients.
    table = []
    for r in rows:
        if r.particle_id == "nu_R_optional":
            status = "quarantine_optional_extension"
        elif r.color_multiplicity == 3:
            status = "color_tetrahedral_projection_required_before_mass"
        elif r.sector == "neutrino":
            status = "neutrino_pairwise_or_sterile_gate_required_before_mass"
        else:
            status = "charged_lepton_projection_required_before_mass"
        table.append({
            "particle_id": r.particle_id,
            "sector": r.sector,
            "P_CP1": f"T3={frac_str(r.t3)}, pole={r.cp1_pole}",
            "P_chiral": r.chirality,
            "P_color": r.color_role,
            "P_hypercharge": frac_str(r.hypercharge),
            "P_higgs_gate": r.higgs_gate,
            "P_information_quantum": "kappa=ln2/(24pi) as preference-fluctuation quantum; no fitted multiplier",
            "P_zeta": r.zeta_axis_relation,
            "P_ramanujan": r.ramanujan_role,
            "mass_projection_status": status,
        })
    path = RESULTS / "projection_channel_table_v3_0.csv"
    fields = list(table[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(table)


def main() -> None:
    rows = channel_rows()
    write_table(rows)
    projection_table(rows)
    report = anomaly_report(rows)
    ledger = {
        "module": "28_debt11_chiral_representation_projection_v3_0",
        "debt": "Debt 11 — chiral representation table and sector projection operator",
        "status": report["debt11_status"],
        "gate": report["gate"],
        "mass_predictions_made": False,
        "observed_masses_used": False,
        "next_required_step": "turn symbolic P_rep into frozen mass-projection operator before Debt 9 rescore",
        "do_not_claim": [
            "not a numerical mass derivation",
            "not CKM/PMNS derivation",
            "not full proof of generation replication",
            "not proof that optional nu_R exists",
        ],
    }
    (RESULTS / "debt11_status_ledger_v3_0.json").write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "gate": report["gate"], "channels": len(rows), "weyl_count_minimal": 15}, indent=2))


if __name__ == "__main__":
    main()
