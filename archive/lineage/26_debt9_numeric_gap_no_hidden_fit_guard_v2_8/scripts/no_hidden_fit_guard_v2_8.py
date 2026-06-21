#!/usr/bin/env python3
"""Debt 9 v2.8: no-hidden-fit guard.

This script audits the one-anchor mass scaling stress test and blocks premature
numeric-mass-derivation claims. It is not a mass-prediction solver.
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "24_debt9_one_anchor_mass_scaling_v2_6/results/one_anchor_mass_scaling_summary_v2_6.csv"
OUTDIR = Path(__file__).resolve().parents[1] / "results"


def read_rows():
    with SUMMARY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["median_abs_log_error_excluding_anchor"] = float(r["median_abs_log_error_excluding_anchor"])
        r["max_abs_log_error_excluding_anchor"] = float(r["max_abs_log_error_excluding_anchor"])
        r["non_anchor_count"] = int(r["non_anchor_count"])
        r["uses_observed_masses_as_inputs_other_than_anchor"] = (r["uses_observed_masses_as_inputs_other_than_anchor"] == "True")
    return rows


def main():
    rows = read_rows()
    assert rows, "Missing v2.6 stress-test summary rows"
    assert all(not r["uses_observed_masses_as_inputs_other_than_anchor"] for r in rows), "Hidden non-anchor mass input detected"
    best = min(rows, key=lambda r: r["median_abs_log_error_excluding_anchor"])
    eb = next(r for r in rows if r["variant"] == "EB_ONLY")
    # Guard criterion: current gap is large, therefore no numeric closure is allowed.
    median_factor = math.exp(best["median_abs_log_error_excluding_anchor"])
    max_factor = math.exp(best["max_abs_log_error_excluding_anchor"])
    debt9_numeric_derivation_pass_allowed_now = False
    payload = {
        "gate_type": "METHODOLOGICAL_GUARD_PASS",
        "best_variant": best["variant"],
        "median_abs_log_error_excluding_anchor": best["median_abs_log_error_excluding_anchor"],
        "max_abs_log_error_excluding_anchor": best["max_abs_log_error_excluding_anchor"],
        "median_factor_error_approx": median_factor,
        "max_factor_error_approx": max_factor,
        "ramanujan_median_log_improvement_vs_EB_ONLY": eb["median_abs_log_error_excluding_anchor"] - best["median_abs_log_error_excluding_anchor"],
        "debt9_numeric_derivation_pass_allowed_now": debt9_numeric_derivation_pass_allowed_now,
        "required_next_step": "derive tau_v2/information eigenvalue before any mass-error improvement claim",
    }
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "no_hidden_fit_guard_run_v2_8.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
