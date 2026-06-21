#!/usr/bin/env python3
from __future__ import annotations
import json, py_compile, sys
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
RESULT = MODULE/'results'/'information_energy_normalizer_v6_0B.json'
SCRIPT = MODULE/'scripts'/'information_energy_normalizer_v6_0B.py'

def main():
    py_compile.compile(str(SCRIPT), doraise=True)
    data = json.loads(RESULT.read_text(encoding='utf-8'))
    issues=[]
    if data.get('technical_status') != 'PASS': issues.append('technical_status not PASS')
    if data.get('absolute_E0_derived') is not False: issues.append('absolute_E0_derived must be false')
    if data.get('mass_prediction_claimed') is not False: issues.append('mass_prediction_claimed must be false')
    if data.get('debt9_numeric_spectrum') != 'OPEN_NOT_CLOSED': issues.append('Debt9 must remain open')
    if data.get('decision',{}).get('pure_information_without_E0') != 'DENIED_BY_DIMENSIONAL_ANALYSIS': issues.append('dimensional denial missing')
    if len(data.get('formula_fingerprint_sha256','')) != 64: issues.append('bad fingerprint')
    nested=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.zip','.tar','.gz','.tgz','.bz2','.xz','.7z','.rar'}:
            nested.append(str(p.relative_to(ROOT)))
    if nested: issues.append('nested archives found: '+str(nested[:5]))
    out = {'schema':'VALIDATION_INFORMATION_ENERGY_NORMALIZER_V6_0B','status':'PASS' if not issues else 'FAIL','issues':issues}
    (MODULE/'results'/'VALIDATION_MODULE60B_v6_0B.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))
    if issues: sys.exit(1)
if __name__ == '__main__': main()
