#!/usr/bin/env python3
from __future__ import annotations
import json, py_compile, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MODULE = Path(__file__).resolve().parents[1]
RESULT = MODULE/'results/planck_information_action_ledger_v6_1.json'
SCRIPT = MODULE/'scripts/planck_information_action_ledger_v6_1.py'
issues=[]
if not RESULT.exists(): issues.append('missing result')
else:
    d=json.loads(RESULT.read_text(encoding='utf-8'))
    if d.get('technical_status') != 'PASS': issues.append('technical status not PASS')
    if d.get('debt9_numeric_spectrum') != 'OPEN_NOT_CLOSED': issues.append('Debt9 not open')
    if d.get('mass_prediction_claimed') is not False: issues.append('mass prediction claimed')
    if d.get('canon_allowed') is not False or d.get('current_promotion') != 'DENY_CURRENT': issues.append('canon/current not denied')
    if d.get('decision',{}).get('planck_E0_candidate') != 'PROMOTE_TO_PRIMARY_DIMENSIONAL_CANDIDATE': issues.append('Planck E0 candidate not promoted to primary candidate')
    if len(d.get('target_action_rows',[])) < 5: issues.append('too few targets')
    if not any(p.get('pair')=='electron->muon' for p in d.get('action_release_pairs',[])): issues.append('missing electron->muon release')
text=SCRIPT.read_text(encoding='utf-8')
for forbidden in ['import NoParamSM','from NoParamSM','noparamSMsolver','mass_ref =','reference_spectrum_execution']:
    if forbidden in text: issues.append('forbidden active token: '+forbidden)
try:
    py_compile.compile(str(SCRIPT), doraise=True)
except Exception as e:
    issues.append('script compile failed: '+repr(e))
nested=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.zip','.tar','.gz','.tgz','.bz2','.xz','.7z','.rar'}:
        nested.append(str(p.relative_to(ROOT)))
if nested: issues.append('nested archives: '+repr(nested[:5]))
out={'schema':'VALIDATION_MODULE61_V6_1','status':'PASS' if not issues else 'FAIL','issues':issues}
(MODULE/'results/VALIDATION_MODULE61_v6_1.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
if issues: sys.exit(1)
