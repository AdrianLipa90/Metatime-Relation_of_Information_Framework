#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
MODULE = pathlib.Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
SCRIPT = MODULE/'scripts'/'sealed_charged_lepton_kernel_benchmark_v5_2.py'
RESULT = MODULE/'results'/'sealed_charged_lepton_kernel_benchmark_v5_2.json'
# Exact executable scan only. Keep this list out of operator logic.
FORBIDDEN = ['NoParamSM', 'ARCHIVE_CANONICAL_SPECTRUM', 'mass_ref', 'reference_spectrum_execution']
issues=[]
if not RESULT.exists():
    issues.append('missing result JSON')
else:
    data=json.loads(RESULT.read_text(encoding='utf-8'))
    if data.get('technical_status')!='PASS': issues.append('technical status not PASS')
    if data.get('sealed_benchmark_performed') is not True: issues.append('sealed benchmark flag missing')
    if data.get('mass_closure_claimed') is not False: issues.append('mass closure claimed unexpectedly')
    if data.get('observed_targets_used_in_operator') is not False: issues.append('observed targets used in operator')
    if data.get('operator_adjusted_after_scoring') is not False: issues.append('operator adjusted after scoring')
    dec=data.get('decision',{})
    if dec.get('debt9_numeric_spectrum')!='OPEN_NOT_CLOSED': issues.append('Debt 9 numeric spectrum not left open')
    if dec.get('canon_allowed') is not False: issues.append('canon allowed unexpectedly')
    if dec.get('current_promotion')!='DENY_CURRENT': issues.append('current promotion not denied')
    metrics=data.get('metrics',{})
    if metrics.get('passes_numeric_debt9_closure_threshold') is not False: issues.append('numeric closure threshold passed unexpectedly')
    rows=data.get('rows',[])
    if len(rows)!=3: issues.append('expected exactly 3 charged-lepton rows')
    for r in rows:
        if r.get('mass_closure_claimed') is not False: issues.append('row claims mass closure')
        if r.get('canon_allowed') is not False: issues.append('row allows canon')
text=SCRIPT.read_text(encoding='utf-8')
for tok in FORBIDDEN:
    if tok in text:
        issues.append(f'forbidden token in active executable: {tok}')
nested=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.zip','.tar','.gz','.tgz','.bz2','.xz','.7z','.rar'}:
        nested.append(str(p.relative_to(ROOT)))
if nested:
    issues.append('nested archives found: '+', '.join(nested[:20]))
out={'schema':'VALIDATION_MODULE52_v5_2','status':'PASS' if not issues else 'FAIL','issues':issues,'checks':['result JSON exists','sealed benchmark performed','no closure/canon/current promotion','active executable forbidden-token scan','nested archive scan']}
(MODULE/'results'/'VALIDATION_MODULE52_v5_2.json').write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
print(json.dumps(out, indent=2))
sys.exit(0 if not issues else 1)
