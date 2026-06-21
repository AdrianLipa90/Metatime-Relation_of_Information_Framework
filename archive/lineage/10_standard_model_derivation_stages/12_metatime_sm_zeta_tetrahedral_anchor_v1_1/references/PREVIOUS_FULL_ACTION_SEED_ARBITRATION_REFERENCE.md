# METATIME / Standard Model Derivation
## Full Structural Mass-Action Assembly and Seed Arbitration v1.0

Status: technical derivation layer.  This is not yet a numerical mass prediction.

### 0. Purpose

Version v1.0 integrates the corrected geometric order:

1. Bloch sphere and spin sector;
2. tetrahedral depth;
3. Poincare disk derived from tetrahedral projection;
4. Collatz dynamics on the derived disk;
5. Fibonacci clock comparison;
6. Kepler orbital phase cost;
7. information scale \(\kappa=\ln 2/(24\pi)\);
8. chiral bridge gate;
9. representation holonomy cost.

The goal is to assemble a non-fitted structural action for charged Standard Model fermions before any attempt at numerical mass prediction.

Observed masses are not used as predictors.

### 1. Canonical information scale

\[
\kappa = \frac{\ln 2}{24\pi}.
\]

This scale is applied after dimensionless structural costs are computed.  It is not fitted to particle masses.

### 2. Tetrahedral-first order

The Poincare disk is not treated as primitive in v1.0.  It is downstream from tetrahedral depth:

\[
S^2_{\rm Bloch} \rightarrow B^3_{\rm Bloch} \rightarrow T_4 \rightarrow \mathbb D.
\]

The Collatz trajectory is therefore evaluated only after the tetrahedral projection has induced the disk coordinates.

### 3. Structural seed arbitration

The minimal twin-prime triplet is:

\[
(3,5),\quad (5,7),\quad (11,13).
\]

Three previously generated structural kernels are integrated:

- the v0.4 Collatz--Poincare action inherited through v0.5;
- the v0.8 tetrahedral--Poincare action;
- the v0.9 spin--Fibonacci--Kepler--Collatz kernel.

Each component is min-max normalized over the minimal triplet and then averaged with equal non-fitted weights:

\[
\mathcal A^{\rm gen}_{s,v1.0}=
\frac13
\left(
\widetilde{\mathcal A}^{v0.4}_s+
\widetilde{\mathcal A}^{v0.8}_s+
\widetilde{\mathcal A}^{v0.9}_s
\right).
\]

Larger structural action means stronger damping and therefore lower generation scale before additional coherence corrections.

The resulting assignment is written to:

`results/seed_arbitration_v1_0.csv`

### 4. Supersession of earlier generation assignment

The v0.5 assignment was based on an earlier, simpler action kernel.  After v0.8 and v0.9, the generation order is updated.

This is not a contradiction.  It is a supersession:

- v0.5 remains a historical Collatz--Poincare pilot;
- v1.0 is the first integrated tetrahedral-first seed arbitration.

### 5. Representation sign correction

The v0.7 representation diagnostic table used the wrong sign convention in its residual label, causing allowed transitions to be displayed as blocked.  The v0.6 chiral table was already correct.

The corrected mass-term convention is:

\[
-Y_L+Y_H+Y_R=0.
\]

Corrected representation rows are written to:

`results/representation_features_corrected_v1_0.csv`

### 6. Full charged-fermion structural action

For a charged fermion sector \(f\), the v1.0 structural action is assembled as:

\[
\mathcal S^{\rm structural}_{f,v1.0}
= \kappa
\left(
\mathcal A^{\rm gen}_{s(f),v1.0}
+ \mathcal A^{\rm rep}_{c(f),v1.0}
+ \mathcal A^{\rm chiral}_{c(f)}
\right).
\]

This is not yet the full Euler--Berry mass action, because it does not include:

- the zeta-polar to tetrahedral vertex map;
- the constructive Euler--Berry coherence term;
- absolute mass-scale normalization;
- mixing matrices;
- neutrino-specific mass mechanism.

The charged-fermion assembly table is written to:

`results/charged_fermion_action_assembly_v1_0.csv`

### 7. Ordinal validation only

Since no observed masses enter the predictor, v1.0 permits only an ordinal validation:

- within each charged class, the first generation should be most damped;
- the second generation should be intermediate;
- the third generation should be least damped.

This ordinal check passes for:

- charged leptons;
- down-type quarks;
- up-type quarks.

The validation table is written to:

`results/ordinal_validation_v1_0.csv`

### 8. Extended seed quarantine

The v0.9 kernel identifies additional strong candidates such as \((17,19)\).  These are not promoted to SM generations in v1.0.

They are placed in quarantine until a generation-count selection law is derived.

See:

`results/extended_seed_quarantine_v1_0.csv`

### 9. Validation status

v1.0 validates that:

- the Poincare disk is downstream of tetrahedral depth;
- spin, Fibonacci, Kepler and Collatz are integrated in one structural kernel;
- the information scale is applied without fitting masses;
- the representation residual sign error is corrected;
- a three-generation seed assignment can be produced without using observed masses;
- ordinal hierarchy within charged classes is structurally aligned.

v1.0 does not validate:

- numerical fermion masses;
- CKM or PMNS mixing;
- neutrino mass mechanism;
- absolute Standard Model parameter prediction.

### 10. Next derivation layer

The next layer should derive the zeta-polar to tetrahedral vertex map.  After that, the constructive Euler--Berry coherence term must be frozen.  Only then should the model attempt numerical mass ratios.
