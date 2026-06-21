#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math, pathlib, hashlib, statistics
from typing import Any, Dict, List

MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
ROOT = MODULE_DIR.parent
OUT = MODULE_DIR / "results"
OUT.mkdir(parents=True, exist_ok=True)

TRACE_PATH = ROOT / "45_debt9_document_collatz_twinprime_tau_v4_5" / "results" / "document_collatz_twinprime_tau_trace_v4_5.json"
V46_PATH = ROOT / "46_debt9_document_formula_selection_benchmark_v4_6" / "results" / "document_formula_selection_benchmark_v4_6.json"
ORIENTATION_PATH = ROOT / "32_debt9_projection_orientation_sector_basis_v3_4" / "results" / "sector_basis_orientation_channels_v3_4.csv"
WHITE_THREAD_PATH = ROOT / "33_debt10_white_thread_open_holonomy_preckm_v3_5" / "results" / "white_thread_open_holonomy_pairs_v3_5.csv"
BENCHMARK_PATH = ROOT / "44_debt9_mmt_sealed_benchmark_v4_4" / "data" / "benchmark_reference_snapshot_v4_4.json"

KAPPA = math.log(2.0) / (24.0 * math.pi)
DOCUMENT_EXPONENTS = {"leptons": 2.97, "light_quarks": 1.5, "heavy_quarks": 1.635}
UNIT_ANCHORS = {"leptons": "e", "light_quarks": "u", "heavy_quarks": "c"}
BENCHMARK_ORDER = ["e", "mu", "tau", "u", "d", "s", "c", "b", "t"]
SAME_GENERATION_UP_FOR_DOWN = {"d": "u", "s": "c", "b": "t"}


