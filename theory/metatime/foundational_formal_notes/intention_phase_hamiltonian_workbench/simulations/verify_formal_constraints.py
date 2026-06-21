#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Formal diagnostics for the toy intention-phase simulation output."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

EXPECTED_KAPPA = math.log(2.0) / (24.0 * math.pi)


def main(path: str = "../data/simulation_summary.json") -> int:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    issues = []
    if abs(data["kappa_ln2_over_24pi"] - EXPECTED_KAPPA) > 1e-15:
        issues.append("kappa mismatch")
    for row in data["summaries"]:
        if abs(row["final_norm"] - 1.0) > 1e-10:
            issues.append(f"norm drift for seed {row['seed']}: {row['final_norm']}")
        if row["max_unitarity_error"] > 1e-10:
            issues.append(f"unitarity error for seed {row['seed']}: {row['max_unitarity_error']}")
    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS")
    print(f"seeds_checked={len(data['summaries'])}")
    print(f"kappa={data['kappa_ln2_over_24pi']:.18f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:]))
