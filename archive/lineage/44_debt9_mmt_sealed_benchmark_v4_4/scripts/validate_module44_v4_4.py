#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, subprocess, sys, zipfile, hashlib, re
MODULE = pathlib.Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
RESULT = MODULE/'results'/'sealed_mmt_benchmark_v4_4.json'
V43 = ROOT/'43_debt9_metatime_mass_operator_freeze_v4_3'/'results'/'metatime_mmt_freeze_v4_3.json'
EXPECTED = 'cf6791ae2010a7e383222fe8edc3d3b41d4a4ebe8b671bd96425b52b33128e37'

def main():
    if not RESULT.exists():
        raise SystemExit('missing benchmark result; run sealed_mmt_benchmark_v4_4.py first')
    r=json.loads(RESULT.read_text())
    v43=json.loads(V43.read_text())
    issues=[]
    if v43.get('operator_trace_sha256') != EXPECTED:
        issues.append('V43_OPERATOR_SHA_MISMATCH')
    if r.get('frozen_operator_trace_sha256') != EXPECTED:
        issues.append('RESULT_FROZEN_SHA_MISMATCH')
    if r.get('operator_mutated_after_freeze') is not False:
        issues.append('OPERATOR_MUTATION_NOT_FALSE')
    if r.get('fitted_parameters_used') is not False:
        issues.append('FITTED_PARAMETERS_NOT_FALSE')
    if r.get('reference_spectrum_execution_claimed') is not False:
        issues.append('REFERENCE_EXECUTION_CLAIM_PRESENT')
    if r.get('mass_prediction_claimed') is not False:
        issues.append('MASS_PREDICTION_CLAIM_PRESENT')
    if r.get('observed_masses_used_by_operator') is not False:
        issues.append('OBSERVED_MASSES_USED_BY_OPERATOR')
    if r.get('benchmark_performed') is not True:
        issues.append('BENCHMARK_NOT_PERFORMED')
    if r.get('current_promotion') != 'DENY_CURRENT':
        issues.append('CURRENT_NOT_DENIED')
    if r.get('canon_allowed') is not False:
        issues.append('CANON_ALLOWED_TRUE')
    if r.get('status') != 'SEALED_BENCHMARK_FAIL_NUMERIC_DEBT9_REMAINS_OPEN':
        issues.append('UNEXPECTED_STATUS_REVIEW_REQUIRED')
    # Ensure active frozen operator script still has no benchmark reference snapshot access.
    op_script = ROOT/'43_debt9_metatime_mass_operator_freeze_v4_3'/'scripts'/'metatime_mass_operator_freeze_v4_3.py'
    op_text = op_script.read_text(encoding='utf-8')
    forbidden_runtime_patterns = ['benchmark_reference_snapshot', 'masses_mev', '105.658', '172760.0', '0.51099895']
    for pat in forbidden_runtime_patterns:
        if pat in op_text:
            issues.append('REFERENCE_LEAK_IN_FROZEN_OPERATOR:'+pat)
    out={
        'schema':'VALIDATION_MODULE44_V4_4',
        'status':'PASS' if not issues else 'FAIL',
        'issues':issues,
        'doctor_verdict':'CONTINUE_RESEARCH_DENY_CANON_DENY_CURRENT' if not issues else 'QUARANTINE',
        'debt9_numeric_spectrum_status':'OPEN_NOT_CLOSED',
    }
    (MODULE/'results'/'VALIDATION_MODULE44_v4_4.json').write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps(out, indent=2))
    if issues:
        raise SystemExit(1)
if __name__=='__main__': main()
