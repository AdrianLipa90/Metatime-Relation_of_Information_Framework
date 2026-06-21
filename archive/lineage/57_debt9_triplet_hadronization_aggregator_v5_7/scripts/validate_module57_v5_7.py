#!/usr/bin/env python3
import json, sys, py_compile
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[1]
ROOT = MODULE_DIR.parents[0]
script = MODULE_DIR / 'scripts' / 'triplet_hadronization_aggregator_v5_7.py'
result_path = MODULE_DIR / 'results' / 'triplet_hadronization_aggregator_v5_7.json'

py_compile.compile(str(script), doraise=True)
result = json.loads(result_path.read_text(encoding='utf-8'))
script_text = script.read_text(encoding='utf-8')
# Scan only active operator import/exec patterns, not historical docs.
forbidden_patterns = [
    'from NoParamSM', 'import NoParamSM', 'noparamSMsolver(', 'PDG[', 'mass_ref', 'reference_spectrum_execution'
]
checks = {
    'result_exists': result_path.exists(),
    'debt9_open': result.get('debt9_numeric_spectrum') == 'OPEN_NOT_CLOSED',
    'no_mass_prediction_claim': result.get('mass_prediction_claimed') is False,
    'canon_denied': result.get('canon_allowed') is False and result.get('current_promotion') == 'DENY_CURRENT',
    'triplet_rows_present': len(result.get('hadron_rows', [])) >= 4,
    'single_quark_exact_denied': result['decision']['quark_single_state_exact_scoring'] == 'DENIED',
    'readme_exact_hadron_table_denied': result['decision']['readme_exact_hadron_table_promotion'].startswith('DENIED'),
    'mu0_anchor_denied': result['decision']['hadron_scale_mu0_promotion'].startswith('DENIED'),
    'all_rows_no_mass_claim': all(r['mass_prediction_mev_claimed'] is False for r in result['hadron_rows']),
    'all_rows_triplet_required': all(r['tetrahedral_triplet_required'] and r['W_ij_loop_required'] for r in result['hadron_rows']),
    'all_rows_binding_dominated_under_21percent': result['metrics']['all_rows_binding_dominated_under_21_percent_proxy_fraction'] is True,
    'no_old_solver_import_or_reference_replay_in_active_script': not any(p in script_text for p in forbidden_patterns),
    'active_script_compiles': True,
}
status = 'PASS' if all(checks.values()) else 'FAIL'
out = {'schema':'VALIDATION_MODULE57_V5_7', 'module':'57_debt9_triplet_hadronization_aggregator_v5_7', 'status':status, 'checks':checks}
(MODULE_DIR/'results'/'VALIDATION_MODULE57_v5_7.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
if status != 'PASS': sys.exit(1)
