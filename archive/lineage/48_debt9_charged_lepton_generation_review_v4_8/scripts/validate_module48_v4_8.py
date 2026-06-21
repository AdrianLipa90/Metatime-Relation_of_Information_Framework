#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
MODULE_DIR = pathlib.Path(__file__).resolve().parents[1]
ROOT = MODULE_DIR.parents[0]
SCRIPT = MODULE_DIR / 'scripts' / 'charged_lepton_generation_review_v4_8.py'
RESULT = MODULE_DIR / 'results' / 'charged_lepton_generation_review_v4_8.json'
FORBIDDEN_ACTIVE_SCRIPT_TOKENS = [
    'NoParamSM',
    'ARCHIVE_CANONICAL_SPECTRUM',
    'mass_ref',
    'reference_spectrum_execution',
]

def main():
    issues=[]
    if not RESULT.exists(): issues.append('missing result json')
    txt = SCRIPT.read_text(encoding='utf-8')
    for token in FORBIDDEN_ACTIVE_SCRIPT_TOKENS:
        if token in txt:
            issues.append(f'forbidden token in active executable: {token}')
    if RESULT.exists():
        r=json.loads(RESULT.read_text(encoding='utf-8'))
        if r.get('technical_status')!='PASS': issues.append('technical status not PASS')
        if r.get('debt9_numeric_spectrum')!='OPEN_NOT_CLOSED': issues.append('Debt 9 was incorrectly closed')
        if r.get('canon_allowed') is not False: issues.append('canon allowed must be false')
        if r.get('current_promotion')!='DENY_CURRENT': issues.append('current promotion must be denied')
        rows=r.get('candidate_rows',[])
        if not rows: issues.append('no candidate rows')
        for row in rows:
            if row.get('debt9_numeric_closure_allowed') is not False:
                issues.append('candidate row allows closure')
            if row.get('mass_prediction_claimed') is not False:
                issues.append('candidate row claims mass prediction')
        if 'candidate_summary_ranked_by_mean_error_excluding_e_anchor' not in r:
            issues.append('missing candidate summary')
    nested=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.zip','.tar','.gz','.tgz','.bz2','.xz','.7z','.rar'}:
            nested.append(str(p.relative_to(ROOT)))
    if nested: issues.append('nested archive(s): '+', '.join(nested[:10]))
    out={
        'schema':'VALIDATION_MODULE48_V4_8',
        'status':'PASS' if not issues else 'FAIL',
        'issues':issues,
        'checked_nested_archives_count':len(nested),
        'active_script':str(SCRIPT.relative_to(ROOT)),
        'result_json':str(RESULT.relative_to(ROOT)),
    }
    (MODULE_DIR/'results'/'VALIDATION_MODULE48_v4_8.json').write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps(out, indent=2))
    if issues: sys.exit(1)
if __name__=='__main__': main()
