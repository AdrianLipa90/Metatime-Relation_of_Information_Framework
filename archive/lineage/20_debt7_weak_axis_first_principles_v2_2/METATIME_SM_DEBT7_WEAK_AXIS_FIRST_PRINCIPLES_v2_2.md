# METATIME / Standard Model Derivation — Debt 7 Weak-Isospin Axis Selection v2.2

## Metadata

- Version: v2.2
- Parent repository: `METATIME_STANDARD_MODEL_DERIVATION_MERGED_REPO_v2_1_NO_NESTED_ZIPS`
- Module: `20_debt7_weak_axis_first_principles_v2_2`
- Purpose: address Debt 7: physical selection of the weak-isospin/Bloch quantization axis from structural first principles.
- Status: conditionally closed as a structural uniqueness result; not closed as an empirical or numerical mass prediction.

---

## Epistemic gate taxonomy added in v2.2

### [DEFINITION]
A **formal/symbolic PASS** verifies an identity, theorem ledger, structural implication, or typed derivation whose truth follows from already accepted premises. It may use a script to check bookkeeping, but the script is not an independent numerical experiment.

### [DEFINITION]
A **computational PASS** verifies a nontrivial calculation over generated data, sequences, candidate sets, or tables. It may still depend on assumptions, but it is not merely a hard-coded restatement of a theorem.

### [DEFINITION]
A **structural-enumeration PASS** sits between the two: it enumerates a finite set of allowed candidates and checks whether exactly one satisfies declared structural constraints. It is stronger than a pure symbolic restatement, but weaker than empirical numerical prediction.

### [VALIDATION GATE]
All future validation reports must report at least these fields:

- `gate_id`
- `gate_type`
- `premises_used`
- `independent_computation: true/false`
- `uses_observed_masses_as_input: true/false`
- `status`

This prevents a Poincaré-Hopf theorem check and a Collatz/Ramanujan enumeration from being collapsed into a single undifferentiated `PASS`.

---

# Debt 7: Why the primitive Bloch/Killing axis is the weak-isospin axis

## [PROBLEM]
Debt 1 established the primitive phase generator as a Killing field on CP1, equivalently on the Bloch sphere. It also established that the two poles are zeros of that field and therefore not arbitrary labels.

Debt 7 remains: **which physical axis realizes this CP1 polar structure?**

Candidate axes considered in the prior module:

1. Berry phase axis.
2. Weak-isospin/Bloch quantization axis.
3. Twin-prime/Collatz generation axis.
4. Zeta imaginary zero axis.
5. Color/SU(3) internal axis.
6. Hypercharge/U(1) axis.

---

## [DEFINITION] Primitive polar axis requirements

A physical candidate may serve as the primitive CP1 polar axis only if it satisfies all of the following requirements.

1. **Two-pole requirement:** it must have a natural two-pole structure matching the CP1/Bloch sphere polar pair.
2. **Killing-flow requirement:** it must generate or select a one-parameter rotation/phase flow with fixed polar points.
3. **Chirality requirement:** it must distinguish the left-handed electroweak doublet structure from right-handed singlet structure.
4. **Charge-splitting requirement:** it must split the two components of a weak doublet before electric charge is assembled.
5. **Mass-gate requirement:** it must feed the allowed left-right transition gate without inserting Yukawa couplings as primitive constants.
6. **Non-arithmetic-selector requirement:** it must be a continuous geometric/gauge axis, not merely a discrete seed label.
7. **Non-connection-only requirement:** it must not be only a connection/holonomy transported around a previously selected axis.

---

## [LEMMA 7.1] Berry phase is not the primitive selector

Berry phase is a holonomy of a connection over a parameter-space path. It requires a chosen bundle/axis/path structure to be transported around. Therefore Berry phase is a transport and closure layer, not the primitive selector of the CP1 polar axis.

### [PROOF]
The Berry layer answers how phase is accumulated under transport. Debt 1 asks which Killing field supplies the two fixed polar states. A connection can carry the phase around a chosen geometry, but it does not by itself pick the physical chiral doublet axis. Therefore Berry is downstream of the axis selection.

### [STATUS]
Symbolic/formal PASS.

---

## [LEMMA 7.2] Twin-prime/Collatz data are not the primitive selector

Twin-prime seeds and Collatz orbits provide arithmetic sector labels and dynamical projections. They do not supply a continuous Killing field on CP1 by themselves.

### [PROOF]
A twin-prime pair is discrete arithmetic input. A Collatz trajectory is a discrete map. Neither object is a smooth vector field on CP1. They can index generation sectors, action weights, suppression gates, and Poincaré-disk trajectories after the geometric surface exists. They cannot be the primitive continuous polar selector.

