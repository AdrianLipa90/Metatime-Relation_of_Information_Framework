#!/usr/bin/env python3
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
path = ROOT/'results/EXACT_TABLE_REPLAY_PDG_PROVENANCE_MATRIX_v6_4.json'
data=json.loads(path.read_text(encoding='utf-8'))
allowed=set(data['allowed_classes'])
required=['id','name','classification','source_path','evidence_path','module_origin','reason','risk','permitted_use','blocked_use','doctor_verdict']
errors=[]
ids=set()
for row in data['rows']:
    for key in required:
        if key not in row or row[key] in (None,''):
            errors.append(f"missing {key} in {row.get('id')}")
    if row.get('classification') not in allowed:
        errors.append(f"bad classification {row.get('classification')} in {row.get('id')}")
    if row.get('id') in ids:
        errors.append(f"duplicate id {row.get('id')}")
    ids.add(row.get('id'))
for required_id in ['TABLE-001','TABLE-002','TABLE-007','TABLE-017']:
    if required_id not in ids:
        errors.append(f"required matrix row missing {required_id}")
if data['summary'].get('unclassified_rows') != 0:
    errors.append('unclassified_rows must be 0')
if data['summary'].get('floating_rows') != 0:
    errors.append('floating_rows must be 0')
if 'DEBT-005' not in data.get('debts_closed',[]):
    errors.append('DEBT-005 not closed')
print(json.dumps({'result':'PASS' if not errors else 'FAIL','errors':errors,'row_count':len(data['rows']),'classifications':data['summary'].get('by_classification')}, indent=2))
sys.exit(0 if not errors else 1)
