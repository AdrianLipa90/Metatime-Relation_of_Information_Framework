# METATIME / Standard Model Derivation
## Representation Holonomy Cost Layer v0.7

Status: technical derivation layer, not a final mass prediction.

### 0. Purpose

This layer follows the previous `METATIME_SM_CHIRAL_HOLONOMY_COST_v0_6` artifact.  Version v0.6 established that the three charged Standard Model Dirac sectors have legal left--right bridges through the appropriate Higgs orientation:

- charged lepton: ordinary Higgs bridge,
- down-type quark: ordinary Higgs bridge,
- up-type quark: conjugate Higgs bridge.

The present layer freezes a representation-level feature map.  Its task is not to predict masses.  Its task is to separate the three mass-sector classes before the generation vector and the Euler--Berry action functional are evaluated.

Observed fermion masses are not used as predictors in this layer.

### 1. Canonical sectors

The layer uses three canonical charged fermion classes:

1. charged leptons,
2. down-type quarks,
3. up-type quarks.

The neutrino sector remains outside this freeze, except as an open optional Dirac extension.  It must not be silently promoted to the same mass law before the neutrino mechanism is decided.

### 2. Chiral bridge check

For each charged sector, the transition must preserve both hypercharge and electric charge across the left--right bridge.  The bridge is evaluated in the physical right-handed convention, not the left-handed conjugate notation used for anomaly bookkeeping.

The transition checks are exact rational checks.  The resulting table is written to:

`results/representation_transition_features_v0_7.csv`

All three charged transitions are allowed.

### 3. Representation feature vector

For every charged class, the representation vector contains:

- color multiplicity depth,
- weak-isospin bridge involvement,
- hypercharge jump across the bridge,
- Higgs selector orientation,
- electric charge sector,
- color coherence,
- Higgs-conjugation marker.

This is a representation-level feature map.  It is not yet the full mass vector.  The full mass vector must still include:

- the generation vector from the twin-prime seed and Collatz orbit,
- the Poincare disk embedding,
- the zeta-polar/tetrahedral-depth component,
- the Euler--Berry coherence term.

### 4. Candidate representation action

A diagnostic candidate representation action is defined in the script.  It is deliberately marked as diagnostic, not final.  It combines transition cost terms and subtracts constructive coherence terms from color multiplicity and the conjugate Higgs bridge.

This candidate is useful because it distinguishes the three charged Standard Model classes without referring to observed masses.

It is not sufficient to predict numerical masses.

### 5. Distinguishability result

The distinguishability check uses the color-depth, electric-charge-sector, and Higgs-conjugation components.  The three class signatures are linearly independent in this diagnostic basis.

Result summary:

- charged leptons, down-type quarks, and up-type quarks are separated at the representation layer;
- no observed masses are used;
- the layer is therefore eligible to enter the later Euler--Berry action functional as a structural component.

See:

`results/representation_rank_summary_v0_7.json`

### 6. What is frozen

Frozen in v0.7:

- the three charged mass-sector classes;
- exact charge-preserving chiral bridges inherited from v0.6;
- the representation feature basis;
- the rule that representation features may enter the Euler--Berry mass action only as structural predictors, not fitted mass labels.

### 7. What remains open

Still open:

- the full Euler--Berry mass action;
- the zeta-polar/tetrahedral-depth contribution;
- the constructive White-Thread/Euler--Berry coherence term;
- the neutrino mass mechanism;
- exact numerical mass predictions.

### 8. Next step

The next derivation layer should combine:

1. the generation assignment from v0.5,
2. the chiral bridge from v0.6,
3. the representation features from v0.7,
4. the Collatz--Poincare action kernel from v0.4,

into a single non-fitted mass-action score.  The output may be compared to observed hierarchy only after the score is computed.
