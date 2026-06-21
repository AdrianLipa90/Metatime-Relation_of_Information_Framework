#!/usr/bin/env python3
import math, json
from pathlib import Path
import pandas as pd
import numpy as np
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results'
OUT.mkdir(exist_ok=True)
KAPPA = math.log(2)/(24*math.pi)
PHI = (1+math.sqrt(5))/2
NZ = 64
STEPS = 64

# Regular tetrahedral frame in the Bloch ball.
V = np.array([
    [0.0,0.0,1.0],
    [2*math.sqrt(2)/3,0.0,-1/3],
    [-math.sqrt(2)/3,math.sqrt(6)/3,-1/3],
    [-math.sqrt(2)/3,-math.sqrt(6)/3,-1/3],
], dtype=float)
base_angles = np.array([0.0, 2*math.pi/3, 4*math.pi/3])

def collatz_next(n:int)->int:
    return n//2 if n%2==0 else 3*n+1

def collatz_orbit(n:int, steps:int=STEPS):
    out=[]
    x=int(n)
    for _ in range(steps):
        out.append(x)
        x=collatz_next(x)
    return out

def circle_dist(a,b):
    d=abs((a-b+math.pi)%(2*math.pi)-math.pi)
    return d

def zeta_zero_table(nz=NZ):
    rows=[]
    g1=float(mp.im(mp.zetazero(1)))
    gN=float(mp.im(mp.zetazero(nz)))
    denom=max(1e-12, math.log(gN/g1))
    for n in range(1,nz+1):
        gamma=float(mp.im(mp.zetazero(n)))
        theta=(gamma % (2*math.pi))
        r=math.tanh(math.log(gamma/g1)/denom) if gamma>g1 else 0.0
        # apex weight is large near the first polar anchor and decays into base-face depth
        w0=max(0.0, 1.0-r)
        # base weights are angular soft assignments to the three base vertices
        sigma=math.pi/3
        logits=np.array([-circle_dist(theta,a)**2/(2*sigma*sigma) for a in base_angles], dtype=float)
        ex=np.exp(logits-logits.max())
        wb=ex/ex.sum()
        w=np.concatenate([[w0], r*wb])
        w=w/w.sum()
        point=w@V
        rows.append({
            'zero_index':n,'gamma':gamma,'theta':theta,'depth_r':r,
            'w_apex':w[0],'w_base_1':w[1],'w_base_2':w[2],'w_base_3':w[3],
            'x':point[0],'y':point[1],'z':point[2]
        })
    return pd.DataFrame(rows)

def seed_indices(p,q,steps=STEPS,nz=NZ):
    op=collatz_orbit(p,steps)
    oq=collatz_orbit(q,steps)
    idx=[]
    for k,(a,b) in enumerate(zip(op,oq)):
        # Deterministic zeta sampling: symmetric in the twin-prime pair, with k retaining time order.
        idx.append(((a + b + k + (a*b)%nz) % nz) + 1)
    return idx, op, oq

def seed_zeta_features(p,q,zdf):
    idx,op,oq=seed_indices(p,q)
    rows=zdf.set_index('zero_index').loc[idx]
    W=rows[['w_apex','w_base_1','w_base_2','w_base_3']].to_numpy()
    meanW=W.mean(axis=0)
    eps=1e-12
    entropy=float(-(meanW*np.log(meanW+eps)).sum()/math.log(4))
    asym=float(meanW.max()-meanW.min())
    polar=float(meanW[0])
    base_balance=float(np.std(meanW[1:]))
    # spectral walk in tetrahedral points
    P=rows[['x','y','z']].to_numpy()
    path=float(np.linalg.norm(np.diff(P,axis=0),axis=1).sum())
    mean_depth=float(rows['depth_r'].mean())
    theta=np.unwrap(rows['theta'].to_numpy())
    phase_winding=float((theta[-1]-theta[0])/(2*math.pi))
    # zeta-tetrahedral spectral action: no mass input; fixed structural coefficients.
    raw=(entropy + asym + 0.5*polar + base_balance + 0.05*path/STEPS + 0.1*abs(phase_winding))
    return {
        'seed_p':p,'seed_q':q,'zeta_entropy':entropy,'vertex_asymmetry':asym,
        'polar_apex_weight':polar,'base_balance_std':base_balance,'tetra_spectral_path':path,
        'mean_zeta_depth':mean_depth,'phase_winding':phase_winding,
        'zeta_tetrahedral_action_raw_v11':raw,
        'mean_w_apex':meanW[0],'mean_w_base_1':meanW[1],'mean_w_base_2':meanW[2],'mean_w_base_3':meanW[3]
    }

