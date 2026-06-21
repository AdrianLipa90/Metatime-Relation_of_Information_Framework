#!/usr/bin/env python3
import json, sys, math
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'results' / 'SEALED_CHARGED_LEPTON_RECONSTRUCTION_BENCHMARK_v6_9.json'
data = json.loads(p.read_text(encoding='utf-8'))
assert data['technical_status'] == 'PASS'
assert data['canon_allowed'] is False
assert data['mass_spectrum_closure_claimed'] is False
pol = data['input_policy']
for key in ['uses_electron_mass_as_input','uses_muon_mass_as_input','uses_tau_mass_as_input','uses_pdg_tables_as_input','uses_exact_replay_tables_as_input','uses_v6_1_target_actions_as_input']:
    assert pol[key] is False, key
assert len(data['prediction_rows']) == 3
assert data['metrics']['max_abs_relative_error_percent'] < 6.0
assert data['decision']['mass_spectrum_closure'] == 'DENIED'
print('VALIDATION_MODULE69_v6_9 PASS')
