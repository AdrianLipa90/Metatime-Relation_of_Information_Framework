#!/usr/bin/env python3
import json, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
result = json.loads((root/'results'/'MU_TAU_RELEASE_REFINEMENT_GATE_v6_8.json').read_text())
errors=[]
policy=result['input_policy']
for key in ['uses_muon_mass_as_input','uses_tau_mass_as_input','uses_pdg_tables_as_input','uses_exact_replay_tables_as_input','uses_v6_1_action_targets_as_input']:
    if policy.get(key) is not False:
        errors.append(f'forbidden input flag not false: {key}')
if not result.get('formula_fingerprint_sha256'):
    errors.append('missing formula fingerprint')
if result.get('canon_allowed') is not False:
    errors.append('canon_allowed must be false')
if result.get('mass_spectrum_closure_claimed') is not False:
    errors.append('mass_spectrum_closure_claimed must be false')
if abs(result['scoring_only']['energy_ratio_rel_error']) > 0.01:
    errors.append('tau/muon energy ratio scoring error exceeds 1 percent gate')
if abs(result['scoring_only']['action_rel_error_vs_measured_ratio_target']) > 0.005:
    errors.append('mu_tau action scoring error exceeds 0.5 percent gate')
if errors:
    print(json.dumps({'status':'FAIL','errors':errors}, indent=2))
    sys.exit(1)
print(json.dumps({'status':'PASS','errors':[]}, indent=2))
