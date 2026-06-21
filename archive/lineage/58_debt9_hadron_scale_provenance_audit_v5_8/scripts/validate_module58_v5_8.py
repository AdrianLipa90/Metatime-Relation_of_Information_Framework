#!/usr/bin/env python3
import json, zipfile, sys, py_compile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parents[1]
res_path = MODULE_DIR / 'results' / 'hadron_scale_provenance_audit_v5_8.json'
res = json.loads(res_path.read_text(encoding='utf-8'))
issues=[]
if res['technical_status'] != 'PASS': issues.append('technical_status_not_PASS')
if res['decision']['small_errors_as_such'] != 'NOT_A_REASON_FOR_REJECTION': issues.append('small_error_policy_not_corrected')
if res['decision']['SM_and_M_Theory_exact_table'] != 'HOLD_AS_PROVENANCE_REQUIRED_NOT_DEBT9_CLOSURE': issues.append('exact_table_wrong_classification')
if res['scale_provenance_tests']['non_mass_hadron_MeV_scale_found'] is not False: issues.append('non_mass_scale_wrongly_claimed')
if res['mass_prediction_claimed'] is not False: issues.append('mass_prediction_claimed')
if res['canon_allowed'] is not False: issues.append('canon_allowed')
if res['decision']['F_hadron_geometric_mean'] != 'PRESERVE_AS_STRUCTURAL_OPERATOR_CANDIDATE': issues.append('F_hadron_not_preserved')
py_compile.compile(str(MODULE_DIR/'scripts'/'hadron_scale_provenance_audit_v5_8.py'), doraise=True)
status='PASS' if not issues else 'FAIL'
out={'module':'58_debt9_hadron_scale_provenance_audit_v5_8','validation_status':status,'issues':issues}
(MODULE_DIR/'results'/'VALIDATION_MODULE58_v5_8.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
if issues: sys.exit(1)
