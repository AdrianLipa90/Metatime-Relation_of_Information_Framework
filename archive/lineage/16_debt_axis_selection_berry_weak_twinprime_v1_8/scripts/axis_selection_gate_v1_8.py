#!/usr/bin/env python3
"""Validation gate for METATIME SM axis-selection debt v1.8."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / "AXIS_SELECTION_SCHEMA_v1_8.json").read_text())
roles = schema["roles"]
checks = {
    "primitive_axis_is_weak_isospin": roles["primitive_axis"] == "weak_isospin_bloch_quantization_axis",
    "generator_is_killing_flow": roles["primitive_generator"] == "killing_flow_generator",
    "berry_is_transport": roles["berry"] == "phase_transport_connection",
    "twin_prime_is_sector_not_axis": roles["twin_prime_seed"] == "generation_sector_index",
    "zeta_constrained_by_polar_pair": roles["zeta_axis"] == "imaginary_zero_spectral_anchor_constrained_by_polar_pair",
}
status = "PASS" if all(checks.values()) else "FAIL"
out = {
    "module": schema["schema_id"],
    "status": status,
    "checks": checks,
    "claim_boundary": "axis-selection canonical working ansatz; not numerical mass proof"
}
results = ROOT / "results"
results.mkdir(exist_ok=True)
(results / "axis_selection_gate_v1_8.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
if status != "PASS":
    raise SystemExit(1)
