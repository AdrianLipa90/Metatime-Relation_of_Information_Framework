#!/usr/bin/env python3
"""
Module 59 / v5.9: Prime-product sigma/R(n) + triplet W_ij hadron-scale candidate freeze.

Purpose:
- Continue from v5.8 without rejecting exact hadron tables merely because errors are small.
- Build a clean dimensionless hadron-scale carrier from non-mass structural inputs.
- Do NOT benchmark baryon MeV values in this module.
- Do NOT claim Debt 9 closure.

Inputs allowed:
- quark prime assignments used in the document path,
- sigma(n)/R(n),
- harmonic correction L(n),
- tetrahedral triplet topology,
- W_ij holonomic pair links,
- OIB = ln2/(24*pi),
- Ramanujan/OI small normalizer,
- confinement residual budget as diagnostic boundary.
"""
import json, math, hashlib, csv
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parents[1]
RESULTS = MODULE_DIR / 'results'
RESULTS.mkdir(exist_ok=True)

OIB = math.log(2) / (24 * math.pi)
L3 = 7
DELTA_CONFINEMENT_BUDGET = 0.21

# Prime assignments follow the clean structural route mentioned in v5.8:
# proton u,u,d -> 3*3*5 = 45.
QUARK_PRIME = {'u': 3, 'd': 5, 's': 7, 'c': 11, 'b': 13, 't': 17}

# Candidate hadron set is deliberately structural; no masses appear here.
HADRONS = {
    'proton':  ['u','u','d'],
    'neutron': ['u','d','d'],
    'lambda':  ['u','d','s'],
    'sigma_plus': ['u','u','s'],
    'sigma_zero': ['u','d','s'],
    'xi_zero': ['u','s','s'],
    'omega_minus': ['s','s','s'],
    'pion_plus': ['u','dbar'],
    'kaon_plus': ['u','sbar'],
}

# Antiquarks use same prime magnitude but get a signed orientation tag in W_ij.
def qbase(q):
    return q[:-3] if q.endswith('bar') else q

def qsign(q):
    return -1 if q.endswith('bar') else 1

def factorint(n):
    out={}
    d=2
    while d*d<=n:
        while n%d==0:
            out[d]=out.get(d,0)+1
            n//=d
        d+=1
    if n>1: out[n]=out.get(n,0)+1
    return out

def sigma(n):
    f=factorint(n)
    prod=1
    for p,a in f.items():
        prod *= (p**(a+1)-1)//(p-1)
    return prod

def hadron_n(comp):
    n=1
    for q in comp:
        n *= QUARK_PRIME[qbase(q)]
    return n

def harmonic_L(comp):
    # Harmonic correction from prime reciprocals, normalized by triplet clock L3.
    # This is intentionally dimensionless.
    return L3 * sum(1.0/QUARK_PRIME[qbase(q)] for q in comp) / len(comp)

def pair_edges(comp):
    return [(comp[i], comp[j]) for i in range(len(comp)) for j in range(i+1, len(comp))]

def wij_pair(qi,qj):
    # Candidate holonomic pair suppression/release from log-prime separation and orientation.
    # Same-orientation quark pairs get a small diffusive suppression.
    # quark-antiquark links get an orientation release term but remain dimensionless.
    pi=QUARK_PRIME[qbase(qi)]; pj=QUARK_PRIME[qbase(qj)]
    orient = qsign(qi)*qsign(qj)
    diff=(math.log(pi)-math.log(pj))**2
    base=math.exp(-OIB * L3 * diff)
    if orient < 0:
        # mesonic open link: orientation boundary, not a mass fit.
        return base * math.exp(OIB * L3)
    return base

def w_triplet(comp):
    edges=pair_edges(comp)
    if not edges: return 1.0
    prod=1.0
    for a,b in edges:
        prod*=wij_pair(a,b)
    return prod ** (1.0/len(edges))

def ramanujan_oi_residue(n, comp):
    # Non-mass small normalizer: divisor abundance relative to log clock.
    # Chosen as a frozen candidate formula, not benchmarked in this module.
    R=sigma(n)/n
    return math.exp(OIB * (math.log1p(R) + harmonic_L(comp)/L3))

def tetrahedral_factor(comp):
    # Baryon triplets are structurally complete; mesons are boundary/open paths.
    if len(comp)==3:
        unique=len({qbase(q) for q in comp})
        # small C3 degeneracy trace, bounded by OIB.
        return math.exp(OIB * (3-unique)/3)
    if len(comp)==2:
        return math.exp(-OIB/2)
    return 1.0

