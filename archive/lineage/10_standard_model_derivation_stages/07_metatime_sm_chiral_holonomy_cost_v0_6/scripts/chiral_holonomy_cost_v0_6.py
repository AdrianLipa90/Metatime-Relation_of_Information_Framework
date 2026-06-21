#!/usr/bin/env python3
from fractions import Fraction
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

transitions = [
    {
        "class": "charged_lepton",
        "left": "e_L",
        "right": "e_R",
        "selector": "H",
        "Y_L": Fraction(-1,2),
        "Y_R": Fraction(-1,1),
        "Y_selector": Fraction(1,2),
        "T3_L": Fraction(-1,2),
        "Q_L": Fraction(-1,1),
        "Q_R": Fraction(-1,1),
        "color_preserved": True,
        "status": "allowed",
    },
    {
        "class": "down_quark",
        "left": "d_L",
        "right": "d_R",
        "selector": "H",
        "Y_L": Fraction(1,6),
        "Y_R": Fraction(-1,3),
        "Y_selector": Fraction(1,2),
        "T3_L": Fraction(-1,2),
        "Q_L": Fraction(-1,3),
        "Q_R": Fraction(-1,3),
        "color_preserved": True,
        "status": "allowed",
    },
    {
        "class": "up_quark",
        "left": "u_L",
        "right": "u_R",
        "selector": "H_conj",
        "Y_L": Fraction(1,6),
        "Y_R": Fraction(2,3),
        "Y_selector": Fraction(-1,2),
        "T3_L": Fraction(1,2),
        "Q_L": Fraction(2,3),
        "Q_R": Fraction(2,3),
        "color_preserved": True,
        "status": "allowed",
    },
    {
        "class": "neutrino_dirac_optional",
        "left": "nu_L",
        "right": "nu_R",
        "selector": "H_conj",
        "Y_L": Fraction(-1,2),
        "Y_R": Fraction(0,1),
        "Y_selector": Fraction(-1,2),
        "T3_L": Fraction(1,2),
        "Q_L": Fraction(0,1),
        "Q_R": Fraction(0,1),
        "color_preserved": True,
        "status": "optional_extension",
    },
]

def fmt(fr):
    return f"{fr.numerator}/{fr.denominator}" if fr.denominator != 1 else str(fr.numerator)

rows = []
failures = []
for t in transitions:
    residual = -t["Y_L"] + t["Y_selector"] + t["Y_R"]
    q_residual = t["Q_R"] - t["Q_L"]
    cost = Fraction(1,1) + abs(t["T3_L"]) + abs(t["Y_selector"])
    row = dict(t)
    row.update({
        "hypercharge_residual": residual,
        "electric_charge_residual": q_residual,
        "chiral_cost_v0_6": cost,
    })
    rows.append(row)
    if residual != 0:
        failures.append((t["class"], "hypercharge_residual", residual))
    if q_residual != 0:
        failures.append((t["class"], "electric_charge_residual", q_residual))
    if not t["color_preserved"]:
        failures.append((t["class"], "color_preserved", False))
    if t["status"] == "allowed" and cost != 2:
        failures.append((t["class"], "chiral_cost", cost))

csv_path = RESULTS / "chiral_transition_table_v0_6.csv"
fields = [
    "class","left","right","selector","Y_L","Y_selector","Y_R",
    "T3_L","Q_L","Q_R","hypercharge_residual",
    "electric_charge_residual","color_preserved","status","chiral_cost_v0_6"
]
with csv_path.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows:
        w.writerow({k: fmt(r[k]) if isinstance(r[k], Fraction) else r[k] for k in fields})

out = []
out.append("METATIME SM CHIRAL HOLONOMY COST v0.6")
out.append("Observed masses used: NO")
out.append("Primitive Yukawa couplings introduced: NO")
out.append("Transition balance: -Y_L + Y_selector + Y_R = 0")
out.append("")
for r in rows:
    out.append(f"{r['class']}: residual_Y={fmt(r['hypercharge_residual'])}; residual_Q={fmt(r['electric_charge_residual'])}; cost={fmt(r['chiral_cost_v0_6'])}; status={r['status']}")
out.append("")
if failures:
    out.append("FAIL")
    for x in failures:
        out.append(str(x))
else:
    out.append("PASS: all allowed charged transitions are gauge-balanced and have universal chiral cost 2.")
    out.append("NOTE: optional Dirac neutrino row is retained as extension hook, not as a promoted mass mechanism.")

(RESULTS / "chiral_validation_result_v0_6.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
