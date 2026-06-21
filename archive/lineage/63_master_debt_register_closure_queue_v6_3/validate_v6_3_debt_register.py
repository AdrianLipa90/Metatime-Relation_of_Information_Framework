#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / '63_master_debt_register_closure_queue_v6_3' / 'MASTER_DEBT_REGISTER_v6_3.json'
ALLOWED = {'CLOSED','ACTIVE_NOW','BLOCKED_WITH_REASON','MERGED_INTO_DEPENDENCY','QUARANTINED_WITH_TRACE'}
ARCHIVE_EXTS = ('.zip','.tar','.tar.gz','.tgz','.gz','.7z','.rar','.bz2','.xz')

def main():
    data=json.loads(REG.read_text(encoding='utf-8'))
    debts=data['debts']
    bad=[d for d in debts if d.get('status') not in ALLOWED]
    if bad:
        print('FAIL unknown debt statuses', bad)
        return 1
    if not debts:
        print('FAIL empty debt register')
        return 1
    nested=[]
    for p in ROOT.rglob('*'):
        if p.is_file():
            s=p.name.lower()
            if s.endswith(ARCHIVE_EXTS):
                nested.append(str(p.relative_to(ROOT)))
    if nested:
        print('FAIL nested archives', nested)
        return 1
    missing=data.get('expected_module_dirs_missing') or []
    if missing:
        print('FAIL expected dirs missing', missing)
        return 1
    print('PASS v6.3 debt register validation')
    print('debts:', len(debts))
    print('nested_archives:', len(nested))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