# Structural base: proton composition n=45, not proton mass.
BASE_COMP=HADRONS['proton']
BASE_N=hadron_n(BASE_COMP)
BASE_R=sigma(BASE_N)/BASE_N
BASE_H=harmonic_L(BASE_COMP)
BASE_W=w_triplet(BASE_COMP)
BASE_RAM=ramanujan_oi_residue(BASE_N, BASE_COMP)
BASE_TET=tetrahedral_factor(BASE_COMP)
BASE_SCORE=BASE_R*BASE_H*BASE_W*BASE_RAM*BASE_TET

rows=[]
for name,comp in HADRONS.items():
    n=hadron_n(comp)
    sig=sigma(n)
    R=sig/n
    H=harmonic_L(comp)
    W=w_triplet(comp)
    Ram=ramanujan_oi_residue(n, comp)
    Tet=tetrahedral_factor(comp)
    raw=R*H*W*Ram*Tet
    rel=raw/BASE_SCORE
    rows.append({
        'hadron':name,
        'composition':' '.join(comp),
        'n_prime_product':n,
        'sigma_n':sig,
        'R_sigma_over_n':R,
        'harmonic_L':H,
        'W_geometric_link':W,
        'ramanujan_oi_residue':Ram,
        'tetrahedral_or_boundary_factor':Tet,
        'dimensionless_raw_score':raw,
        'dimensionless_score_relative_to_proton_structural_base':rel,
        'state_class':'baryon_triplet' if len(comp)==3 else 'meson_open_path',
        'mev_prediction_claimed':False,
        'benchmark_used':False,
    })

stable_payload={
    'formula':'score = (sigma(n)/n) * L_harmonic(comp) * W_geom(comp) * RamanujanOI(n,comp) * TetraBoundary(comp); normalized to proton structural n=45 base only as dimensionless base carrier',
    'constants': {'OIB':OIB, 'L3':L3, 'delta_confinement_budget':DELTA_CONFINEMENT_BUDGET},
    'quark_prime':QUARK_PRIME,
    'hadrons':HADRONS,
    'rows':rows,
    'no_mass_inputs': True,
    'no_benchmark_in_module': True,
}
formula_hash=hashlib.sha256(json.dumps(stable_payload, sort_keys=True).encode()).hexdigest()

result={
    'schema':'METATIME_DEBT9_PRIME_PRODUCT_HADRON_SCALE_CANDIDATE_V5_9',
    'module':'59_debt9_prime_product_hadron_scale_candidate_v5_9',
    'created_utc':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'technical_status':'PASS',
    'formal_status':'PASS_FROZEN_DIMENSIONLESS_CANDIDATE_WITH_NO_BENCHMARK',
    'substantive_status':'STRUCTURAL_HADRON_SCALE_CARRIER_FROZEN_ABSOLUTE_MEV_SCALE_NOT_DERIVED',
    'debt9_numeric_spectrum':'OPEN_NOT_CLOSED',
    'canon_allowed':False,
    'current_promotion':'DENY_CURRENT',
    'mass_prediction_claimed':False,
    'benchmark_performed':False,
    'formula_fingerprint_sha256':formula_hash,
    'constants':stable_payload['constants'],
    'quark_prime':QUARK_PRIME,
    'structural_base':{
        'base':'proton structural carrier, composition uud, n=45',
        'base_n':BASE_N,
        'base_sigma':sigma(BASE_N),
        'base_R':BASE_R,
        'base_score':BASE_SCORE,
        'note':'This is a dimensionless structural base, not an input proton mass.'
    },
    'rows':rows,
    'decision':{
        'prime_product_sigma_R_route':'PROMOTED_TO_FROZEN_DIMENSIONLESS_CANDIDATE',
        'absolute_hadron_MeV_scale':'NOT_DERIVED_IN_V5_9',
        'exact_hadron_tables':'REMAIN_PROVENANCE_REQUIRED_SCORING_ONLY',
        'next_step':'v6.0 may perform a sealed ratio benchmark or derive an absolute MeV normalizer before benchmarking.'
    },
    'guardrails':{
        'pdg_or_hadron_mass_inputs_used':False,
        'NoParamSM_used':False,
        'exact_table_replay_used':False,
        'mass_benchmark_used_in_formula':False,
        'nested_archives_allowed':False,
    },
    'blockers':[
        'No absolute MeV normalizer from non-mass constants yet.',
        'Dimensionless hadron ratios not benchmarked in this module.',
        'Debt 9 remains open.'
    ]
}

(RESULTS/'prime_product_hadron_scale_candidate_v5_9.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
with (RESULTS/'prime_product_hadron_scale_candidate_v5_9.csv').open('w', newline='', encoding='utf-8') as f:
    fields=list(rows[0].keys())
    w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

print(json.dumps({'status':'PASS','formula_hash':formula_hash,'rows':len(rows)}, indent=2))
