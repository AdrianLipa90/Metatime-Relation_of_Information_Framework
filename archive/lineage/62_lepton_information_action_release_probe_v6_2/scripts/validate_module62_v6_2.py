#!/usr/bin/env python3
from __future__ import annotations
import json, py_compile, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parents[1]
SCRIPT = MODULE_DIR/'scripts/lepton_information_action_release_probe_v6_2.py'
RESULT = MODULE_DIR/'results/lepton_information_action_release_probe_v6_2.json'

issues=[]
try:
    py_compile.compile(str(SCRIPT), doraise=True)
except Exception as e:
    issues.append(f'active script compile failed: {e}')
if not RESULT.exists():
    issues.append('missing result json')
else:
    data=json.loads(RESULT.read_text(encoding='utf-8'))
    if data.get('debt9_numeric_spectrum') != 'OPEN_NOT_CLOSED': issues.append('Debt9 not open')
    if data.get('mass_prediction_claimed') is not False: issues.append('mass prediction claimed')
    if data.get('absolute_action_derived') is not False: issues.append('absolute action derived claimed')
    if data.get('canon_allowed') is not False or data.get('current_promotion') != 'DENY_CURRENT': issues.append('canon/current promotion not denied')
    guard=data.get('guardrails', {})
    if guard.get('target_actions_used_in_candidate_rule') is not False: issues.append('target actions used in candidate rule')
    rows=data.get('transition_rows', [])
    if len(rows) != 3: issues.append(f'expected 3 transition rows, got {len(rows)}')
    # keep thresholds wide enough to validate signal, not closure
    if rows and rows[0]['action_relative_error_abs'] > 0.02: issues.append('e->mu signal too weak for v6.2 claim')
    if rows and rows[1]['action_relative_error_abs'] > 0.08: issues.append('mu->tau partial signal too weak for v6.2 claim')
# no nested archives inside repo
nested=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.zip','.tar','.gz','.tgz','.bz2','.xz','.7z','.rar'}:
        nested.append(str(p.relative_to(ROOT)))
if nested: issues.append('nested archives found: '+repr(nested[:5]))
status='PASS' if not issues else 'FAIL'
out={'schema':'VALIDATION_MODULE62_V6_2','status':status,'issues':issues,'checked_script':str(SCRIPT.relative_to(ROOT))}
(MODULE_DIR/'results'/'VALIDATION_MODULE62_v6_2.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(out, indent=2, ensure_ascii=False))
if issues: sys.exit(1)
