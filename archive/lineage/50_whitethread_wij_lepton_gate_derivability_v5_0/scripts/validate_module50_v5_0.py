#!/usr/bin/env python3
from __future__ import annotations
import json, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOD = Path(__file__).resolve().parents[1]
SCRIPT = MOD / 'scripts' / 'whitethread_wij_lepton_gate_derivability_v5_0.py'
RESULT = MOD / 'results' / 'whitethread_wij_lepton_gate_derivability_v5_0.json'
errors = []
if not RESULT.exists():
    errors.append('missing result JSON')
else:
    obj = json.loads(RESULT.read_text(encoding='utf-8'))
    if obj.get('mass_prediction_claimed') is not False:
        errors.append('mass prediction claim must be false')
    if obj.get('benchmark_performed') is not False:
        errors.append('benchmark must not be performed')
    if obj.get('decision',{}).get('large_document_F_table_promoted') is not False:
        errors.append('large document F table must not be promoted')
    if obj.get('debt9_numeric_spectrum') != 'OPEN_NOT_CLOSED':
        errors.append('Debt 9 numeric status must remain open')
    for row in obj.get('rows', []):
        if row.get('short_doc_derives_document_F') is not False:
            errors.append('row incorrectly promotes strong F derivation')

text = SCRIPT.read_text(encoding='utf-8')
for forbidden in ['import NoParamSM', 'noparamSMsolver', 'PDG =', 'mass_calc == reference']:
    if forbidden in text:
        errors.append(f'forbidden executable token found: {forbidden}')

nested = []
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.zip', '.tar', '.gz', '.tgz', '.rar', '.7z'}:
        # The repo should not contain nested archives other than original unpacked source files; in this line we forbid all active archives.
        nested.append(str(p.relative_to(ROOT)))
if nested:
    errors.append('nested archives present: ' + '; '.join(nested[:10]))

out = {'schema':'VALIDATION_MODULE50_v5_0','status':'FAIL' if errors else 'PASS','errors':errors,
       'checks':['result exists','no benchmark','no mass claim','large F not promoted','active executable scan','nested archive scan']}
(MOD/'results/VALIDATION_MODULE50_v5_0.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(out, indent=2, ensure_ascii=False))
raise SystemExit(1 if errors else 0)
