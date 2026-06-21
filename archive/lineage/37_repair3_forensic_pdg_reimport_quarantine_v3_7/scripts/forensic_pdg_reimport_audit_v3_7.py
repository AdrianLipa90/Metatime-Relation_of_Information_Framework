#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metatime v3.7 forensic audit: PDG/reference reimport guard."""
import csv, json, importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "36_repair2_archive_formula_source_extraction_execution/external_mass_execution_sources/METATIME_ARCHIVE_FORMULA_MASS_EXECUTION_v3_9.csv"
SOLVER = ROOT / "00_original_metatime/Metatime-main/NoParamSM/noparamSMsolver.py"
OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)
rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
by = {}
for r in rows:
    by.setdefault(r["mode"], []).append(r)
stats = {}
for mode, rs in by.items():
    eq = [float(r["mass_calc"]) == float(r["reference"]) for r in rs]
    stats[mode] = {
        "n": len(rs),
        "equal_count": sum(eq),
        "all_mass_calc_equal_reference": all(eq),
        "max_abs_relative_error": max(abs(float(r["relative_error"])) for r in rs),
    }
spec = importlib.util.spec_from_file_location("noparamSMsolver_forensic", SOLVER)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
O = mod.SpectralConstants().O_I_REF
engine = mod.MassEngine(mod.TopoMapping(mod.SpectralConstants()))
refs = {**mod.PDG["leptons"], **mod.PDG["quarks"]}
base = {p: engine.fermion_mass(p, O) for p in refs}
mod.PDG["leptons"]["e"] = 123.456
mod.PDG["quarks"]["c"] = 9999.0
mod.PDG["quarks"]["t"] = 42.0
engine2 = mod.MassEngine(mod.TopoMapping(mod.SpectralConstants()))
mutation = {p: engine2.fermion_mass(p, O) for p in ["e", "c", "t"]}
verdict = {
    "archive_canonical_spectrum_reference_replay": stats.get("ARCHIVE_CANONICAL_SPECTRUM", {}).get("all_mass_calc_equal_reference"),
    "noparam_outputs_equal_PDG_at_OI_ref": all(base[p] == refs[p] for p in refs),
    "noparam_mutation_follows_PDG_input": mutation == {"e": 123.456, "c": 9999.0, "t": 42.0},
    "debt9_status": "OPEN_NOT_CLOSED",
    "doctor_verdict": "QUARANTINE_MODULE36_DENY_CANON_DENY_CURRENT",
}
(OUT / "forensic_audit_rerun_stats_v3_7.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
(OUT / "forensic_audit_rerun_verdict_v3_7.json").write_text(json.dumps(verdict, indent=2), encoding="utf-8")
print(json.dumps(verdict, indent=2))
