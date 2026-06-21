#!/usr/bin/env python3
from __future__ import annotations
import json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[0]
FORBIDDEN_CODE_PATTERNS = [
    r"\b" + "PD" + "G" + r"\s*=\s*\{",
    "mass" + "_ref" + r"\s*=",
    "reference" + "_masses",
    "CK" + "M" + r"\s*=\s*\[",
    "PM" + "NS" + r"\s*=\s*\[",
]
FORBIDDEN_NUMERIC_MASS_TOKENS = [
    "0.510" + "998", "0.511" + "000", "105." + "658", "1776" + ".86",
    "172" + "760", "173" + "000", "2.524" + "e-3", "7.53" + "e-5"
]

def scan_file(path: Path, patterns):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    hits = []
    for pat in patterns:
        if re.search(pat, txt):
            hits.append(pat)
    return hits

script_files = sorted((ROOT / 'scripts').glob('*.py'))
result_files = [p for p in sorted((ROOT / 'results').glob('*')) if not p.name.startswith('VALIDATION_MODULE38')]
code_hits = {str(p.relative_to(ROOT)): scan_file(p, FORBIDDEN_CODE_PATTERNS) for p in script_files}
code_hits = {k:v for k,v in code_hits.items() if v}
num_hits = {}
for p in script_files + [x for x in result_files if x.is_file()]:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    hits = [tok for tok in FORBIDDEN_NUMERIC_MASS_TOKENS if tok in txt]
    if hits:
        num_hits[str(p.relative_to(ROOT))] = hits

# Current whole repo may contain historical/quarantine zip references in text, but must not contain nested archive files.
nested_archives = [str(p.relative_to(REPO)) for p in REPO.rglob('*') if p.is_file() and p.suffix.lower() == '.zip']

# Execute JSON outputs have required non-prediction flags.
struct = json.loads((ROOT / 'results' / 'pdg_free_structural_signature_v3_8.json').read_text())
hyp = json.loads((ROOT / 'results' / 'sm_hypercharge_anomaly_derivation_v3_8.json').read_text())
struct_mass_claims = []
for row in struct.get('all_twin_prime_seed_signatures', []):
    if row.get('mass_prediction_claimed') is not False:
        struct_mass_claims.append(row.get('seed_pair'))
checks_zero = hyp.get('all_checks_zero') is True

status = 'PASS'
issues = []
if code_hits:
    status = 'FAIL'; issues.append({'code_forbidden_pattern_hits': code_hits})
if num_hits:
    status = 'FAIL'; issues.append({'forbidden_numeric_mass_token_hits': num_hits})
if nested_archives:
    status = 'FAIL'; issues.append({'nested_archives': nested_archives})
if struct_mass_claims:
    status = 'FAIL'; issues.append({'structural_rows_claiming_mass_prediction': struct_mass_claims})
if not checks_zero:
    status = 'FAIL'; issues.append({'hypercharge_checks_zero': False})

payload = {
    'schema': 'METATIME_SM_MODULE38_VALIDATION_V3_8',
    'status': status,
    'scope': 'active module v3.8 scripts/results plus no nested archives in repo',
    'checks': {
        'active_code_forbidden_PDG_table_patterns': not bool(code_hits),
        'active_outputs_forbidden_mass_tokens_absent': not bool(num_hits),
        'structural_signature_claims_no_masses': not bool(struct_mass_claims),
        'hypercharge_anomaly_and_yukawa_checks_zero': checks_zero,
        'no_nested_archives': not bool(nested_archives),
    },
    'issues': issues,
    'doctor_verdict': 'CONTINUE_RESEARCH__MODULE38_GUARD_PASS' if status == 'PASS' else 'STOP_CRITICAL',
}
(ROOT / 'results' / 'VALIDATION_MODULE38_v3_8.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
print(json.dumps(payload, indent=2))
