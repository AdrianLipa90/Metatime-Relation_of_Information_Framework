#!/usr/bin/env python3
from __future__ import annotations
import json, re
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

def scan_text(path: Path, patterns):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    return [pat for pat in patterns if re.search(pat, txt)]

script_files = sorted((ROOT/'scripts').glob('*.py'))
result_files = [p for p in sorted((ROOT/'results').glob('*')) if p.is_file() and not p.name.startswith('VALIDATION_MODULE39')]
code_hits = {str(p.relative_to(ROOT)): scan_text(p, FORBIDDEN_CODE_PATTERNS) for p in script_files}
code_hits = {k:v for k,v in code_hits.items() if v}
num_hits = {}
for p in script_files + result_files:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    hits = [tok for tok in FORBIDDEN_NUMERIC_MASS_TOKENS if tok in txt]
    if hits:
        num_hits[str(p.relative_to(ROOT))] = hits

nested_archives = [str(p.relative_to(REPO)) for p in REPO.rglob('*') if p.is_file() and p.suffix.lower() in {'.zip', '.tar', '.gz', '.tgz', '.bz2', '.7z'}]

payload_path = ROOT/'results'/'tetra_triplet_su3_lift_v3_9.json'
payload = json.loads(payload_path.read_text(encoding='utf-8'))
checks = {
    'status_pass': payload.get('status') == 'PASS',
    'mass_prediction_not_claimed': payload.get('mass_prediction_claimed') is False,
    'full_qcd_not_claimed': payload.get('full_qcd_claimed') is False,
    'tetrahedral_edge_modes_independent': payload.get('tetrahedron', {}).get('edge_modes_independent') is True,
    'tetrahedral_center_closure_zero': payload.get('tetrahedron', {}).get('centered_closure_sum') == ['0','0','0'],
    'cp2_carrier_complex_dimension_three': payload.get('cp2_su3_lift', {}).get('complex_dimension_before_projectivization') == 3,
    'finite_symmetry_not_enough_declared': payload.get('cp2_su3_lift', {}).get('finite_tetrahedral_symmetry_is_not_enough') is True,
    'gell_mann_generator_count_8': payload.get('gell_mann_su3_candidate_checks', {}).get('generator_count') == 8,
    'gell_mann_hermitian_traceless_normed': all([
        payload.get('gell_mann_su3_candidate_checks', {}).get('all_hermitian') is True,
        payload.get('gell_mann_su3_candidate_checks', {}).get('all_traceless') is True,
        payload.get('gell_mann_su3_candidate_checks', {}).get('trace_normalization_Tr_lambda_a_lambda_b_2_delta_ab') is True,
    ]),
    'commutator_closure_pass': payload.get('gell_mann_su3_candidate_checks', {}).get('commutator_closure_pass') is True,
    'no_active_forbidden_code_patterns': not bool(code_hits),
    'no_active_forbidden_numeric_mass_tokens': not bool(num_hits),
    'no_nested_archives': not bool(nested_archives),
}
issues = []
for k, ok in checks.items():
    if not ok:
        issues.append({k: False})
if code_hits:
    issues.append({'code_hits': code_hits})
if num_hits:
    issues.append({'numeric_mass_token_hits': num_hits})
if nested_archives:
    issues.append({'nested_archives': nested_archives})

status = 'PASS' if not issues else 'FAIL'
out = {
    'schema': 'METATIME_SM_MODULE39_VALIDATION_V3_9',
    'status': status,
    'scope': 'active module v3.9 plus repo no-nested-archive check',
    'checks': checks,
    'issues': issues,
    'doctor_verdict': 'CONTINUE_RESEARCH__MODULE39_TETRA_TRIPLET_SU3_LIFT_PASS__QCD_NOT_CLOSED' if status == 'PASS' else 'STOP_CRITICAL',
}
(ROOT/'results'/'VALIDATION_MODULE39_v3_9.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
