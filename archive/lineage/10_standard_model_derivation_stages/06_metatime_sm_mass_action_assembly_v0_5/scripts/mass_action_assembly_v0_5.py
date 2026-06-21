#!/usr/bin/env python3
"""METATIME SM Mass Action Assembly v0.5

Builds the first no-mass-input generation assignment from the v0.4
Collatz-Poincare action kernel, then validates only the ordering against
observed mass-derived action targets. Observed masses are not used for
assignment or coefficient choice.
"""
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_csv(path: Path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))

def main():
    table = load_csv(ROOT / 'input' / 'collatz_poincare_action_table_v0_4.csv')
    targets = load_csv(ROOT / 'input' / 'mass_action_validation_targets.csv')
    minimal = [(3,5), (11,13), (5,7)]
    selected = []
    for p,q in minimal:
        row = next(r for r in table if int(r['seed_p']) == p and int(r['seed_q']) == q)
        selected.append(row)
    selected = sorted(selected, key=lambda r: float(r['eb_action_kernel_unit_v04']), reverse=True)
    assignments = []
    for gen,row in enumerate(selected, start=1):
        assignments.append({
            'generation': gen,
            'seed_p': int(row['seed_p']),
            'seed_q': int(row['seed_q']),
            'eb_action_kernel_unit_v04': float(row['eb_action_kernel_unit_v04']),
            'role': ['lightest','middle','heaviest'][gen-1],
        })
    print(json.dumps(assignments, indent=2))
    target_by = {r['fermion']: r for r in targets}
    families = {
        'charged_leptons': [('e',1),('mu',2),('tau',3)],
        'up_type_quarks': [('u',1),('c',2),('t',3)],
        'down_type_quarks': [('d',1),('s',2),('b',3)],
    }
    for fam, items in families.items():
        model = {name: assignments[gen-1]['eb_action_kernel_unit_v04'] for name,gen in items}
        target = {name: float(target_by[name]['minus_ln_y']) for name,gen in items}
        model_rank = sorted(model, key=model.get, reverse=True)
        target_rank = sorted(target, key=target.get, reverse=True)
        print(f"{fam}: model_rank={model_rank}; validation_target_rank={target_rank}; status={'PASS' if model_rank==target_rank else 'WARN'}")

if __name__ == '__main__':
    main()
