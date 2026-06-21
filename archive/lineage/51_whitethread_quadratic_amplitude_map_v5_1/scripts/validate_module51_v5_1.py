#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = Path(__file__).resolve().parents[1]
RESULT = MODULE / 'results' / 'whitethread_quadratic_amplitude_map_v5_1.json'
SCRIPT = MODULE / 'scripts' / 'whitethread_quadratic_amplitude_map_v5_1.py'

FORBIDDEN_ACTIVE_TOKENS = [
    'NoParamSM',
    'ARCHIVE_CANONICAL_SPECTRUM',
    'mass_calc == reference',
    'pdg_id',
    'PDG =',
    'mass_ref',
]

errors = []
if not RESULT.exists():
    errors.append('result JSON missing')
else:
    data = json.loads(RESULT.read_text(encoding='utf-8'))
    for key, expected in [
        ('mass_prediction_claimed', False),
        ('benchmark_performed', False),
        ('observed_mass_input_used', False),
        ('reference_spectrum_input_used', False),
        ('canon_allowed', False),
    ]:
        if data.get(key) is not expected:
            errors.append(f'{key} expected {expected}, got {data.get(key)!r}')
    if data.get('debt9_numeric_spectrum') != 'OPEN_NOT_CLOSED':
        errors.append('Debt 9 numeric spectrum must remain open')
    diag = data.get('diagnostics', {})
    if not diag.get('root_gates_close_to_large_document_F'):
        errors.append('root gate diagnostic did not pass candidate threshold')
    if diag.get('all_pair_gate_derivation_passes'):
        errors.append('all-pair derivation unexpectedly passed; expected explicit all-pair failure boundary')

active_text = SCRIPT.read_text(encoding='utf-8')
for tok in FORBIDDEN_ACTIVE_TOKENS:
    if tok in active_text:
        errors.append(f'forbidden active executable token found: {tok}')

nested = []
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.zip', '.tar', '.gz', '.tgz', '.bz2', '.xz', '.7z', '.rar'}:
        nested.append(str(p.relative_to(ROOT)))
if nested:
    errors.append('nested archives found: ' + ', '.join(nested[:20]))

out = {
    'schema': 'VALIDATION_MODULE51_v5_1',
    'status': 'PASS' if not errors else 'FAIL',
    'errors': errors,
    'checks': [
        'result JSON exists',
        'no mass prediction',
        'no benchmark',
        'no observed/reference spectrum input',
        'active executable forbidden-token scan',
        'nested archive scan',
        'root gates pass only as candidate',
        'all-pair gate failure remains explicit',
    ],
}
(MODULE/'results'/'VALIDATION_MODULE51_v5_1.json').write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
print(json.dumps(out, indent=2))
sys.exit(0 if not errors else 1)
