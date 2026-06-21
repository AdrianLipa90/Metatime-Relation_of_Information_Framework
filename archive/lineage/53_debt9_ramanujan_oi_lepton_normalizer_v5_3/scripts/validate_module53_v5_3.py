#!/usr/bin/env python3
from __future__ import annotations
import json, sys, zipfile
from pathlib import Path
MODULE=Path(__file__).resolve().parents[1]
ROOT=MODULE.parents[0]
RESULT=MODULE/'results'/'ramanujan_oi_lepton_normalizer_v5_3.json'
SCRIPT=MODULE/'scripts'/'ramanujan_oi_lepton_normalizer_v5_3.py'
FORBIDDEN_EXEC_TOKENS=['mass_ref','reference_spectrum_execution','ARCHIVE_CANONICAL_SPECTRUM','noparamSMsolver.py']

def main():
    issues=[]
    if not RESULT.exists(): issues.append('missing result json')
    else:
        obj=json.load(open(RESULT,encoding='utf-8'))
        if obj.get('mass_closure_claimed') is not False: issues.append('mass closure claim not false')
        if obj.get('observed_targets_used_in_operator') is not False: issues.append('observed targets marked as operator input')
        if obj.get('old_solver_used') is not False: issues.append('old solver marked used')
        if obj.get('table_replay_used') is not False: issues.append('table replay marked used')
        dec=obj.get('decision',{})
        if dec.get('debt9_numeric_spectrum')!='OPEN_NOT_CLOSED': issues.append('Debt 9 not left open')
        if dec.get('canon_allowed') is not False: issues.append('canon allowed unexpectedly')
    text=SCRIPT.read_text(encoding='utf-8')
    for tok in FORBIDDEN_EXEC_TOKENS:
        if tok in text:
            issues.append(f'forbidden executable token present: {tok}')
    nested=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.zip','.tar','.gz','.tgz','.bz2','.xz','.7z','.rar'}:
            nested.append(str(p.relative_to(ROOT)))
    if nested: issues.append('nested archives inside repo: '+repr(nested[:10]))
    status='PASS' if not issues else 'FAIL'
    out={'schema':'VALIDATION_MODULE53_V5_3','status':status,'issues':issues,'debt9_numeric_spectrum':'OPEN_NOT_CLOSED','canon_allowed':False}
    (MODULE/'results'/'VALIDATION_MODULE53_v5_3.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
    if issues: sys.exit(1)
if __name__=='__main__': main()
