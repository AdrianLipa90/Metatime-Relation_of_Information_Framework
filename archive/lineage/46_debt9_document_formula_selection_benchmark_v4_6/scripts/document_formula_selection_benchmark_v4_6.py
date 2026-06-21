#!/usr/bin/env python3
"""
METATIME / Standard Model derivation v4.6
Debt 9 document formula selection + sealed benchmark.

This script uses the v4.5 document-derived Collatz/twin-prime/tau trace as the
operator source and a previously frozen benchmark snapshot only after formula
selection. It separates clean structural formulas from formulas that reproduce
known values only by fitted scales, anchors, correction factors, or polynomial
interpolation.
"""
from __future__ import annotations
import csv, hashlib, json, math, pathlib, statistics
from typing import Any, Dict, List, Tuple

MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
ROOT = MODULE_DIR.parent
OUT = MODULE_DIR / "results"
OUT.mkdir(parents=True, exist_ok=True)
TRACE_PATH = ROOT / "45_debt9_document_collatz_twinprime_tau_v4_5" / "results" / "document_collatz_twinprime_tau_trace_v4_5.json"
BENCH_PATH = ROOT / "44_debt9_mmt_sealed_benchmark_v4_4" / "data" / "benchmark_reference_snapshot_v4_4.json"

INFO_QUANTUM = math.log(2.0) / (24.0 * math.pi)
L3 = 7
DOCUMENT_EXPONENTS = {
    "leptons": 2.97,
    "light_quarks": 1.50,
    "heavy_quarks": 1.635,
}
# Anchors used only to convert dimensionless hierarchy to MeV for diagnostics.
# This is not a no-parameter prediction. It is intentionally recorded as benchmark_anchor_used=True.
ANCHORS = {
    "leptons": "e",
    "light_quarks": "u",
    "heavy_quarks": "c",
}
BENCHMARK_ORDER = ["e", "mu", "tau", "u", "d", "s", "c", "b", "t"]

# Generation-level twin-prime centers from the document layer.  v4.5 family centers are
# family-level carriers; this table is the generation-resolved interpretation requested for v4.6.
GENERATION_CENTERS = {
    1: {"pair": (3, 5), "center": 4},
    2: {"pair": (5, 7), "center": 6},
    3: {"pair": (11, 13), "center": 12},
}
GENERATION_LOWER_PRIMES = {1: 3, 2: 5, 3: 11}


