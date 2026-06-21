#!/usr/bin/env python3
"""Validation for module 43. Tests executable purity and frozen-operator outputs."""
from __future__ import annotations
import json, pathlib, subprocess, sys, zipfile, hashlib, re, math

MOD = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = MOD / 'scripts' / 'metatime_mass_operator_freeze_v4_3.py'
RESULT = MOD / 'results' / 'metatime_mmt_freeze_v4_3.json'

# Real executable contamination scan. This intentionally scans only the active executable,
# not this validator or prose reports, because prose may mention banned classes as guardrails.
FORBIDDEN_EXEC_TOKENS = [
    'PDG =', 'PDG[', 'mass_ref', 'reference_mass', 'reference_spectrum',
    'NoParamSM', 'noparamSMsolver', 'ckm_matrix', 'pmns_matrix',
    '0.510998', '105.658', '1776.86', '172760', '4.18', '1.27',
]

issues = []
text = SCRIPT.read_text(encoding='utf-8')
for tok in FORBIDDEN_EXEC_TOKENS:
    if tok in text:
        issues.append(f'forbidden executable token: {tok}')

# Run operator script.
proc = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, cwd=str(MOD))
if proc.returncode != 0:
    issues.append(f'operator script failed: {proc.stderr[-500:]}')
if not RESULT.exists():
    issues.append('result json missing after execution')
else:
    data = json.loads(RESULT.read_text(encoding='utf-8'))
    if data.get('mass_prediction_claimed') is not False:
        issues.append('mass_prediction_claimed must be false')
    if data.get('pdg_reference_input_used') is not False:
        issues.append('pdg_reference_input_used must be false')
    if data.get('observed_masses_used') is not False:
        issues.append('observed_masses_used must be false')
    if data.get('fitted_parameters_used') is not False:
        issues.append('fitted_parameters_used must be false')
    traces = data.get('traces', [])
    if len(traces) != 9:
        issues.append(f'expected 9 charged-fermion slots, got {len(traces)}')
    for tr in traces:
        if tr.get('physical_mass_prediction_claimed') is not False:
            issues.append(f"slot {tr.get('slot')} claims physical mass prediction")
        amp = tr.get('dimensionless_mmt_amplitude_frozen')
        logt = tr.get('log_yukawa_trace_frozen')
        if not isinstance(amp, (int,float)) or not (amp > 0) or not math.isfinite(float(amp)):
            issues.append(f"slot {tr.get('slot')} invalid amplitude")
        if not isinstance(logt, (int,float)) or not math.isfinite(float(logt)):
            issues.append(f"slot {tr.get('slot')} invalid log trace")
    # Verify trace fingerprint reproducibility from traces only.
    trace_json = json.dumps(traces, sort_keys=True, separators=(',', ':'))
    fp = hashlib.sha256(trace_json.encode('utf-8')).hexdigest()
    if fp != data.get('operator_trace_sha256'):
        issues.append('operator trace sha256 mismatch')

status = 'PASS' if not issues else 'FAIL'
out = {
    'schema': 'VALIDATION_MODULE43_V4_3',
    'status': status,
    'issues': issues,
    'notes': [
        'This validates a frozen PDG-free operator candidate only.',
        'It intentionally does not benchmark or compute physical masses.',
        'Debt 9 numeric spectrum remains open until a sealed future benchmark uses this exact fingerprint.',
    ],
}
(MOD / 'results' / 'VALIDATION_MODULE43_v4_3.json').write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
print(json.dumps(out, indent=2))
sys.exit(0 if status == 'PASS' else 1)