def normalize(s):
    arr=np.array(s,dtype=float)
    mn,mx=float(arr.min()),float(arr.max())
    if abs(mx-mn)<1e-12:
        return np.zeros_like(arr)
    return (arr-mn)/(mx-mn)

zdf=zeta_zero_table(NZ)
zdf.to_csv(OUT/'zeta_zero_tetrahedral_weights_v1_1.csv', index=False)

seeds=[(3,5),(5,7),(11,13),(17,19),(29,31),(41,43)]
sdf=pd.DataFrame([seed_zeta_features(p,q,zdf) for p,q in seeds])
sdf['zeta_tetrahedral_action_norm_v11']=normalize(sdf['zeta_tetrahedral_action_raw_v11'])
sdf['zeta_tetrahedral_action_kappa_v11']=KAPPA*sdf['zeta_tetrahedral_action_norm_v11']
sdf.to_csv(OUT/'seed_zeta_tetrahedral_table_v1_1.csv', index=False)

prev_path=Path('/mnt/data/metatime_sm_full_action_seed_arbitration_v1_0/results/charged_fermion_action_assembly_v1_0.csv')
prev=pd.read_csv(prev_path)
minimal=sdf[sdf[['seed_p','seed_q']].apply(tuple, axis=1).isin([(3,5),(5,7),(11,13)])][['seed_p','seed_q','zeta_tetrahedral_action_norm_v11','zeta_tetrahedral_action_kappa_v11']]
merged=prev.merge(minimal,on=['seed_p','seed_q'],how='left')
# Add spectral term as explicit extra contribution, not refit. Preserve previous components.
merged['total_structural_action_unit_v11']=merged['total_structural_action_unit_v10']+merged['zeta_tetrahedral_action_norm_v11']
merged['total_structural_action_kappa_v11']=KAPPA*merged['total_structural_action_unit_v11']
# ordinal check within classes: heavier generation should have lower action.
order=[]
for cls,grp in merged.groupby('class'):
    gg=grp.sort_values('assigned_generation_v10')
    vals=gg['total_structural_action_unit_v11'].to_list()
    ok=all(vals[i]>vals[i+1] for i in range(len(vals)-1))
    order.append({'class':cls,'generation_action_descending':ok,'actions_by_generation':vals})
merged.to_csv(OUT/'charged_fermion_action_with_zeta_v1_1.csv', index=False)
summary={
    'version':'v1.1',
    'kappa':KAPPA,
    'zeta_zero_count':NZ,
    'steps_per_seed':STEPS,
    'mass_values_used_as_input':False,
    'minimal_triplet_order_by_zeta_action': sdf[sdf[['seed_p','seed_q']].apply(tuple,axis=1).isin([(3,5),(5,7),(11,13)])].sort_values('zeta_tetrahedral_action_raw_v11')[['seed_p','seed_q','zeta_tetrahedral_action_raw_v11']].to_dict(orient='records'),
    'charged_fermion_ordinal_checks':order,
    'open_debts':['derive final zeta-polar anchor rule from operator spectrum rather than candidate phase assignment','derive constructive Euler-Berry coherence term','derive numeric masses, not only ordinal hierarchy','extend to neutrino sector and mixing']
}
(OUT/'zeta_tetrahedral_summary_v1_1.json').write_text(json.dumps(summary,indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
