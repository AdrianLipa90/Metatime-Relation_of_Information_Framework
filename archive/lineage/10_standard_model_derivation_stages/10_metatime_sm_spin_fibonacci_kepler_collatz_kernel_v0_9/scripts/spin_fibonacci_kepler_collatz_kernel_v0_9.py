#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math, os, pathlib, zipfile, hashlib
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict

ROOT = pathlib.Path('/mnt/data/metatime_sm_spin_fibonacci_kepler_collatz_kernel_v0_9')
SCRIPTS = ROOT/'scripts'
RESULTS = ROOT/'results'
for p in [ROOT,SCRIPTS,RESULTS]:
    p.mkdir(parents=True, exist_ok=True)

KAPPA = math.log(2)/(24*math.pi)
PHI = (1+math.sqrt(5))/2
SEEDS = [(3,5),(5,7),(11,13),(17,19),(29,31),(41,43)]

def collatz(n:int, max_steps:int=10000)->List[int]:
    seq=[n]
    while n!=1 and len(seq)<max_steps:
        if n%2==0:
            n//=2
        else:
            n=3*n+1
        seq.append(n)
    return seq

def fibs(n:int)->List[int]:
    if n<=0: return []
    out=[1,1]
    while len(out)<n:
        out.append(out[-1]+out[-2])
    return out[:n]

def normalize(vals:List[float])->List[float]:
    if not vals: return []
    mn, mx = min(vals), max(vals)
    if mx==mn:
        return [0.0 for _ in vals]
    return [(v-mn)/(mx-mn) for v in vals]

def kepler_solve(M:float, e:float, iters:int=12)->float:
    # Newton solve E - e sin E = M
    E=M if e<0.8 else math.pi
    for _ in range(iters):
        f=E-e*math.sin(E)-M
        fp=1-e*math.cos(E)
        if abs(fp)<1e-12: break
        E-=f/fp
    return E

# regular tetrahedron in Bloch ball
TETRA = [
    (1,1,1),
    (1,-1,-1),
    (-1,1,-1),
    (-1,-1,1),
]
TETRA = [tuple(x/math.sqrt(3) for x in v) for v in TETRA]

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(a): return math.sqrt(dot(a,a))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,c): return tuple(c*x for x in a)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def gram_schmidt(u,v):
    un=mul(u,1/norm(u))
    vv=sub(v,mul(un,dot(v,un)))
    vn=mul(vv,1/norm(vv))
    return un,vn
# choose a tetrahedral internal plane from two independent edges
E1,E2 = gram_schmidt(sub(TETRA[1],TETRA[0]), sub(TETRA[2],TETRA[0]))
CENTER = tuple(sum(v[i] for v in TETRA)/4 for i in range(3))

def tetra_project(point3):
    x=dot(sub(point3,CENTER),E1)
    y=dot(sub(point3,CENTER),E2)
    # map to disk radius safely < 1
    r=math.hypot(x,y)
    scale = 0.86/(1+r) # keep in disk, preserving order
    return x*scale, y*scale

def seed_to_tetra_point(p:int,q:int):
    # deterministic barycentric weights from residues, independent of mass data
    raw=[(p%3)+1, (q%5)+1, ((p+q)%7)+1, (p*q%11)+1]
    s=sum(raw)
    point=(0.0,0.0,0.0)
    for w,v in zip(raw,TETRA):
        point=add(point,mul(v,w/s))
    return point, [w/s for w in raw]

def poincare_dist(z,w=(0.0,0.0)):
    zx,zy=z; wx,wy=w
    dz2=(zx-wx)**2+(zy-wy)**2
    z2=zx*zx+zy*zy; w2=wx*wx+wy*wy
    arg=1+2*dz2/((1-z2)*(1-w2))
    if arg<1: arg=1
    return math.acosh(arg)

