#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math, pathlib
import numpy as np

OUT = pathlib.Path(__file__).resolve().parents[1]
KAPPA = math.log(2)/(24*math.pi)
V = 246.22
# tau values taken as internal Metatime candidate eigenvalues from Formal_SM / framework summary.
# They are model-side labels, not observed masses.
FERMIONS = [
    # name, sector, tau, color_dim, weak_dim_L, Y_L_or_relevant, T3_L, Q, chirality_type, generation_index
    ("e",   "charged_lepton", 4.0,   1, 2, -0.5, -0.5, -1.0, "L/R_pair", 1),
    ("mu",  "charged_lepton", 1.0,   1, 2, -0.5, -0.5, -1.0, "L/R_pair", 2),
    ("tau", "charged_lepton", 10.0,  1, 2, -0.5, -0.5, -1.0, "L/R_pair", 3),
    ("u",   "up_quark",       0.05,  3, 2,  1/6,  0.5,  2/3, "L/R_pair", 1),
    ("c",   "up_quark",       5.0,   3, 2,  1/6,  0.5,  2/3, "L/R_pair", 2),
    ("t",   "up_quark",       100.0, 3, 2,  1/6,  0.5,  2/3, "L/R_pair", 3),
    ("d",   "down_quark",     0.10,  3, 2,  1/6, -0.5, -1/3, "L/R_pair", 1),
    ("s",   "down_quark",     0.40,  3, 2,  1/6, -0.5, -1/3, "L/R_pair", 2),
    ("b",   "down_quark",     10.0,  3, 2,  1/6, -0.5, -1/3, "L/R_pair", 3),
]
# validation targets only: masses are not used to define any no-input candidate.
MASSES_GEV = {
    "e":0.00051099895, "mu":0.1056583755, "tau":1.77686,
    "u":0.00216, "d":0.00467, "s":0.0934,
    "c":1.27, "b":4.18, "t":172.69,
}

def target_action(name: str) -> tuple[float,float,float]:
    y = math.sqrt(2)*MASSES_GEV[name]/V
    A = -math.log(y)
    S = KAPPA*A
    return y,A,S

def features(row):
    name, sector, tau, color_dim, weak_dim, Y, T3, Q, chirality, gen = row
    # Model-side feature basis. No observed mass enters.
    log_tau = math.log(tau)
    inv_log_tau = math.log(1/tau) if tau > 0 else 0
    colorless = 1 if color_dim == 1 else 0
    colored = 1 if color_dim == 3 else 0
    up_type = 1 if sector == "up_quark" else 0
    down_type = 1 if sector == "down_quark" else 0
    charged_lepton = 1 if sector == "charged_lepton" else 0
    return {
        "intercept":1.0,
        "log_tau":log_tau,
        "abs_log_tau":abs(log_tau),
        "log_tau_sq":log_tau*log_tau,
        "colorless":colorless,
        "colored":colored,
        "weak_dim_minus_1":weak_dim-1,
        "abs_Y":abs(Y),
        "abs_Q":abs(Q),
        "T3":T3,
        "generation_index":gen,
        "up_type":up_type,
        "down_type":down_type,
        "charged_lepton":charged_lepton,
    }

def no_input_candidate(row):
    """A deliberately non-fitted first action candidate using unit coefficients.
    This is a stress test, not a prediction claim.
    """
    name, sector, tau, color_dim, weak_dim, Y, T3, Q, chirality, gen = row
    # top is normalized to minimal action when tau = 100 and colored up-type.
    collatz_depth = max(0.0, math.log(100.0/tau))
    representation_barrier = 0.0
    # colorless states need an orientation barrier in this crude candidate.
    representation_barrier += (1 if color_dim == 1 else 0) * math.log(3.0)
    # charge magnitude as phase-orientation mismatch.
    representation_barrier += abs(Q) * 0.5
    # weak doublet chiral transition cost.
    representation_barrier += (weak_dim-1) * 0.25
    # down-sector Euler-Berry pairing penalty; sign is model-side from T3=-1/2.
    representation_barrier += (1 if T3 < 0 else 0) * 0.25
    return collatz_depth + representation_barrier

