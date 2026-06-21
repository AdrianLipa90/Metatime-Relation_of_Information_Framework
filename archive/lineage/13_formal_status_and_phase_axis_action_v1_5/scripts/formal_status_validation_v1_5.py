#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
ROOT = Path(__file__).resolve().parents[2]
MODULE = Path(__file__).resolve().parents[1]
archive_exts = {'.zip','.tar','.gz','.tgz','.rar','.7z','.bz2','.xz'}
# include .tar.gz by name check too
archives=[]
for p in ROOT.rglob('*'):
    if p.is_file():
        name=p.name.lower()
        if any(name.endswith(ext) for ext in archive_exts) or name.endswith('.tar.gz'):
            archives.append(str(p.relative_to(ROOT)))
ledger=MODULE/'FORMAL_STATUS_LEDGER_v1_5.csv'
allowed={'definition','ansatz','lemma','proof','interpretation','hypothesis','validation_gate','formal_debt'}
bad=[]
with ledger.open(newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['status'] not in allowed:
            bad.append(row)
required_terms=['definition','ansatz','lemma','proof','interpretation','hypothesis','validation_gate','formal_debt']
text=(MODULE/'METATIME_SM_FORMAL_STATUS_PHASE_AXIS_ACTION_v1_5.md').read_text(encoding='utf-8').lower()
missing=[t for t in required_terms if t not in text]
result={
 'nested_archives_found': archives,
 'formal_status_bad_rows': bad,
 'required_terms_missing': missing,
 'pass': not archives and not bad and not missing
}
out=MODULE/'results'/'formal_status_validation_v1_5.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
if not result['pass']:
    sys.exit(1)
