#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, zipfile
from pathlib import Path
MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]
RESULT = MODULE/'results'/'short_doc_charged_lepton_kernel_freeze_v4_9.json'
FORBIDDEN_EXEC = [
    re.compile(r'from\s+NoParamSM|import\s+NoParamSM|noparamSMsolver\s*\(', re.I),
    re.compile(r'mass_ref\s*=|PDG\s*=\s*\{|reference_spectrum_execution', re.I),
]
errors=[]
if not RESULT.exists(): errors.append('missing result JSON')
else:
    data=json.loads(RESULT.read_text())
    if data.get('technical_status')!='PASS': errors.append('technical status not PASS')
    if data.get('substantive_status')!='FROZEN_SHORT_DOC_KERNEL_NOT_NUMERIC_CLOSURE': errors.append('unexpected substantive status')
    if data.get('canon_allowed') is not False: errors.append('canon_allowed must be false')
    for row in data.get('rows', []):
        if row.get('mass_prediction_claimed') is not False: errors.append(f"mass prediction claimed for {row.get('slot')}")
        if row.get('benchmark_performed') is not False: errors.append(f"benchmark performed for {row.get('slot')}")
        if row.get('pdg_reference_input_used') is not False: errors.append(f"PDG input used for {row.get('slot')}")
        if row.get('observed_mass_input_used') is not False: errors.append(f"observed mass input used for {row.get('slot')}")

# Active executable scan only; reports may mention forbidden source names as taint ledger.
for p in (MODULE/'scripts').glob('*.py'):
    if p.name.startswith('validate_'):
        continue
    text=p.read_text(errors='replace')
    for rx in FORBIDDEN_EXEC:
        if rx.search(text): errors.append(f'forbidden executable pattern in {p.name}: {rx.pattern}')

# No nested archives anywhere in repository.
archive_ext={'.zip','.tar','.gz','.tgz','.bz2','.xz','.7z','.rar'}
for p in ROOT.rglob('*'):
    if p.is_file() and ''.join(p.suffixes[-2:]) in {'.tar.gz','.tar.xz','.tar.bz2'}:
        errors.append(f'nested archive: {p.relative_to(ROOT)}')
    elif p.is_file() and p.suffix.lower() in archive_ext:
        errors.append(f'nested archive: {p.relative_to(ROOT)}')

validation={
    'schema':'VALIDATION_MODULE49_v4_9',
    'status':'PASS' if not errors else 'FAIL',
    'errors':errors,
    'checks':[ 'result JSON exists', 'no benchmark performed', 'no mass prediction claimed', 'active executable PDG/NoParamSM scan', 'nested archive scan' ]
}
out=MODULE/'results'/'VALIDATION_MODULE49_v4_9.json'
out.write_text(json.dumps(validation, indent=2, ensure_ascii=False))
print(json.dumps(validation, indent=2))
if errors: raise SystemExit(1)
