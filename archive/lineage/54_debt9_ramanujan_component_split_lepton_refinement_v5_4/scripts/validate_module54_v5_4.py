#!/usr/bin/env python3
from __future__ import annotations
import json, zipfile
from pathlib import Path
MODULE=Path(__file__).resolve().parents[1]
ROOT=MODULE.parents[0]
RESULT=MODULE/'results'/'ramanujan_component_split_lepton_refinement_v5_4.json'
SCRIPT=MODULE/'scripts'/'ramanujan_component_split_lepton_refinement_v5_4.py'
FORBIDDEN_EXEC_TOKENS=['mass_ref','reference_spectrum_execution','ARCHIVE_CANONICAL_SPECTRUM','noparamSMsolver.py']

def main():
    issues=[]
    if not RESULT.exists(): issues.append('missing result json')
    else:
        obj=json.load(open(RESULT,encoding='utf-8'))
        if obj.get('mass_closure_claimed') is not False: issues.append('mass_closure_claimed must remain false')
        if obj.get('observed_targets_used_in_operator') is not False: issues.append('observed targets used in operator')
        if obj.get('new_free_parameter_added') is not False: issues.append('new free parameter added')
        if obj.get('decision',{}).get('debt9_numeric_spectrum')!='OPEN_NOT_CLOSED': issues.append('Debt 9 must remain open')
        if obj.get('decision',{}).get('canon_allowed') is not False: issues.append('canon allowed unexpectedly')
        if obj.get('metrics',{}).get('mean_absolute_relative_error_excluding_e_anchor', 999) >= obj.get('metrics',{}).get('v5_3_mean_absolute_relative_error_excluding_e_anchor', -1):
            issues.append('no improvement over v5.3 diagnostic')
    text=SCRIPT.read_text(encoding='utf-8')
    for tok in FORBIDDEN_EXEC_TOKENS:
        if tok in text:
            issues.append(f'forbidden executable token present: {tok}')
    nested=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.zip','.tar','.gz','.tgz','.7z','.rar'}:
            nested.append(str(p.relative_to(ROOT)))
    if nested: issues.append('nested archives present: '+str(nested[:5]))
    out={'schema':'VALIDATION_MODULE54_V5_4','status':'PASS' if not issues else 'FAIL','issues':issues,'debt9_numeric_spectrum':'OPEN_NOT_CLOSED','canon_allowed':False}
    (MODULE/'results'/'VALIDATION_MODULE54_v5_4.json').write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps(out,indent=2))
    return 0 if not issues else 1
if __name__=='__main__': raise SystemExit(main())