def sha256_text(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def collatz_orbit(n: int, max_steps: int = 10000) -> List[int]:
    if n < 1:
        raise ValueError("n must be positive")
    x = n
    out = [x]
    for _ in range(max_steps):
        if x == 1:
            break
        x = x // 2 if x % 2 == 0 else 3 * x + 1
        out.append(x)
    return out


def stopping_length(n: int) -> int:
    return len(collatz_orbit(n)) - 1


def safe_pow(x: float, alpha: float) -> float:
    if x <= 0:
        return 0.0
    return math.exp(alpha * math.log(x))


def load_rows() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
    bench = json.loads(BENCH_PATH.read_text(encoding="utf-8"))
    rows = [r for r in trace["rows"] if r["slot"] in BENCHMARK_ORDER]
    return rows, bench


def candidate_lambda(row: Dict[str, Any], formula_id: str) -> float:
    generation = int(row["generation"])
    if formula_id == "CENTER_P_PLUS_1_L3_POWER_SELECTED_CLEAN_DIAGNOSTIC":
        center = GENERATION_CENTERS[generation]["center"]
        return (stopping_length(center) / L3) ** 2
    if formula_id == "LOWER_TWIN_PRIME_P_L3_POWER_DIAGNOSTIC":
        p = GENERATION_LOWER_PRIMES[generation]
        return (stopping_length(p) / L3) ** 2
    if formula_id == "DOCUMENT_TAU_EIGENVALUE_POWER_DIAGNOSTIC":
        return float(row["tau_doc"])
    if formula_id == "V45_COMPOSITE_TRACE_POWER_DIAGNOSTIC":
        return max(float(row["composite_document_tau_trace"]), 1e-300)
    raise KeyError(formula_id)


def family_for_slot(slot: str, row: Dict[str, Any]) -> str:
    return str(row["family"])


def benchmark_formula(rows: List[Dict[str, Any]], bench: Dict[str, Any], formula_id: str, selected: bool) -> Dict[str, Any]:
    masses = bench["masses_mev"]
    # compute lambda coordinates before benchmark anchoring
    lambdas = {r["slot"]: candidate_lambda(r, formula_id) for r in rows}
    families = {r["slot"]: family_for_slot(r["slot"], r) for r in rows}
    scales: Dict[str, float] = {}
    for family, anchor in ANCHORS.items():
        if anchor in lambdas and family in DOCUMENT_EXPONENTS:
            scales[family] = masses[anchor]["value"] / safe_pow(lambdas[anchor], DOCUMENT_EXPONENTS[family])
    out_rows: List[Dict[str, Any]] = []
    for r in rows:
        slot = r["slot"]
        family = families[slot]
        if family not in DOCUMENT_EXPONENTS or slot not in masses:
            continue
        alpha = DOCUMENT_EXPONENTS[family]
        pred = scales[family] * safe_pow(lambdas[slot], alpha)
        ref = masses[slot]["value"]
        ratio = pred / ref if ref else None
        abs_rel = abs(ratio - 1.0) if ratio is not None else None
        out_rows.append({
            "formula_id": formula_id,
            "selected_formula": selected,
            "slot": slot,
            "family": family,
            "generation": r["generation"],
            "lambda_coordinate": lambdas[slot],
            "document_exponent": alpha,
            "family_anchor_slot": ANCHORS[family],
            "benchmark_anchor_used_for_units": True,
            "predicted_mev": pred,
            "benchmark_mev": ref,
            "ratio_pred_over_benchmark": ratio,
            "absolute_relative_error": abs_rel,
            "reference_use_scope": "POST_SELECTION_BENCHMARK_AND_UNIT_ANCHOR_DIAGNOSTIC_ONLY",
            "debt9_closure_allowed": False,
        })
    abs_errors = [x["absolute_relative_error"] for x in out_rows if x["absolute_relative_error"] is not None and x["slot"] not in ANCHORS.values()]
    log_pairs = [(math.log(max(x["predicted_mev"], 1e-300)), math.log(max(x["benchmark_mev"], 1e-300))) for x in out_rows]
    # simple Pearson on log masses; Spearman avoided for stdlib clarity.
    if len(log_pairs) >= 2:
        xs, ys = zip(*log_pairs)
        mx, my = statistics.mean(xs), statistics.mean(ys)
        vx = sum((x-mx)**2 for x in xs)
        vy = sum((y-my)**2 for y in ys)
        cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
        pearson = cov / math.sqrt(vx*vy) if vx > 0 and vy > 0 else None
    else:
        pearson = None
    return {
        "formula_id": formula_id,
        "selected_formula": selected,
        "rows": out_rows,
        "metrics_excluding_anchor_slots": {
            "median_absolute_relative_error": statistics.median(abs_errors) if abs_errors else None,
            "max_absolute_relative_error": max(abs_errors) if abs_errors else None,
            "mean_absolute_relative_error": statistics.mean(abs_errors) if abs_errors else None,
        },
        "log_mass_pearson_all_slots": pearson,
    }


def main() -> None:
    rows, bench = load_rows()
    if stopping_length(3) != 7:
        raise RuntimeError("L3 base check failed")

    formula_candidates = [
        {
            "formula_id": "CENTER_P_PLUS_1_L3_POWER_SELECTED_CLEAN_DIAGNOSTIC",
            "status": "SELECTED_BEFORE_BENCHMARK",
            "definition": "lambda_i=(L(center=p+1)/L3)^2; m_i = scale_family * lambda_i^alpha_family",
            "why_selected": "directly matches user correction: Collatz dynamics plus twin-prime center p+1 at base L3=7",
            "provenance_class": "clean_structural_formula_with_family_unit_anchor_for_benchmark_units",
        },
        {
            "formula_id": "LOWER_TWIN_PRIME_P_L3_POWER_DIAGNOSTIC",
            "status": "COMPARISON_ONLY",
            "definition": "lambda_i=(L(lower twin prime p)/L3)^2",
            "why_selected": "MetaTheory text also mentions Collatz orbit length of the seed pair/lower p",
            "provenance_class": "clean_structural_comparison",
        },
        {
            "formula_id": "DOCUMENT_TAU_EIGENVALUE_POWER_DIAGNOSTIC",
            "status": "COMPARISON_ONLY_WITH_TAINT_WARNINGS",
            "definition": "lambda_i=tau_doc/eigenvalue from document empirical spectrum; m_i=scale_family*lambda_i^alpha_family",
            "why_selected": "tests the explicit tau/eigenvalue table recovered in v4.5",
            "provenance_class": "mixed: clean for some rows; heavy rows and tau row carry document taint/inconsistency",
        },
        {
            "formula_id": "V45_COMPOSITE_TRACE_POWER_DIAGNOSTIC",
            "status": "COMPARISON_ONLY",
            "definition": "lambda_i=v4.5 composite_document_tau_trace; m_i=scale_family*lambda_i^alpha_family",
            "why_selected": "tests v4.5 frozen trace coordinate without editing residuals",
            "provenance_class": "clean trace coordinate but not document mass formula",
        },
    ]

    benchmark_results = []
    for c in formula_candidates:
        fid = c["formula_id"]
        benchmark_results.append(benchmark_formula(rows, bench, fid, selected=(fid == "CENTER_P_PLUS_1_L3_POWER_SELECTED_CLEAN_DIAGNOSTIC")))

    selected = next(x for x in benchmark_results if x["selected_formula"])
    selected_metrics = selected["metrics_excluding_anchor_slots"]
    selected_pass = bool(selected_metrics["median_absolute_relative_error"] is not None and selected_metrics["median_absolute_relative_error"] < 0.5)

    taint_ledger = {
        "document_formula_taint": [
            {"name": "charged_lepton_vandermonde_polynomial", "status": "TAINTED_FIT", "reason": "degree-2 interpolation through e, mu, tau masses"},
            {"name": "light_quark_intention_corrections_Fi", "status": "TAINTED_BENCHMARK_RATIO", "reason": "F_i computed from known mass/model ratios"},
            {"name": "heavy_quark_scale_and_exponent", "status": "TAINTED_POWER_LAW_FIT", "reason": "document says heavy quarks follow a fitted power law"},
            {"name": "neutrino_global_scale_and_pairwise_corrections", "status": "TAINTED_ANCHOR_CORRECTION", "reason": "uses observed mass splittings as anchors/corrections"},
        ],
        "document_inconsistencies": [
            {"name": "tau_lepton_tau_doc", "status": "REVIEW_REQUIRED", "reason": "document labels tau_doc=10 around (11,13), but center of (11,13) is 12"},
            {"name": "lambda_ordering", "status": "REVIEW_REQUIRED", "reason": "document text says smaller lambda lighter, but e lambda=4 and mu lambda=1 conflict with observed ordering"},
        ],
    }

    result = {
        "schema": "METATIME_DOCUMENT_FORMULA_SELECTION_BENCHMARK_V4_6",
        "module": "46_debt9_document_formula_selection_benchmark_v4_6",
        "selected_clean_formula_id": "CENTER_P_PLUS_1_L3_POWER_SELECTED_CLEAN_DIAGNOSTIC",
        "formal_status": "PASS_WITH_EXPLICIT_TAINT_LEDGER",
        "substantive_status": "SELECTED_CLEAN_DOCUMENT_FORMULA_BENCHMARK_FAILS_AS_NUMERIC_MASS_CLOSURE",
        "debt9_numeric_spectrum": "OPEN_NOT_CLOSED",
        "canon_allowed": False,
        "current_promotion": "DENY_CURRENT",
        "operator_input_policy": {
            "benchmark_masses_used_inside_selected_formula": False,
            "benchmark_masses_used_for_post_selection_unit_anchor_and_error_only": True,
            "archived_mass_solver_used": False,
            "reference_replay_used": False,
            "post_residual_formula_editing": False,
            "family_unit_anchor_means_no_parameter_free_numeric_closure": True,
        },
        "constants": {
            "L3": L3,
            "information_quantum_ln2_over_24pi": INFO_QUANTUM,
            "document_exponents": DOCUMENT_EXPONENTS,
            "family_unit_anchors": ANCHORS,
        },
        "formula_candidates": formula_candidates,
        "benchmark_results": benchmark_results,
        "taint_ledger": taint_ledger,
        "validation_summary": {
            "selected_formula_passes_technical_execution": True,
            "selected_formula_numerically_closes_debt9": selected_pass,
            "selected_formula_median_abs_rel_error_excluding_anchors": selected_metrics["median_absolute_relative_error"],
            "selected_formula_max_abs_rel_error_excluding_anchors": selected_metrics["max_absolute_relative_error"],
            "interpretation": "The user's document route is structurally real, but the literal center p+1 / L3 power-law formula does not generate the charged-fermion mass hierarchy. Tainted document fits reproduce some sectors by construction and must not be promoted."
        }
    }
    result["freeze_sha256"] = sha256_text({
        "selected_clean_formula_id": result["selected_clean_formula_id"],
        "constants": result["constants"],
        "formula_definition": formula_candidates[0]["definition"],
        "trace_source_sha256": json.loads(TRACE_PATH.read_text(encoding="utf-8"))["operator_trace_sha256"],
    })

    (OUT / "document_formula_selection_benchmark_v4_6.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    # Flat CSV over all formula rows.
    all_rows: List[Dict[str, Any]] = []
    for br in benchmark_results:
        all_rows.extend(br["rows"])
    csv_path = OUT / "document_formula_selection_benchmark_v4_6.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    # concise Markdown table for humans
    lines = ["# v4.6 Benchmark Summary", "", "Formula candidates:"]
    for br in benchmark_results:
        m = br["metrics_excluding_anchor_slots"]
        lines.append(f"- `{br['formula_id']}` selected={br['selected_formula']} median_abs_rel_error_ex_anchor={m['median_absolute_relative_error']} max={m['max_absolute_relative_error']}")
    lines.append("")
    lines.append("Selected formula result: FAIL as numeric Debt 9 closure; PASS as sealed diagnostic.")
    (OUT / "BENCHMARK_SUMMARY_v4_6.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
