#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
RESULT = MODULE/'results'/'debt9_lepton_freeze_full_sector_boundary_v5_5.json'
SCRIPT = MODULE/'scripts'/'debt9_lepton_freeze_full_sector_boundary_v5_5.py'

def fail(msg):
    print('FAIL:', msg)
    sys.exit(1)

def main():
    if not RESULT.exists(): fail('missing result json')
    data = json.loads(RESULT.read_text(encoding='utf-8'))
    if data['technical_status'] != 'PASS': fail('technical status not PASS')
    if data['mass_closure_claimed'] is not False: fail('mass closure claimed')
    if data['debt9_numeric_spectrum'] != 'OPEN_NOT_CLOSED': fail('debt9 status not open')
    if data['decision']['blind_full_sector_extension'] != 'FAIL_AND_DENY_PROMOTION': fail('blind extension not denied')
    if data['metrics']['charged_leptons_v5_5_freeze_mean_error_excluding_e_anchor'] > 0.05: fail('lepton freeze no longer matches v5.4 quality')
    if data['metrics']['blind_extension_passes_full_sector'] is not False: fail('blind full-sector extension incorrectly passed')
    text = SCRIPT.read_text(encoding='utf-8')
    hard_forbidden = ['noparamSMsolver.py', 'mass_ref =', 'PDG[']
    for token in hard_forbidden:
        if token in text:
            fail(f'hard forbidden active token found in executable: {token}')
    out = {
        'schema': 'VALIDATION_MODULE55_V5_5',
        'status': 'PASS',
        'checks': {
            'result_exists': True,
            'no_mass_closure_claim': True,
            'debt9_open': True,
            'blind_full_sector_extension_denied': True,
            'active_executable_forbidden_tokens_absent': True,
        },
        'module': MODULE.name,
    }
    (MODULE/'results'/'VALIDATION_MODULE55_v5_5.json').write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