### [STATUS]
Symbolic/formal PASS.

---

## [LEMMA 7.3] Zeta imaginary zeros are not the primitive selector

The zeta axis is an imaginary spectral axis that anchors coherence and polar labels. It does not independently generate the CP1 Killing field.

### [PROOF]
The zeta layer is defined in previous modules as an imaginary-zero coherence axis. It labels or constrains the polar structure after the two-pole geometry is available. If it were allowed to pick arbitrary poles, Debt 3 would become arbitrary again. Therefore zeta must be a spectral coherence axis respecting the existing polar pair, not the primitive selector.

### [STATUS]
Symbolic/formal PASS.

---

## [LEMMA 7.4] Color cannot be the primitive CP1 polar selector

Color is a triplet internal sector. Its natural minimal internal multiplicity is three, not two. It is also vectorlike in the Standard Model representation structure relevant to mass generation.

### [PROOF]
The CP1/Bloch polar geometry requires a two-state polar pair. SU(3) color supplies a triplet degree of freedom. It is crucial for quark multiplicity and representation cost, but it does not provide the two-component chiral weak doublet axis. Therefore color is downstream of the weak doublet structure in this derivation.

### [STATUS]
Structural/formal PASS.

---

## [LEMMA 7.5] Hypercharge alone cannot be the primitive CP1 selector

Hypercharge supplies a U(1) label. It does not by itself provide the two-pole doublet splitting needed for the two components of an electroweak doublet.

### [PROOF]
A single U(1) label can assign phase/charge weight, but it does not create an internal two-component doublet with opposite third components. Electric charge requires the combination of weak isospin component and hypercharge. Therefore hypercharge is a closure/label component, not the primitive polar selector.

### [STATUS]
Structural/formal PASS.

---

## [THEOREM 7.6] Conditional uniqueness of the weak-isospin axis

Given the primitive polar axis requirements, the weak-isospin/Bloch quantization axis is the unique candidate among the listed physical sectors that satisfies all requirements.

### [PROOF]
Berry is excluded because it transports phase around an already selected axis. Twin-prime/Collatz is excluded as primitive because it is discrete and arithmetic rather than a smooth CP1 Killing selector. Zeta is excluded as primitive because it is a spectral coherence axis that must respect the polar pair. Color is excluded because its natural multiplicity is three, not the CP1 polar pair. Hypercharge alone is excluded because it cannot split a doublet into two polar components.

The remaining candidate is weak isospin. It supplies a two-component left-handed doublet, a quantization axis with two polar eigenstates, chiral distinction between left doublets and right singlets, and the required pre-electric-charge splitting. Therefore, within these premises, the primitive CP1/Killing axis must be the weak-isospin/Bloch quantization axis.

### [STATUS]
Structural-enumeration PASS, conditional on the candidate set and primitive-axis requirements.

---

## [INTERPRETATION]
Debt 7 is not solved by saying “choose weak isospin because the Standard Model has weak isospin.” That would be circular. The v2.2 result is narrower and stronger:

- the CP1/Killing structure demands a two-pole continuous axis;
- mass generation demands chirality and a legal left-right transition gate;
- charge assembly demands a doublet splitting before hypercharge completes electric charge;
- among the available physical sectors, weak isospin is the only sector satisfying all of these simultaneously.

Thus weak isospin is not merely selected by convention; it is selected as the only candidate that can carry the primitive polar geometry without breaking the already established constraints.

---

## [HYPOTHESIS]
The weak-isospin axis is the physical realization of the primitive CP1 Killing axis because it is the minimal continuous two-pole chiral axis from which charge splitting, Berry transport, zeta coherence, and generation-sector arithmetic can be layered without circularity.

---

## [DO NOT CLAIM]

Do not claim that v2.2 derives the full Standard Model from absolute nothing.

Do not claim that v2.2 numerically predicts particle masses.

Do not claim that weak isospin has been empirically derived from a new measurement.

Do not claim that the proof is independent of the chosen candidate set and the declared primitive-axis requirements.

---

## [DEBT STATUS UPDATE]

- Debt 7 previous status: open.
- Debt 7 new status: conditionally closed as structural-enumeration theorem.
- Remaining debt inside Debt 7: prove that the candidate set is complete from the root geometry itself, not merely from the known Standard Model sector list.
- New derived debt: formulate the root-geometry-to-gauge-sector completeness theorem.

---

## [NEXT STEP]

The next formal target is the first controlled mass-ratio attempt using:

1. weak-isospin CP1 axis;
2. zeta imaginary-axis coherence;
3. Collatz transition axis four-two-one-half;
4. Ramanujan scaling/suppression;
5. chiral gate;
6. representation cost;
7. no observed masses as input.