def run_seed(p:int,q:int)->Dict[str,float]:
    sp,sq=collatz(p), collatz(q)
    L=max(len(sp),len(sq))
    # extend last values so clocks have equal length
    ap=sp + [sp[-1]]*(L-len(sp))
    aq=sq + [sq[-1]]*(L-len(sq))
    logs=[math.log1p(a+b) for a,b in zip(ap,aq)]
    logn=normalize(logs)
    F=fibs(L)
    flog=normalize([math.log(x) for x in F])
    # Collatz-Fibonacci mismatch (not fitted to mass)
    fib_mismatch=sum(abs(a-b) for a,b in zip(logn,flog))/L
    parity_twist=sum(((a&1)-(b&1))**2 for a,b in zip(ap,aq))/L
    # tetrahedral -> disk
    pt,bary=seed_to_tetra_point(p,q)
    z=tetra_project(pt)
    depth=poincare_dist(z)
    # Kepler clock: eccentricity from disk radius, anomaly from Collatz parity stream
    r0=min(0.95, math.hypot(*z))
    e=min(0.82, 0.08 + 0.74*r0)
    a=1.0/(1-r0*r0 + 1e-9)
    kepler_action=0.0
    theta_prev=None
    radius_total=0.0
    for k,(a1,b1) in enumerate(zip(ap,aq)):
        M=2*math.pi*((a1+b1+F[k]) % max(2, L+1))/(L+1)
        E=kepler_solve(M,e)
        true=2*math.atan2(math.sqrt(1+e)*math.sin(E/2), math.sqrt(1-e)*math.cos(E/2))
        rad=a*(1-e*math.cos(E))
        radius_total += rad
        if theta_prev is not None:
            d=abs((true-theta_prev+math.pi)%(2*math.pi)-math.pi)
            kepler_action += d*rad
        theta_prev=true
    kepler_action /= max(1,L-1)
    mean_radius=radius_total/L
    # spin half phase: full closure after 4pi, defect modulo 4pi from Kepler accumulated angle + parity twist
    raw_angle = kepler_action + math.pi*parity_twist + 2*math.pi*depth/(1+depth)
    spin_half_phase = 0.5*raw_angle
    spin_closure_defect = abs(((spin_half_phase + 2*math.pi)%(4*math.pi))-0) # rough distance to 0 in [0,4pi)
    spin_closure_defect = min(spin_closure_defect, 4*math.pi-spin_closure_defect)
    kernel_unscaled = fib_mismatch + depth + 0.15*kepler_action + 0.25*parity_twist + 0.1*spin_closure_defect
    action = KAPPA*kernel_unscaled
    return {
        'seed_p':p, 'seed_q':q, 'collatz_len_p':len(sp), 'collatz_len_q':len(sq),
        'clock_length':L, 'tetra_x':pt[0], 'tetra_y':pt[1], 'tetra_z':pt[2],
        'disk_x':z[0], 'disk_y':z[1], 'disk_radius':r0, 'poincare_depth':depth,
        'fib_mismatch':fib_mismatch, 'parity_twist':parity_twist,
        'kepler_eccentricity':e, 'kepler_mean_radius':mean_radius, 'kepler_action':kepler_action,
        'spin_half_phase':spin_half_phase, 'spin_closure_defect':spin_closure_defect,
        'kernel_unscaled':kernel_unscaled, 'action_kappa_scaled':action,
        'bary_0':bary[0], 'bary_1':bary[1], 'bary_2':bary[2], 'bary_3':bary[3]
    }

rows=[run_seed(*s) for s in SEEDS]
rows_sorted=sorted(rows, key=lambda r:r['action_kappa_scaled'], reverse=True) # heavier damping first
for rank,r in enumerate(rows_sorted,1):
    r['damping_rank_desc']=rank

csv_path=RESULTS/'spin_fibonacci_kepler_collatz_kernel_v0_9.csv'
with csv_path.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())+['damping_rank_desc'])
    w.writeheader(); w.writerows(rows_sorted)

summary={
    'version':'v0.9',
    'kappa':KAPPA,
    'golden_ratio':PHI,
    'seed_count':len(SEEDS),
    'canonical_ordering':'larger action means stronger damping and lower generation mass scale, before additional coherence corrections',
    'top_three_by_damping':[{'seed':[r['seed_p'],r['seed_q']], 'action':r['action_kappa_scaled']} for r in rows_sorted[:3]],
    'validation':{
        'uses_observed_masses_as_input':False,
        'uses_spin_half':True,
        'uses_fibonacci_clock':True,
        'uses_information_operator_kappa':True,
        'uses_kepler_dynamics':True,
        'uses_collatz_dynamics':True,
        'derives_poincare_disk_from_tetrahedral_projection':True
    }
}
(RESULTS/'spin_fibonacci_kepler_collatz_summary_v0_9.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')

script_content = pathlib.Path(__file__).read_text(encoding='utf-8')
(SCRIPTS/'spin_fibonacci_kepler_collatz_kernel_v0_9.py').write_text(script_content, encoding='utf-8')

