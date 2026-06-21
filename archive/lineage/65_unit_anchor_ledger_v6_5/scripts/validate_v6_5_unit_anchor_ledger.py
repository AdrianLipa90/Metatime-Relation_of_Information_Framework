#!/usr/bin/env python3
from __future__ import annotations
import json
import pathlib
import sys

STATUS_ENUM = {
    'ALLOWED_DIMENSIONAL_NORMALIZER',
    'DERIVED_OPERATOR',
    'SCORING_ONLY_AFTER_FREEZE',
    'FORBIDDEN_INPUT_FOR_DERIVATION',
    'QUARANTINED',
    'BLOCKED_PENDING_SOURCE_INDEX',
}
ROLE_ENUM = {
    'unit_anchor', 'mass_anchor', 'dimensional_normalizer', 'operator_constant',
    'benchmark_table', 'ratio_denominator', 'calibration_scale', 'target_ledger'
}
DENY_INPUT_STATUSES = {'FORBIDDEN_INPUT_FOR_DERIVATION', 'QUARANTINED', 'SCORING_ONLY_AFTER_FREEZE'}

def main() -> int:
    here = pathlib.Path(__file__).resolve().parents[1]
    ledger_path = here / 'results' / 'UNIT_ANCHOR_LEDGER_v6_5.json'
    ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    failures = []
    ids = set()
    anchors = ledger.get('anchors', [])
    if not anchors:
        failures.append('no anchors')
    for a in anchors:
        aid = a.get('id')
        if aid in ids:
            failures.append(f'duplicate id {aid}')
        ids.add(aid)
        if a.get('status') not in STATUS_ENUM:
            failures.append(f'{aid} invalid status {a.get("status")}')
        if a.get('role') not in ROLE_ENUM:
            failures.append(f'{aid} invalid role {a.get("role")}')
        if a.get('status') in DENY_INPUT_STATUSES and a.get('allowed_as_input_before_freeze') is not False:
            failures.append(f'{aid} status {a.get("status")} must deny pre-freeze input')
        for field in ['reason','closure_rule','debt_links','affected_modules']:
            if not a.get(field):
                failures.append(f'{aid} missing {field}')
    if ledger.get('debt_delta', {}).get('debt_id') != 'DEBT-006':
        failures.append('debt delta does not close DEBT-006')
    if ledger.get('final_verdict', {}).get('current_promotion') != 'DENY_CURRENT':
        failures.append('current promotion must be DENY_CURRENT')
    report = {
        'module': '65_unit_anchor_ledger_v6_5',
        'status': 'PASS' if not failures else 'FAIL',
        'anchor_count': len(anchors),
        'failures': failures,
        'denied_input_count': sum(1 for a in anchors if a.get('allowed_as_input_before_freeze') is False),
        'allowed_dimensional_normalizer_count': sum(1 for a in anchors if a.get('status') == 'ALLOWED_DIMENSIONAL_NORMALIZER'),
        'quarantined_count': sum(1 for a in anchors if a.get('status') == 'QUARANTINED'),
    }
    out = here / 'results' / 'VALIDATION_MODULE65_v6_5.json'
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not failures else 1

if __name__ == '__main__':
    raise SystemExit(main())