def read_csv(path: pathlib.Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sha256_json(obj: Any) -> str:
    data = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def load_inputs() -> Dict[str, Any]:
    trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
    v46 = json.loads(V46_PATH.read_text(encoding="utf-8"))
    bench = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
    orientation_rows = {r["particle"]: r for r in read_csv(ORIENTATION_PATH)}
    white_rows = read_csv(WHITE_THREAD_PATH)
    selected_v46 = next(x for x in v46["benchmark_results"] if x["selected_formula"])
    base_rows = {r["slot"]: r for r in selected_v46["rows"] if r["slot"] in BENCHMARK_ORDER}
    trace_rows = {r["slot"]: r for r in trace["rows"] if r["slot"] in BENCHMARK_ORDER}
    return {
        "trace": trace,
        "v46": v46,
        "benchmark": bench,
        "orientation_rows": orientation_rows,
        "white_rows": white_rows,
        "base_rows": base_rows,
        "trace_rows": trace_rows,
    }


def h_orientation_gate(slot: str, orientation_rows: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    row = orientation_rows.get(slot)
    if not row:
        return {"h_orientation_gate": 1.0, "h_orientation_role": "none", "abs_v7_over_kappa": 0.0}
    path = row["chirality_path"]
    v7 = abs(float(row["v7"]))
    release = 1.0 + v7 / KAPPA
    if "H_minus" in path:
        return {
            "h_orientation_gate": 1.0 / release,
            "h_orientation_role": "H_minus_suppression_existing_v3_4_orientation",
            "abs_v7_over_kappa": v7 / KAPPA,
        }
    if "H_plus" in path:
        return {
            "h_orientation_gate": 1.0,
            "h_orientation_role": "H_plus_no_extra_release_in_v4_7_selected_formula",
            "abs_v7_over_kappa": v7 / KAPPA,
        }
    return {"h_orientation_gate": 1.0, "h_orientation_role": "H_zero_or_neutral", "abs_v7_over_kappa": v7 / KAPPA}


def white_thread_gate(slot: str, white_rows: List[Dict[str, str]]) -> Dict[str, Any]:
    if slot not in SAME_GENERATION_UP_FOR_DOWN:
        return {"white_thread_gate": 1.0, "white_thread_role": "not_down_quark_channel", "paired_up_channel": None}
    up = SAME_GENERATION_UP_FOR_DOWN[slot]
    for r in white_rows:
        if r["up_particle"] == up and r["down_particle"] == slot:
            return {
                "white_thread_gate": abs(float(r["oriented_open_holonomy_overlap"])),
                "white_thread_role": "same_generation_up_down_open_holonomy_gate_existing_v3_5",
                "paired_up_channel": up,
                "phase_gap_rad": float(r["phase_gap_rad"]),
                "white_thread_open_coherence": float(r["white_thread_open_coherence"]),
                "feature_hash": r["feature_hash"],
            }
    raise RuntimeError(f"missing white-thread pair for {slot}")


def selected_sector_split_coordinate(slot: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    base = inputs["base_rows"][slot]
    h = h_orientation_gate(slot, inputs["orientation_rows"])
    w = white_thread_gate(slot, inputs["white_rows"])
    base_lambda = float(base["lambda_coordinate"])
    sector_gate = h["h_orientation_gate"] * w["white_thread_gate"]
    # This selected v4.7 operator is deliberately simple and frozen before benchmark:
    # v4.6 Collatz/twin-prime p+1 carrier times existing v3.4 H/Htilde orientation
    # and existing v3.5 White-Thread same-generation down-quark holonomy.
    split_lambda = base_lambda * sector_gate
    return {
        "slot": slot,
        "family": base["family"],
        "generation": int(base["generation"]),
        "base_v46_lambda": base_lambda,
        "h_orientation_gate": h["h_orientation_gate"],
        "h_orientation_role": h["h_orientation_role"],
        "abs_v7_over_kappa": h["abs_v7_over_kappa"],
        "white_thread_gate": w["white_thread_gate"],
        "white_thread_role": w["white_thread_role"],
        "paired_up_channel": w.get("paired_up_channel"),
        "sector_split_gate": sector_gate,
        "sector_split_lambda": split_lambda,
        "selected_operator_formula": "lambda_47=lambda_v46_center_p_plus_1_L3 * H_orientation_gate_v3_4 * WhiteThread_down_gate_v3_5",
        "mass_input_used_inside_operator": False,
        "benchmark_input_used_inside_operator": False,
        "post_residual_tuning_used": False,
    }


def benchmark_rows(operator_rows: List[Dict[str, Any]], bench: Dict[str, Any]) -> Dict[str, Any]:
    masses = bench["masses_mev"]
    by_slot = {r["slot"]: r for r in operator_rows}
    scales: Dict[str, float] = {}
    for family, anchor in UNIT_ANCHORS.items():
        lam = by_slot[anchor]["sector_split_lambda"]
        scales[family] = masses[anchor]["value"] / (lam ** DOCUMENT_EXPONENTS[family])
    rows: List[Dict[str, Any]] = []
    for slot in BENCHMARK_ORDER:
        rec = by_slot[slot]
        family = rec["family"]
        if family not in DOCUMENT_EXPONENTS:
            continue
        pred = scales[family] * (rec["sector_split_lambda"] ** DOCUMENT_EXPONENTS[family])
        ref = masses[slot]["value"]
        ratio = pred / ref
        rows.append({
            **rec,
            "document_exponent": DOCUMENT_EXPONENTS[family],
            "family_unit_anchor_slot": UNIT_ANCHORS[family],
            "unit_anchor_used_for_benchmark_units": True,
            "predicted_mev_diagnostic": pred,
            "benchmark_mev": ref,
            "ratio_pred_over_benchmark": ratio,
            "absolute_relative_error": abs(ratio - 1.0),
            "reference_use_scope": "POST_FREEZE_BENCHMARK_AND_UNIT_ANCHOR_DIAGNOSTIC_ONLY",
            "debt9_numeric_closure_allowed": False,
        })
    non_anchor_errors = [r["absolute_relative_error"] for r in rows if r["slot"] not in UNIT_ANCHORS.values()]
    log_pairs = [(math.log(max(r["predicted_mev_diagnostic"], 1e-300)), math.log(max(r["benchmark_mev"], 1e-300))) for r in rows]
    xs, ys = zip(*log_pairs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    pearson = cov / math.sqrt(vx * vy) if vx > 0 and vy > 0 else None
    return {
        "rows": rows,
        "metrics_excluding_anchor_slots": {
            "median_absolute_relative_error": statistics.median(non_anchor_errors),
            "mean_absolute_relative_error": statistics.mean(non_anchor_errors),
            "max_absolute_relative_error": max(non_anchor_errors),
        },
        "log_mass_pearson_all_slots": pearson,
    }


def compare_to_v46(v46: Dict[str, Any], v47_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    selected = next(x for x in v46["benchmark_results"] if x["selected_formula"])
    old = {r["slot"]: r for r in selected["rows"]}
    new = {r["slot"]: r for r in v47_rows}
    delta_rows = []
    for slot in BENCHMARK_ORDER:
        if slot not in old or slot not in new:
            continue
        delta_rows.append({
            "slot": slot,
            "v46_abs_rel_error": old[slot]["absolute_relative_error"],
            "v47_abs_rel_error": new[slot]["absolute_relative_error"],
            "error_improvement_positive_is_better": old[slot]["absolute_relative_error"] - new[slot]["absolute_relative_error"],
            "v46_predicted_mev": old[slot]["predicted_mev"],
            "v47_predicted_mev": new[slot]["predicted_mev_diagnostic"],
        })
    improved = [r for r in delta_rows if r["error_improvement_positive_is_better"] > 0]
    worsened = [r for r in delta_rows if r["error_improvement_positive_is_better"] < 0]
    return {"rows": delta_rows, "improved_slots": [r["slot"] for r in improved], "worsened_slots": [r["slot"] for r in worsened]}


def write_csv(path: pathlib.Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerows(rows)


def main() -> None:
    inputs = load_inputs()
    op_rows = [selected_sector_split_coordinate(slot, inputs) for slot in BENCHMARK_ORDER]
    operator_fingerprint = sha256_json({"formula": op_rows, "kappa": KAPPA, "unit_anchors": UNIT_ANCHORS, "document_exponents": DOCUMENT_EXPONENTS})
    bench = benchmark_rows(op_rows, inputs["benchmark"])
    comparison = compare_to_v46(inputs["v46"], bench["rows"])

    selected_metrics = bench["metrics_excluding_anchor_slots"]
    substantive = "PARTIAL_SECTOR_SPLIT_PROGRESS_FAIL_AS_NUMERIC_CLOSURE"
    result = {
        "schema": "METATIME_SM_SECTOR_SPLIT_HOLONOMY_OPERATOR_V4_7",
        "module": "47_debt9_sector_split_holonomy_operator_v4_7",
        "technical_status": "PASS",
        "formal_status": "PASS_WITH_EXPLICIT_TAINT_LEDGER",
        "substantive_status": substantive,
        "debt9_numeric_spectrum": "OPEN_NOT_CLOSED",
        "canon_allowed": False,
        "current_promotion": "DENY_CURRENT",
        "operator_fingerprint_sha256": operator_fingerprint,
        "operator_definition": {
            "carrier": "v4.6 selected clean p+1/L3 Collatz/twin-prime lambda",
            "sector_split": "existing v3.4 H/Htilde orientation gate times existing v3.5 White-Thread down-quark same-generation open holonomy gate",
            "h_orientation_gate": "H_minus -> 1/(1+abs(v7)/kappa); H_plus -> 1; neutral -> 1",
            "white_thread_gate": "down quarks only: abs(oriented_open_holonomy_overlap(up_same_generation, down))",
            "free_parameters_added_after_residuals": 0,
            "new_structures_added": False,
        },
        "operator_policy": {
            "mass_input_used_inside_operator": False,
            "benchmark_input_used_inside_operator": False,
            "post_residual_tuning_used": False,
            "archived_mass_solver_used": False,
            "reference_replay_used": False,
            "unit_anchors_used_only_after_freeze_for_benchmark_units": True,
            "family_unit_anchors_make_this_non_closure": True,
        },
        "operator_rows": op_rows,
        "benchmark": bench,
        "comparison_to_v4_6_selected_formula": comparison,
        "taint_ledger": {
            "document_exponents": "retained from document/v4.6 trace as diagnostic; not a proof of no-parameter mass closure",
            "unit_anchors": "used post-freeze for units; therefore numerical closure is denied",
            "heavy_quark_document_layer": "still historically tainted by power-law anchor; v4.7 tests structural split only",
            "lepton_mode_problem": "mu remains badly mis-scaled; charged lepton generation operator not solved",
        },
        "main_findings": [
            "Existing H/Htilde + White-Thread gates strongly reduce the v4.6 b and d overprediction.",
            "The same operator does not solve the mu channel and over-suppresses s; Debt 9 remains open.",
            "The b/t split moves in the expected direction without adding a new ontology or post-residual parameter.",
        ],
    }

    (OUT / "sector_split_holonomy_operator_v4_7.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    write_csv(OUT / "sector_split_holonomy_operator_v4_7.csv", bench["rows"])
    write_csv(OUT / "comparison_to_v4_6_selected_formula_v4_7.csv", comparison["rows"])
    summary = [
        "# v4.7 sector-split holonomy benchmark summary",
        "",
        f"Operator fingerprint: `{operator_fingerprint}`",
        "",
        "Status: PASS as structural diagnostic; FAIL as numeric Debt 9 closure.",
        "",
        "Metrics excluding unit-anchor slots:",
        f"- median absolute relative error: {selected_metrics['median_absolute_relative_error']}",
        f"- mean absolute relative error: {selected_metrics['mean_absolute_relative_error']}",
        f"- max absolute relative error: {selected_metrics['max_absolute_relative_error']}",
        "",
        "Improved slots versus v4.6 selected formula: " + ", ".join(comparison["improved_slots"]),
        "Worsened slots versus v4.6 selected formula: " + ", ".join(comparison["worsened_slots"]),
        "",
        "The operator uses existing v3.4 H/Htilde orientation and v3.5 White-Thread open holonomy; no new structure is introduced.",
    ]
    (OUT / "BENCHMARK_SUMMARY_v4_7.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "operator_fingerprint_sha256": operator_fingerprint, "metrics": selected_metrics}, indent=2))


if __name__ == "__main__":
    main()
