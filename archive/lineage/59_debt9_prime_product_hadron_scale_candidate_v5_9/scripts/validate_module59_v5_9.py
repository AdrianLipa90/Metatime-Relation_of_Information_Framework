#!/usr/bin/env python3
import json, zipfile, sys, py_compile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MODULE = Path(__file__).resolve().parents[1]
res = json.loads((MODULE/'results'/'prime_product_hadron_scale_candidate_v5_9.json').read_text(encoding='utf-8'))
issues=[]
if res['technical_status']!='PASS': issues.append('technical_status not PASS')
if res['mass_prediction_claimed']: issues.append('mass prediction claimed')
if res['benchmark_performed']: issues.append('benchmark performed in freeze module')
for key,val in res['guardrails'].items():
    if key=='nested_archives_allowed':
        if val is not False: issues.append('nested archive flag not false')
    elif val is not False:
        issues.append(f'guardrail expected false: {key}')
if res['debt9_numeric_spectrum']!='OPEN_NOT_CLOSED': issues.append('Debt 9 incorrectly closed')
if not res['formula_fingerprint_sha256'] or len(res['formula_fingerprint_sha256'])!=64: issues.append('bad fingerprint')
if not res['rows']: issues.append('no rows')
# Active script compile check.
for p in (MODULE/'scripts').glob('*.py'):
    py_compile.compile(str(p), doraise=True)
# Check no nested archives in current root.
nested=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.zip','.7z','.rar','.tar','.tgz','.gz'}:
        # allow no nested archives at all inside repo
        nested.append(str(p.relative_to(ROOT)))
if nested: issues.append('nested archives found: '+str(nested[:5]))
out={'module':'59','status':'PASS' if not issues else 'FAIL','issues':issues,'checked_rows':len(res['rows'])}
(MODULE/'results'/'VALIDATION_MODULE59_v5_9.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
if issues: sys.exit(1)
