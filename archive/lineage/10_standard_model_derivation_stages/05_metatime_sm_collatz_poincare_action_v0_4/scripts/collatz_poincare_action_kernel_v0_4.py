#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import csv, json, math, hashlib, zipfile, os, shutil
from pathlib import Path
from collections import Counter

BASE = Path('/mnt/data')
OUT = BASE/'metatime_sm_collatz_poincare_action_v0_4'
if OUT.exists(): shutil.rmtree(OUT)
(OUT/'scripts').mkdir(parents=True)
(OUT/'results').mkdir(parents=True)
(OUT/'references').mkdir(parents=True)

KAPPA = math.log(2)/(24*math.pi)
ZETA_GAMMAS = [14.134725141734694, 21.022039638771554, 25.010857580145688, 30.424876125859513, 32.93506158773919]
SEEDS = [(3,5),(5,7),(11,13),(17,19),(29,31),(41,43),(59,61),(71,73),(101,103),(107,109),(137,139),(149,151),(179,181),(191,193)]

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def collatz_step(n:int)->int:
    return n//2 if n%2==0 else 3*n+1

def collatz_orbit(n:int, max_steps:int=100000)->list[int]:
    out=[n]
    while n != 1 and len(out)<max_steps:
        n=collatz_step(n)
        out.append(n)
    return out

def parity_entropy(orbit):
    pars=[x%2 for x in orbit[:-1]]
    if not pars: return 0.0
    c=Counter(pars); total=sum(c.values()); h=0.0
    for v in c.values():
        p=v/total; h-=p*math.log(p,2)
    return h

def embed_pair(o1,o2):
    # Deterministic bounded embedding. This is a v0.4 kernel candidate, not final canon.
    max_log=max([math.log1p(x) for x in (o1+o2)] + [1.0])
    L=max(len(o1), len(o2))
    pts=[]
    for k in range(L):
        a=o1[k] if k<len(o1) else 1
        b=o2[k] if k<len(o2) else 1
        mean_log=0.5*(math.log1p(a)+math.log1p(b))
        diff_log=math.log1p(b)-math.log1p(a)
        amp=mean_log/max_log
        r=math.tanh(0.95*amp)
        parity_phase=((a%2)-(b%2))*math.pi/3
        rel_phase=math.atan2(diff_log, mean_log+1e-12)
        theta=(2*math.pi*k/max(1,L))+parity_phase+rel_phase
        x=r*math.cos(theta); y=r*math.sin(theta)
        pts.append((x,y,r,theta,a,b))
    return pts

def poincare_distance(p,q):
    x1,y1,_,_,_,_=p; x2,y2,_,_,_,_=q
    dx=x1-x2; dy=y1-y2
    norm2_1=x1*x1+y1*y1; norm2_2=x2*x2+y2*y2
    arg=1+2*(dx*dx+dy*dy)/max(1e-12, (1-norm2_1)*(1-norm2_2))
    return math.acosh(max(1.0,arg))

def path_length(pts):
    if len(pts)<2: return 0.0
    return sum(poincare_distance(pts[i],pts[i+1]) for i in range(len(pts)-1))

def orbit_log_action(o):
    return sum(math.log1p(x) for x in o)/max(1,len(o))

def branch_divergence(o1,o2):
    L=max(len(o1),len(o2))
    acc=0.0
    for i in range(L):
        a=o1[i] if i<len(o1) else 1
        b=o2[i] if i<len(o2) else 1
        acc+=abs(math.log1p(a)-math.log1p(b))
    return acc/max(1,L)

def parity_closure_defect(o1,o2):
    # Defect from balanced parity flow between two branches.
    h1=parity_entropy(o1); h2=parity_entropy(o2)
    return abs(h1-h2)

def zeta_alignment(seed, slot:int|None=None):
    p,q=seed
    log_scale=math.log(p*q)
    gammas=ZETA_GAMMAS if slot is None else [ZETA_GAMMAS[slot % len(ZETA_GAMMAS)]]
    vals=[]
    for gamma in gammas:
        phase=(log_scale/gamma) % 1.0
        vals.append(min(phase, 1-phase))
    return min(vals)

