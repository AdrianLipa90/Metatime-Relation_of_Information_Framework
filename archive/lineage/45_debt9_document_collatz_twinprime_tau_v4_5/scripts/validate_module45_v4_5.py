#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, subprocess, sys, zipfile
MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = MODULE_DIR/'scripts'/'document_collatz_twinprime_tau_operator_v4_5.py'
RESULT = MODULE_DIR/'results'/'document_collatz_twinprime_tau_trace_v4_5.json'
OUT = MODULE_DIR/'results'

def main():
    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(MODULE_DIR), text=True, capture_output=True)
    issues=[]
    if proc.returncode != 0:
        issues.append({'severity':'STOP_CRITICAL','code':'EXECUTION_FAILED','stderr':proc.stderr[-2000:]})
    data = json.loads(RESULT.read_text(encoding='utf-8')) if RESULT.exists() else {}
    active_text = SCRIPT.read_text(encoding='utf-8')
    forbidden_active_tokens = [
        "'mass':", 'masses_mev', 'benchmark_reference', 'PDG =', 'mass_ref', 'reference_spectrum_execution', 'observed_masses_used_by_operator'
    ]
    for tok in forbidden_active_tokens:
        if tok in active_text:
            issues.append({'severity':'WARN_REVIEW_REQUIRED','code':'ACTIVE_EXECUTABLE_FORBIDDEN_TOKEN','token':tok})
    if data.get('benchmark_performed') is not False:
        issues.append({'severity':'STOP_CRITICAL','code':'BENCHMARK_SHOULD_NOT_RUN_IN_V45'})
    if data.get('mass_prediction_claimed') is not False:
        issues.append({'severity':'STOP_CRITICAL','code':'MASS_PREDICTION_CLAIMED_FORBIDDEN'})
    if data.get('L3_base_collatz_length_of_3') != 7:
        issues.append({'severity':'STOP_CRITICAL','code':'L3_BASE_MISMATCH'})
    if abs(data.get('information_quantum_ln2_over_24pi',0) - 0.009193150006360484) > 1e-15:
        issues.append({'severity':'STOP_CRITICAL','code':'INFO_QUANTUM_MISMATCH'})
    rows=data.get('rows',[])
    if len(rows) != 12:
        issues.append({'severity':'STOP_CRITICAL','code':'EXPECTED_12_ROWS','count':len(rows)})
    # Tainted source categories should be present rather than hidden.
    taints={r.get('origin_class') for r in rows}
    if 'tainted_power_law_anchor' not in taints or 'document_inconsistency_review' not in taints:
        issues.append({'severity':'WARN_REVIEW_REQUIRED','code':'TAINT_OR_INCONSISTENCY_NOT_EXPOSED','classes':sorted(taints)})
    status='PASS' if not any(i['severity']=='STOP_CRITICAL' for i in issues) else 'FAIL'
    validation={
        'schema':'VALIDATION_MODULE45_V4_5',
        'status':status,
        'doctor_verdict':'CONTINUE_PROXY' if status=='PASS' else 'STOP_CRITICAL',
        'issues':issues,
        'stdout':proc.stdout[-2000:],
        'stderr':proc.stderr[-2000:],
        'debt9_numeric_spectrum':'OPEN_NOT_CLOSED',
        'canon_allowed':False,
        'current_promotion':'DENY_CURRENT'
    }
    OUT.mkdir(exist_ok=True)
    (OUT/'VALIDATION_MODULE45_v4_5.json').write_text(json.dumps(validation, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if status=='PASS' else 1
if __name__ == '__main__':
    raise SystemExit(main())