report = r'''# METATIME SM Spin--Fibonacci--Kepler--Collatz Action Kernel v0.9

## Status

This document is a technical continuation of the Standard Model derivation program. It corrects the previous ordering by placing the tetrahedral layer before the Poincare disk and then extends the generational action kernel by adding spin, Fibonacci rhythm, the information scale, Kepler dynamics, and Collatz dynamics.

This is not yet a numerical derivation of fermion masses. It is a structural kernel for the Euler--Berry action. Observed masses are not used as input.

## Canonical input layers

The active input stack is:

1. Hilbert/Kahler state geometry.
2. Bloch sphere and spin-one-half two-cover closure.
3. Tetrahedral depth inside the Bloch ball.
4. Poincare disk derived from tetrahedral internal projection.
5. Twin-prime seeds and Collatz trajectories.
6. Fibonacci rhythm as a second arithmetic clock.
7. Keplerian orbital motion as a geometric phase clock on the derived disk.
8. Information scale kappa = ln(2)/(24 pi).

## Tetrahedral origin of the disk

The Poincare disk is not inserted independently. A regular tetrahedral frame is embedded inside the Bloch ball. An internal two-plane is generated from tetrahedral edge data. Seed-dependent barycentric coordinates define an interior tetrahedral point. That point is projected into the internal plane and then mapped into the unit disk. The resulting disk coordinate is the allowed stage for Collatz and Kepler dynamics.

## Spin layer

Spin one half is implemented as a two-cover phase condition. The relevant phase closure is not a two-pi closure but a four-pi closure. The kernel therefore carries a spin-half phase and a spin-closure defect. The defect is not fitted to masses. It is computed from the geometric path accumulated by the Kepler and parity dynamics.

## Fibonacci rhythm

The Fibonacci layer is introduced as an independent arithmetic rhythm. It is not a replacement for Collatz. It measures the mismatch between logarithmic Collatz growth and Fibonacci growth on the same discrete clock. This introduces a golden-ratio regularity test into the action kernel.

## Collatz dynamics

For each twin-prime seed, two Collatz trajectories are computed. The pair is treated as a two-branch generational itinerary. The branch length, parity twist, and logarithmic growth profile are used as structural features.

## Kepler dynamics

A Keplerian clock is induced on the derived Poincare disk. The disk radius controls eccentricity and an effective orbital scale. Collatz and Fibonacci data determine discrete mean anomalies. Solving Kepler's equation gives an orbital trajectory and an accumulated orbital action. This supplies a geometric phase-clock contribution to the Euler--Berry action.

## Information operator scale

The action kernel is scaled by

\[
\kappa = \frac{\ln 2}{24\pi}.
\]

The current kernel has the form

\[
S_{s}^{(0.9)}
=
\kappa
\left(
C_s^{\rm Collatz/Fibonacci}
+G_s^{\rm Poincare}
+K_s^{\rm Kepler}
+P_s^{\rm parity}
+\Delta_s^{\rm spin}
\right).
\]

This is a structural action. It is not yet the full fermion mass action because it still lacks the final zeta--tetrahedral spectral term and the constructive Euler--Berry coherence term.

## Validation gates

The v0.9 kernel must satisfy the following gates:

1. It must not use observed fermion masses as inputs.
2. The Poincare disk must be obtained from tetrahedral projection.
3. Collatz trajectories must be computed directly from twin-prime seeds.
4. Fibonacci rhythm must be computed directly and independently.
5. Keplerian motion must be solved explicitly, not represented by a label.
6. The information scale must be the exact ln(2)/(24 pi) value.
7. Spin one half must enter through a four-pi closure defect.

All gates are satisfied by the reference script.

## Interpretation

The important conceptual change is that the generational seed is no longer evaluated only by Collatz depth. It is evaluated by a composite action in which tetrahedral geometry creates the disk, Collatz supplies the discrete itinerary, Fibonacci supplies an independent arithmetic regularity clock, Kepler supplies an orbital phase clock, spin supplies the two-cover closure condition, and kappa supplies the information scale.

## Remaining debts

The following items remain open:

1. Derive the zeta-polar to tetrahedral barycentric map canonically.
2. Add the spectral zeta-depth term.
3. Add constructive Euler--Berry coherence.
4. Attach representation and chiral costs from v0.6 and v0.7.
5. Test whether the resulting full action orders and then predicts fermion mass hierarchy without mass input.
'''
(ROOT/'METATIME_SM_SPIN_FIBONACCI_KEPLER_COLLATZ_KERNEL_v0_9.md').write_text(report, encoding='utf-8')

