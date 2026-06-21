#!/usr/bin/env python3
"""Reproduce METATIME SM full action seed arbitration v1.0.
This script uses only structural source tables from previous artifacts and does not use observed masses as predictors.
"""
from pathlib import Path
import pandas as pd, math, json
from fractions import Fraction
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
DATA = Path('/mnt/data')
KAPPA = math.log(2)/(24*math.pi)

def load_csv(path):
    return pd.read_csv(path)

v4 = load_csv(DATA/'metatime_sm_mass_action_assembly_v0_5/results/generation_seed_assignment_v0_5.csv')
v8 = load_csv(DATA/'metatime_sm_tetrahedral_poincare_depth_v0_8/results/tetra_poincare_depth_table_v0_8.csv')
v9 = load_csv(DATA/'metatime_sm_spin_fibonacci_kepler_collatz_kernel_v0_9/results/spin_fibonacci_kepler_collatz_kernel_v0_9.csv')

seeds = [(3,5),(5,7),(11,13)]
rows=[]
for p,q in seeds:
    rows.append({
        'seed_p':p,
        'seed_q':q,
        'collatz_poincare_v04':float(v4[(v4.seed_p==p)&(v4.seed_q==q)].eb_action_kernel_unit_v04.iloc[0]),
        'tetra_poincare_v08':float(v8[(v8.seed_p==p)&(v8.seed_q==q)].tetra_poincare_action_v0_8.iloc[0]),
        'spin_fib_kepler_collatz_v09':float(v9[(v9.seed_p==p)&(v9.seed_q==q)].kernel_unscaled.iloc[0]),
    })
seeddf = pd.DataFrame(rows)
for c in ['collatz_poincare_v04','tetra_poincare_v08','spin_fib_kepler_collatz_v09']:
    seeddf[c+'_norm']=(seeddf[c]-seeddf[c].min())/(seeddf[c].max()-seeddf[c].min())
seeddf['integrated_damping_unit_v10']=seeddf[[c+'_norm' for c in ['collatz_poincare_v04','tetra_poincare_v08','spin_fib_kepler_collatz_v09']]].mean(axis=1)
seeddf['integrated_action_kappa_v10']=seeddf['integrated_damping_unit_v10']*KAPPA
seeddf=seeddf.sort_values('integrated_damping_unit_v10', ascending=False).reset_index(drop=True)
seeddf['assigned_generation_v10']=range(1,len(seeddf)+1)
seeddf.to_csv(ROOT/'results'/'seed_arbitration_v1_0.csv', index=False)
print(seeddf.to_string(index=False))
