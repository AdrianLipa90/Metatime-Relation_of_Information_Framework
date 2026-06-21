#!/usr/bin/env python3
from __future__ import annotations
import json, zipfile, sys
from pathlib import Path

EXPECTED_SOURCE = '4b7e39882f06ce105c5e12b7c068165973baca4624815fce505ed445ca06fbe9'

def main():
    root = Path(__file__).resolve().parents[2]
    result_path = root/'60_hadron_ratio_benchmark_v6_0A/results/hadron_ratio_benchmark_v6_0A.json'
    result = json.loads(result_path.read_text(encoding='utf-8'))
    issues=[]
    if result.get('source_formula_fingerprint_sha256') != EXPECTED_SOURCE:
        issues.append('source fingerprint mismatch')
    if result.get('mass_prediction_claimed') is not False:
        issues.append('mass_prediction_claimed must remain false')
    if result.get('absolute_mev_scale_derived') is not False:
        issues.append('absolute_mev_scale_derived must remain false')
    if result.get('debt9_numeric_spectrum') != 'OPEN_NOT_CLOSED':
        issues.append('Debt9 must remain open')
    if result.get('decision', {}).get('debt9_closure') != 'DENIED':
        issues.append('Debt9 closure must be denied')
    rows=result.get('rows', [])
    if len(rows) < 8:
        issues.append('too few benchmark rows')
    for r in rows:
        if r.get('benchmark_used_only_after_freeze') is not True:
            issues.append(f'benchmark freeze flag missing for {r.get("hadron")}')
        if r.get('mev_prediction_claimed') is not False:
            issues.append(f'MeV prediction claimed for {r.get("hadron")}')
    status='PASS' if not issues else 'FAIL'
    out = {'module':'60', 'status':status, 'issues':issues, 'checked_rows':len(rows)}
    (root/'60_hadron_ratio_benchmark_v6_0A/results/VALIDATION_MODULE60_v6_0A.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))
    if issues:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