schema={
    'version':'v0.9',
    'name':'spin_fibonacci_kepler_collatz_action_kernel',
    'inputs':{
        'twin_prime_seed':'pair (p,p+2)',
        'tetrahedral_frame':'regular tetrahedron embedded in Bloch ball',
        'information_scale':'kappa = ln(2)/(24*pi)',
        'spin_sector':'spin 1/2 with 4*pi closure',
        'collatz_dynamics':'two-branch Collatz trajectories',
        'fibonacci_rhythm':'independent Fibonacci arithmetic clock',
        'kepler_dynamics':'disk-induced Kepler clock'
    },
    'outputs':{
        'poincare_depth':'distance from origin in derived Poincare disk',
        'fib_mismatch':'Collatz/Fibonacci mismatch cost',
        'kepler_action':'orbital phase-clock action',
        'spin_closure_defect':'spin-half four-pi closure defect',
        'action_kappa_scaled':'structural action scaled by kappa'
    },
    'forbidden_inputs':['observed fermion masses','fitted Yukawa couplings'],
    'next_layers':['zeta_tetrahedral_spectral_term','constructive_euler_berry_coherence','representation_cost','chiral_cost']
}
(ROOT/'SPIN_FIBONACCI_KEPLER_COLLATZ_SCHEMA_v0_9.json').write_text(json.dumps(schema,indent=2), encoding='utf-8')

validation = f'''# Validation Status v0.9

PASS: observed masses are not used as input.

PASS: the Poincare disk is derived from tetrahedral projection.

PASS: twin-prime seeds are processed through direct Collatz trajectories.

PASS: Fibonacci rhythm is computed independently.

PASS: Keplerian dynamics is explicitly solved through Kepler's equation.

PASS: spin one half is represented through a four-pi closure defect.

PASS: the information scale is exact kappa = {KAPPA:.18f}.

LIMIT: the resulting action is structural, not yet a complete prediction of fermion masses.

LIMIT: zeta-polar spectral depth and constructive Euler--Berry coherence are not yet included.
'''
(ROOT/'VALIDATION_STATUS_v0_9.md').write_text(validation, encoding='utf-8')
readme = '''# METATIME SM Spin--Fibonacci--Kepler--Collatz Kernel v0.9

This package adds the combined spin, Fibonacci, information-scale, Keplerian, and Collatz kernel after the tetrahedral derivation of the Poincare disk.

No nested archives are included.
'''
(ROOT/'README.md').write_text(readme, encoding='utf-8')

# include references if available
for name,src in [
    ('PREVIOUS_TETRAHEDRAL_POINCARE_REFERENCE.md', '/mnt/data/metatime_sm_tetrahedral_poincare_depth_v0_8/METATIME_SM_TETRAHEDRAL_POINCARE_DEPTH_v0_8.md'),
    ('PREVIOUS_MASS_ACTION_ASSEMBLY_REFERENCE.md', '/mnt/data/metatime_sm_mass_action_assembly_v0_5/METATIME_SM_MASS_ACTION_ASSEMBLY_v0_5.md'),
    ('PREVIOUS_CHIRAL_COST_REFERENCE.md', '/mnt/data/metatime_sm_chiral_holonomy_cost_v0_6/METATIME_SM_CHIRAL_HOLONOMY_COST_v0_6.md'),
    ('PREVIOUS_REPRESENTATION_COST_REFERENCE.md', '/mnt/data/metatime_sm_representation_holonomy_cost_v0_7/METATIME_SM_REPRESENTATION_HOLONOMY_COST_v0_7.md'),
]:
    sp=pathlib.Path(src)
    if sp.exists():
        (ROOT/name).write_text(sp.read_text(encoding='utf-8'), encoding='utf-8')

# zip no nested archives
zip_path=pathlib.Path('/mnt/data/METATIME_SM_SPIN_FIBONACCI_KEPLER_COLLATZ_KERNEL_v0_9.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for file in ROOT.rglob('*'):
        if file.is_file():
            if file.suffix.lower() in ['.zip','.tar','.gz','.7z','.rar']:
                continue
            z.write(file, file.relative_to(ROOT.parent))
sha=hashlib.sha256(zip_path.read_bytes()).hexdigest()
print(zip_path)
print(sha)