rows=[]
for row in FERMIONS:
    name, sector, tau, color_dim, weak_dim, Y, T3, Q, chirality, gen = row
    y,A,S = target_action(name)
    feat = features(row)
    A0 = no_input_candidate(row)
    rows.append({
        "fermion":name,"sector":sector,"tau":tau,"color_dim":color_dim,"weak_dim":weak_dim,
        "Y":Y,"T3":T3,"Q":Q,"generation_index":gen,
        "y_eff_validation":y,"A_required_minus_ln_y":A,"S_required":S,
        "A_no_input_candidate":A0,"S_no_input_candidate":KAPPA*A0,
        "A_residual_candidate_minus_required":A0-A,
        **{f"feature_{k}":v for k,v in feat.items()}
    })

# Representation-only rank: remove tau and generation, use reps only.
rep_cols=["intercept","colorless","colored","weak_dim_minus_1","abs_Y","abs_Q","T3","up_type","down_type","charged_lepton"]
full_cols=["intercept","log_tau","abs_log_tau","log_tau_sq","colorless","colored","weak_dim_minus_1","abs_Y","abs_Q","T3","generation_index","up_type","down_type","charged_lepton"]

def fit(cols):
    X=np.array([[r[f"feature_{c}"] for c in cols] for r in rows], dtype=float)
    y=np.array([r["A_required_minus_ln_y"] for r in rows], dtype=float)
    rank=int(np.linalg.matrix_rank(X))
    coef, residuals, _, _ = np.linalg.lstsq(X,y,rcond=None)
    pred=X@coef
    rmse=float(np.sqrt(np.mean((pred-y)**2)))
    max_abs=float(np.max(np.abs(pred-y)))
    return X,y,rank,coef,pred,rmse,max_abs

_,_,rank_rep,coef_rep,pred_rep,rmse_rep,max_rep=fit(rep_cols)
_,_,rank_full,coef_full,pred_full,rmse_full,max_full=fit(full_cols)

for i,r in enumerate(rows):
    r["A_diagnostic_fit_rep_only"] = float(pred_rep[i])
    r["A_diagnostic_fit_full_basis"] = float(pred_full[i])
    r["residual_rep_only"] = float(pred_rep[i]-r["A_required_minus_ln_y"])
    r["residual_full_basis"] = float(pred_full[i]-r["A_required_minus_ln_y"])

with (OUT/"results"/"mass_action_feature_table.csv").open("w", newline="") as f:
    writer=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

summary={
    "kappa_ln2_over_24pi":KAPPA,
    "charged_fermions_checked":len(rows),
    "no_input_candidate_status":"stress test only; not a successful mass prediction",
    "representation_only_rank":rank_rep,
    "representation_only_columns":rep_cols,
    "representation_only_rmse_on_validation_actions":rmse_rep,
    "representation_only_max_abs_residual":max_rep,
    "full_diagnostic_basis_rank":rank_full,
    "full_diagnostic_basis_columns":full_cols,
    "full_diagnostic_rmse_on_validation_actions":rmse_full,
    "full_diagnostic_max_abs_residual":max_full,
    "rank_warning":"Fits using validation targets are diagnostic only. They do not define S_EB.",
    "mathematical_conclusion":[
        "Representation data alone are rank-deficient for generation-dependent masses.",
        "A generation/orbit vector is necessary.",
        "A pure unit-coefficient action is not sufficient.",
        "The next required object is an explicit orbit-to-geometry map z_s(k) and a derived Euler-Berry action integral."
    ]
}
with (OUT/"results"/"mass_action_rank_summary.json").open("w") as f:
    json.dump(summary,f,indent=2)

# write human readable report
with (OUT/"results"/"mass_action_basis_report.txt").open("w") as f:
    f.write("METATIME SM EB ACTION BASIS AUDIT v0.2\n")
    f.write(f"kappa = {KAPPA}\n")
    f.write(f"representation-only rank = {rank_rep}, RMSE on validation actions = {rmse_rep:.6f}, max_abs = {max_rep:.6f}\n")
    f.write(f"full diagnostic basis rank = {rank_full}, RMSE on validation actions = {rmse_full:.6f}, max_abs = {max_full:.6f}\n")
    f.write("\nConclusion: representation-only vectors cannot derive the generation hierarchy. Collatz/orbit geometry is mathematically required.\n")

print(json.dumps(summary, indent=2))
