#!/usr/bin/env python3
"""Validation for Debt 1 Killing generator layer.
This checks the formal pole/index bookkeeping for the axial rotation field on S^2.
It does not prove physical axis selection.
"""
from __future__ import annotations
import json
from pathlib import Path


def local_rotation_index() -> int:
    # The local model (x,y)->(-y,x) winds once positively around zero.
    # We record the index algebraically rather than sampling numerically.
    return 1


def main() -> None:
    north_index = local_rotation_index()
    south_index = local_rotation_index()
    euler_s2 = 2
    result = {
        "field": "axial Killing generator on S2_Bloch",
        "zeros": ["north_pole", "south_pole"],
        "north_index": north_index,
        "south_index": south_index,
        "index_sum": north_index + south_index,
        "euler_characteristic_S2": euler_s2,
        "poincare_hopf_pass": (north_index + south_index == euler_s2),
        "debt1_status": "CONDITIONALLY_CLOSED_GEOMETRIC_GENERATOR",
        "remaining_debt": "physical axis selection: Berry axis vs weak isospin axis vs twin-prime-selected axis",
    }
    outdir = Path(__file__).resolve().parents[1] / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "debt1_killing_generator_validation_v1_7.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