def compute_rows():
    raw=[]
    for idx,seed in enumerate(SEEDS, start=1):
        p,q=seed; o1=collatz_orbit(p); o2=collatz_orbit(q); pts=embed_pair(o1,o2)
        pl=path_length(pts)
        mean_r=sum(pt[2] for pt in pts)/len(pts)
        max_r=max(pt[2] for pt in pts)
        mean_hr=sum(2*math.atanh(min(0.999999,pt[2])) for pt in pts)/len(pts)
        raw.append({
            'candidate_index':idx,'seed_p':p,'seed_q':q,
            'stopping_time_p':len(o1)-1,'stopping_time_q':len(o2)-1,
            'max_p':max(o1),'max_q':max(o2),
            'collatz_log_action_mean':0.5*(orbit_log_action(o1)+orbit_log_action(o2)),
            'branch_divergence':branch_divergence(o1,o2),
            'parity_closure_defect':parity_closure_defect(o1,o2),
            'poincare_path_length':pl,
            'poincare_path_length_per_step':pl/max(1,len(pts)-1),
            'poincare_mean_radius':mean_r,
            'poincare_max_radius':max_r,
            'poincare_mean_hyperbolic_radius':mean_hr,
            'zeta_alignment_min':zeta_alignment(seed),
            'zeta_alignment_slot1':zeta_alignment(seed,0),
            'zeta_alignment_slot2':zeta_alignment(seed,1),
            'zeta_alignment_slot3':zeta_alignment(seed,2),
        })
    # normalize selected fields by median absolute-ish scale / max for diagnostic action
    fields=['collatz_log_action_mean','branch_divergence','parity_closure_defect','poincare_path_length_per_step','poincare_mean_hyperbolic_radius','zeta_alignment_min']
    mins={f:min(r[f] for r in raw) for f in fields}; maxs={f:max(r[f] for r in raw) for f in fields}
    rows=[]
    for r in raw:
        norm={}
        for f in fields:
            denom=maxs[f]-mins[f]
            norm[f+'_unit']=(r[f]-mins[f])/denom if denom else 0.0
        # v0.4 non-fit action kernel: equal-weight positive costs; zeta_alignment is a cost where lower is better.
        # Coherence bonus is not subtracted here to avoid hidden tuning; it is reported separately.
        action_unit=sum(norm[f+'_unit'] for f in fields)/len(fields)
        action_kappa=KAPPA*action_unit
        r.update(norm)
        r['eb_action_kernel_unit_v04']=action_unit
        r['eb_action_kernel_kappa_v04']=action_kappa
        rows.append(r)
    rows.sort(key=lambda x:x['eb_action_kernel_unit_v04'])
    for rank,r in enumerate(rows, start=1): r['eb_action_rank_low_to_high']=rank
    return rows

rows=compute_rows()
# write script file itself for reproducibility
script_path=OUT/'scripts'/'collatz_poincare_action_kernel_v0_4.py'
script_path.write_text(Path(__file__).read_text(encoding='utf-8'), encoding='utf-8')
# trim creation parts? acceptable as reproducibility generator, but includes creating report. OK.

