#!/usr/bin/env python3
import json, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
result = json.loads((root/'results'/'DOCUMENT_OPERATOR_SOURCE_INDEX_v6_6.json').read_text(encoding='utf-8'))
allowed = set(result['classification_boundary'].keys())
fail=[]
if result.get('operator_count') != len(result.get('index', [])):
    fail.append('operator_count_mismatch')
for entry in result['index']:
    if entry.get('status') not in allowed:
        fail.append(f"bad_status:{entry.get('operator_id')}:{entry.get('status')}")
    if entry.get('status') in {'SOURCE_INDEXED_CONTENT','SOURCE_INDEXED_MINIMAL_CONTENT'} and entry.get('content_files_count',0) <= 0:
        fail.append(f"content_status_without_content:{entry.get('operator_id')}")
    if not entry.get('priority_evidence') and entry.get('status') != 'BLOCKED_NO_SOURCE_FOUND':
        fail.append(f"no_priority_evidence:{entry.get('operator_id')}")
for forbidden in ['unknown','floating','later','implicit']:
    if any(str(entry.get('status','')).lower() == forbidden for entry in result['index']):
        fail.append(f'forbidden_status:{forbidden}')
print(json.dumps({'validator':'v6_6_document_operator_source_index','passed': not fail,'failures': fail,'operator_count': len(result['index'])}, indent=2))
sys.exit(1 if fail else 0)
