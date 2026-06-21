#!/usr/bin/env python3
"""
METATIME / Standard Model Derivation
Tetrahedral -> Poincare Depth Kernel v0.8

This script derives the Poincare disk layer from a tetrahedral depth frame.
It does not use observed fermion masses as input.
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from typing import List, Tuple, Dict, Any

OUT = Path(__file__).resolve().parents[1] / 'results'
OUT.mkdir(parents=True, exist_ok=True)

SQRT2 = math.sqrt(2.0)
SQRT6 = math.sqrt(6.0)

# Canonical regular tetrahedron in the Bloch ball with one polar apex.
VERTICES = [
    (0.0, 0.0, 1.0),
    (2.0 * SQRT2 / 3.0, 0.0, -1.0 / 3.0),
    (-SQRT2 / 3.0, SQRT6 / 3.0, -1.0 / 3.0),
    (-SQRT2 / 3.0, -SQRT6 / 3.0, -1.0 / 3.0),
]

# Disk basis: the base face plane carries the internal three-direction frame.
BASE_CENTER = tuple(sum(VERTICES[i][j] for i in (1,2,3)) / 3.0 for j in range(3))

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(a): return math.sqrt(dot(a,a))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def mul(s,a): return tuple(s*x for x in a)
def unit(a):
    n=norm(a)
    return tuple(x/n for x in a)

E1 = unit(sub(VERTICES[1], BASE_CENTER))
_temp = sub(VERTICES[2], BASE_CENTER)
E2 = unit(sub(_temp, mul(dot(_temp, E1), E1)))
POLAR = VERTICES[0]

def gram_matrix(vertices):
    return [[dot(a,b) for b in vertices] for a in vertices]

def collatz_orbit(n: int, steps: int = 96) -> List[int]:
    out = [int(n)]
    x = int(n)
    for _ in range(steps-1):
        if x % 2 == 0:
            x //= 2
        else:
            x = 3*x + 1
        out.append(x)
    return out

def barycentric_weights_from_pair(a: int, b: int, k: int) -> List[float]:
    """Candidate non-mass mapping from a paired Collatz step to tetrahedral weights.

    Apex/polar weight responds to parity disagreement and branch asymmetry.
    Base weights are driven by residues modulo 3, representing the three
    tetrahedral internal directions. All weights are positive.
    """
    parity_disagreement = abs((a % 2) - (b % 2))
    log_asym = abs(math.log1p(a) - math.log1p(b)) / max(1e-12, (math.log1p(a)+math.log1p(b))/2.0)
    w0 = 1.0 + parity_disagreement + 0.5 * math.tanh(log_asym)
    base = [1.0, 1.0, 1.0]
    for r in (a % 3, b % 3, (a + b + k) % 3):
        base[r] += 1.0
    # Small deterministic phase-like cyclic drive, independent of mass targets.
    base[k % 3] += 0.25
    return [w0] + base

def tetra_point(weights: List[float]) -> Tuple[float,float,float]:
    total = sum(weights)
    x = (0.0,0.0,0.0)
    for w,v in zip(weights, VERTICES):
        x = add(x, mul(w/total, v))
    # Numerical safety: keep strict interior for Poincare conversion.
    r = norm(x)
    if r >= 1.0:
        x = mul((1.0 - 1e-9)/r, x)
    return x

def klein_ball_to_poincare_ball(x: Tuple[float,float,float]) -> Tuple[float,float,float]:
    r2 = min(1.0 - 1e-15, dot(x,x))
    denom = 1.0 + math.sqrt(1.0 - r2)
    return tuple(v/denom for v in x)

def project_to_disk(y: Tuple[float,float,float]) -> Tuple[float,float]:
    return (dot(y,E1), dot(y,E2))

def disk_radius(z): return math.sqrt(z[0]*z[0] + z[1]*z[1])

def hyp_dist(u, v):
    ru2 = min(1-1e-15, u[0]*u[0]+u[1]*u[1])
    rv2 = min(1-1e-15, v[0]*v[0]+v[1]*v[1])
    duv2 = (u[0]-v[0])**2 + (u[1]-v[1])**2
    arg = 1.0 + 2.0*duv2/((1.0-ru2)*(1.0-rv2))
    return math.acosh(max(1.0, arg))

def angle_between(a,b,c):
    # Euclidean turning angle at b in disk coordinates.
    ba = (a[0]-b[0], a[1]-b[1])
    bc = (c[0]-b[0], c[1]-b[1])
    nba = math.hypot(*ba); nbc = math.hypot(*bc)
    if nba < 1e-12 or nbc < 1e-12:
        return 0.0
    cosv = max(-1.0, min(1.0, (ba[0]*bc[0]+ba[1]*bc[1])/(nba*nbc)))
    return math.acos(cosv)

def entropy(weights):
    s=sum(weights)
    ps=[w/s for w in weights]
    return -sum(p*math.log(p) for p in ps if p>0)

def seed_metrics(seed: Tuple[int,int], steps: int = 96) -> Dict[str, Any]:
    a_orb = collatz_orbit(seed[0], steps)
    b_orb = collatz_orbit(seed[1], steps)
    points=[]; ent=[]; polar=[]; base_balance=[]
    for k,(a,b) in enumerate(zip(a_orb,b_orb)):
        w = barycentric_weights_from_pair(a,b,k)
        x = tetra_point(w)
        y = klein_ball_to_poincare_ball(x)
        z = project_to_disk(y)
        points.append(z)
        ent.append(entropy(w))
        polar.append(w[0]/sum(w))
        base = w[1:]
        m=sum(base)/3.0
        base_balance.append(math.sqrt(sum((bb-m)**2 for bb in base)/3.0)/max(1e-12,m))
    path = sum(hyp_dist(points[i], points[i+1]) for i in range(len(points)-1))
    mean_radius = sum(disk_radius(z) for z in points)/len(points)
    max_radius = max(disk_radius(z) for z in points)
    turn = sum(angle_between(points[i-1], points[i], points[i+1]) for i in range(1,len(points)-1))
    closure = hyp_dist(points[-1], points[-4]) if len(points)>4 else 0.0
    mean_entropy = sum(ent)/len(ent)
    mean_polar = sum(polar)/len(polar)
    mean_base_balance = sum(base_balance)/len(base_balance)
    # Candidate action: purely geometric/tetrahedral, not fitted to masses.
    action = (path/steps) + 0.75*mean_radius + 0.25*(turn/steps) + 0.5*closure + 0.35*mean_base_balance - 0.20*mean_entropy
    return {
        'seed_p': seed[0], 'seed_q': seed[1], 'steps': steps,
        'poincare_path_per_step': path/steps,
        'mean_disk_radius': mean_radius,
        'max_disk_radius': max_radius,
        'turning_per_step': turn/steps,
        'cycle_closure_distance': closure,
        'mean_tetra_entropy': mean_entropy,
        'mean_polar_weight': mean_polar,
        'mean_base_balance': mean_base_balance,
        'tetra_poincare_action_v0_8': action,
    }

def main():
    candidates = [(3,5),(5,7),(11,13),(17,19),(29,31),(41,43),(59,61),(71,73)]
    rows = [seed_metrics(s) for s in candidates]
    rows_sorted = sorted(rows, key=lambda r: r['tetra_poincare_action_v0_8'])
    for rank,r in enumerate(rows_sorted, start=1):
        r['action_rank_low_to_high'] = rank
    # restore original sort by rank for output
    rows = rows_sorted
    csv_path = OUT/'tetra_poincare_depth_table_v0_8.csv'
    with csv_path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    summary = {
        'status': 'candidate_kernel_not_mass_prediction',
        'non_fitting_rule': 'observed fermion masses are not used',
        'tetrahedron_vertices': VERTICES,
        'gram_matrix': gram_matrix(VERTICES),
        'disk_basis': {'E1': E1, 'E2': E2, 'polar': POLAR},
        'candidate_count': len(candidates),
        'best_seed_by_tetra_poincare_action': [rows[0]['seed_p'], rows[0]['seed_q']],
        'minimal_triplet_rank_order': [[r['seed_p'], r['seed_q'], r['action_rank_low_to_high']] for r in rows if (r['seed_p'],r['seed_q']) in [(3,5),(5,7),(11,13)]],
        'output_table': str(csv_path),
    }
    (OUT/'tetra_poincare_depth_summary_v0_8.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    # Simple SVG plot without external deps
    svg = []
    W=600; H=600; cx=300; cy=300; scale=260
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{scale}" fill="none" stroke="black" stroke-width="2"/>')
    colors=['#111','#444','#777','#999','#bbb','#555','#333','#888']
    for idx,seed in enumerate(candidates[:3]):
        a_orb=collatz_orbit(seed[0],64); b_orb=collatz_orbit(seed[1],64)
        pts=[]
        for k,(a,b) in enumerate(zip(a_orb,b_orb)):
            z=project_to_disk(klein_ball_to_poincare_ball(tetra_point(barycentric_weights_from_pair(a,b,k))))
            pts.append((cx+scale*z[0], cy-scale*z[1]))
        d='M '+' L '.join(f'{x:.2f},{y:.2f}' for x,y in pts)
        svg.append(f'<path d="{d}" fill="none" stroke="{colors[idx]}" stroke-width="1.5" opacity="0.85"/>')
        svg.append(f'<text x="20" y="{30+20*idx}" font-size="14" fill="{colors[idx]}">seed {seed[0]}-{seed[1]}</text>')
    svg.append('</svg>')
    (OUT/'tetra_poincare_minimal_triplet_paths_v0_8.svg').write_text('\n'.join(svg), encoding='utf-8')

if __name__ == '__main__':
    main()