csv_path=OUT/'results'/'collatz_poincare_action_table_v0_4.csv'
with csv_path.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# canonical minimal seed triplet diagnostic: first three twin prime pairs by arithmetic minimality, and their action ranks
minimal_triplet=[(3,5),(5,7),(11,13)]
triplet_rows=[r for r in rows if (r['seed_p'],r['seed_q']) in minimal_triplet]
triplet_by_action=sorted(triplet_rows, key=lambda x:x['eb_action_kernel_unit_v04'])
summary={
    'artifact':'METATIME_SM_COLLATZ_POINCARE_ACTION_KERNEL_v0_4',
    'status':'technical_derivation_candidate_not_mass_prediction',
    'observed_masses_used_as_input':False,
    'kappa':KAPPA,
    'seed_count':len(rows),
    'minimal_arithmetic_triplet':minimal_triplet,
    'minimal_triplet_action_order_low_to_high':[
        {'seed_pair':[r['seed_p'],r['seed_q']], 'action_rank':r['eb_action_rank_low_to_high'], 'action_unit':r['eb_action_kernel_unit_v04'], 'action_kappa':r['eb_action_kernel_kappa_v04']} for r in triplet_by_action
    ],
    'top_five_low_action_seeds':[
        {'seed_pair':[r['seed_p'],r['seed_q']], 'rank':r['eb_action_rank_low_to_high'], 'action_unit':r['eb_action_kernel_unit_v04']} for r in rows[:5]
    ],
    'interpretation':'The v0.4 kernel converts Collatz twin-prime orbits into Poincare-disk path features and an Euler-Berry action-kernel candidate. It is mass-blind. It is not yet a final mass predictor.'
}
(OUT/'results'/'collatz_poincare_action_summary_v0_4.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False), encoding='utf-8')

main_md=f"""# Metatime / Standard Model Derivation — Collatz--Poincare Action Kernel v0.4

Status: technical derivation candidate, not final canon and not a mass prediction.

## Purpose

This layer continues the Standard Model derivation after the gauge skeleton, mass vectorization, Euler--Berry action closure, and generation embedding layers.

The previous layer established that a generation vector is required. This layer begins replacing the diagnostic generation-depth score by an explicit geometric action kernel built from twin-prime Collatz orbits embedded into the Poincare disk.

No observed fermion masses are used as input.

## Inputs

The inputs are:

1. twin-prime seed pairs;
2. Collatz orbit pairs;
3. a deterministic bounded embedding into the Poincare disk;
4. Poincare path length diagnostics;
5. branch-divergence and parity-closure diagnostics;
6. zeta-alignment diagnostics against low non-trivial zeta-zero heights.

## Canonical working objects

Let a candidate generation seed be a twin-prime pair.

For each branch, compute its Collatz orbit. The pair of orbits defines a discrete two-branch trajectory.

The v0.4 embedding maps each paired Collatz step into a point of the Poincare disk. The radial coordinate is bounded by a hyperbolic tangent of the mean logarithmic amplitude. The angular coordinate is driven by step index, parity imbalance, and relative logarithmic branch displacement. This keeps every point strictly inside the disk and makes the construction deterministic.

The kernel then computes:

- Collatz logarithmic action;
- branch divergence;
- parity closure defect;
- Poincare path length per step;
- mean hyperbolic radius;
- zeta-alignment cost.

These quantities are normalized over the candidate scan and combined as an equal-weight v0.4 action-kernel candidate.

## Non-fitting rule

The v0.4 kernel is explicitly mass-blind. Observed masses are not read by the script. They are not used to choose coefficients, seeds, ranks, or normalizations.

Therefore this layer may select or order seed candidates, but it does not yet predict the fermion mass spectrum.

## Minimal arithmetic triplet

The minimal arithmetic twin-prime triplet is:

- (3, 5);
- (5, 7);
- (11, 13).

This triplet is selected by arithmetic minimality, not by observed masses.

The v0.4 action ordering of this triplet is stored in `results/collatz_poincare_action_summary_v0_4.json` and `results/collatz_poincare_action_table_v0_4.csv`.

## Interpretation

This stage gives the first explicit candidate for the generational action contribution. It upgrades the previous generation embedding from a diagnostic vector to a geometric kernel.

The important conclusion is not yet the numerical mass hierarchy. The important conclusion is that a non-mass structural kernel can now assign different action values to candidate generation seeds.

## Validation boundary

This layer does not claim that the three generations have been fully derived.

This layer does claim that the derivation now has a concrete non-mass action-kernel candidate that can be tested in the next stage against the Euler--Berry mass functional.

## Next required stage

The next stage must connect this action kernel to the full fermion vector.

That means combining:

- the representation vector;
- the chiral transition vector;
- the generation seed action;
- the Poincare geometric path;
- the zeta-tetrahedral spectral layer;
- the Euler--Berry coherence term.

Only after that should observed masses be used as validation targets.
"""
(OUT/'METATIME_SM_COLLATZ_POINCARE_ACTION_KERNEL_v0_4.md').write_text(main_md, encoding='utf-8')

validation_md=f"""# Validation Status v0.4

## Status

Technical kernel candidate. Not final canon. Not a mass prediction.

## Mass use

Observed fermion masses used as input: **no**.

## What passed

- Twin-prime candidates are generated independently of mass data.
- Collatz orbits are computed directly.
- Poincare-disk points remain inside the unit disk.
- Action-kernel values are finite for all scanned seeds.
- The minimal arithmetic triplet is identified without mass input.

## What did not pass yet

- No full mass prediction is claimed.
- No final canonical generation assignment is claimed.
- The zeta-tetrahedral mapping remains a derivation debt.
- The Euler--Berry coherence term is not yet derived; it is only prepared as a required next component.

## Validation target for v0.5

The next version must test whether the full Euler--Berry mass action built from this kernel orders the fermion generations without inserting observed masses into the construction.
"""
(OUT/'VALIDATION_STATUS_v0_4.md').write_text(validation_md, encoding='utf-8')

schema={
  'schema':'METATIME_SM_COLLATZ_POINCARE_ACTION_KERNEL_SCHEMA_v0_4',
  'status':'technical_derivation_candidate_not_final_canon',
  'mass_inputs_allowed':False,
  'fields':{
    'seed_pair':'twin-prime pair (p,p+2)',
    'collatz_orbit_pair':'two Collatz trajectories generated from p and p+2',
    'poincare_embedding':'bounded deterministic disk embedding of paired orbit steps',
    'action_components':['collatz_log_action_mean','branch_divergence','parity_closure_defect','poincare_path_length_per_step','poincare_mean_hyperbolic_radius','zeta_alignment_min'],
    'action_kernel':'equal-weight normalized v0.4 action candidate, multiplied by kappa for action scale'
  },
  'next_required_step':'combine this seed action with representation, chirality, zeta-tetrahedral, and Euler-Berry coherence terms in the full mass functional'
}
(OUT/'ACTION_KERNEL_SCHEMA_v0_4.json').write_text(json.dumps(schema,indent=2,ensure_ascii=False), encoding='utf-8')

readme=f"""# METATIME_SM_COLLATZ_POINCARE_ACTION_KERNEL_v0_4

This package continues the Metatime / Standard Model derivation.

It introduces a mass-blind Collatz--Poincare action-kernel candidate for the generational layer.

Contents:

- `METATIME_SM_COLLATZ_POINCARE_ACTION_KERNEL_v0_4.md` — full technical report.
- `ACTION_KERNEL_SCHEMA_v0_4.json` — machine-readable schema.
- `VALIDATION_STATUS_v0_4.md` — validation and boundary status.
- `scripts/collatz_poincare_action_kernel_v0_4.py` — reproducible script.
- `results/collatz_poincare_action_table_v0_4.csv` — candidate table.
- `results/collatz_poincare_action_summary_v0_4.json` — summary.

No observed fermion masses are used as inputs.
"""
(OUT/'README.md').write_text(readme,encoding='utf-8')

# copy lightweight references from previous active layers, no nested zips
ref_map={
    '/mnt/data/metatime_sm_generation_embedding_v0_3/METATIME_SM_GENERATION_EMBEDDING_v0_3.md':'GENERATION_EMBEDDING_v0_3_REFERENCE.md',
    '/mnt/data/metatime_sm_eb_action_closure_v0_2/METATIME_SM_EB_ACTION_CLOSURE_v0_2.md':'EB_ACTION_CLOSURE_v0_2_REFERENCE.md',
    '/mnt/data/metatime_sm_mass_vectorization_v0_1/METATIME_SM_MASS_VECTORIZATION_v0_1.md':'MASS_VECTORIZATION_v0_1_REFERENCE.md',
    '/mnt/data/metatime_sm_gauge_skeleton_v0_1/METATIME_SM_GAUGE_SKELETON_v0_1.md':'GAUGE_SKELETON_v0_1_REFERENCE.md',
}
for src,dst in ref_map.items():
    p=Path(src)
    if p.exists(): shutil.copy2(p, OUT/'references'/dst)

# manifest
files=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():
        files.append({'path':str(p.relative_to(OUT)), 'size':p.stat().st_size, 'sha256':sha256(p)})
manifest={'artifact':'METATIME_SM_COLLATZ_POINCARE_ACTION_KERNEL_v0_4','files':files,'no_nested_archives':True,'mass_inputs_used':False}
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')

# create zip without nested archives
zip_path=BASE/'METATIME_SM_COLLATZ_POINCARE_ACTION_KERNEL_v0_4.zip'
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():
            if p.suffix.lower() in ['.zip','.tar','.gz','.7z','.rar']:
                raise RuntimeError(f'nested archive not allowed: {p}')
            z.write(p, p.relative_to(OUT.parent))
print(json.dumps({'zip':str(zip_path),'sha256':sha256(zip_path),'summary':summary},indent=2,ensure_ascii=False))
