# METATIME SM — Debt 11 Chiral Representation Projection v3.0

**Status:** technical repo module.  
**Epistemic class:** structural-enumeration / formal-symbolic with exact rational checks.  
**Scope:** one-generation chiral representation table and projection-channel interface.  
**Mass prediction:** no.  
**Observed masses used:** no.  
**Purpose:** remove the flat scalar bottleneck identified in Debt 9 before any further one-anchor mass rescore.

## 1. Motivation

The v2.6 one-anchor mass test was methodologically clean but numerically negative. Its main ansatz used a single scalar proportionality between the electron anchor and each fermion action. The old Metatime documents indicate a richer chain:

`seed/orbit -> eigenvalue/tau -> sector -> representation projection -> holonomy/information/White-Thread -> mass`

Therefore Debt 11 must be addressed before returning to Debt 9. This module does not change the mass formula. It constructs the missing representation/projection interface.

## 2. Formal status legend

- **DEFINITION** — introduced convention or object.
- **ANSATZ** — controlled structural choice, not yet a theorem.
- **LEMMA** — local result under the listed assumptions.
- **PROOF / CHECK** — exact symbolic or rational verification.
- **INTERPRETATION** — physical reading of a formal object.
- **HYPOTHESIS** — not yet validated.
- **QUARANTINE** — useful candidate not promoted.
- **DO NOT CLAIM** — explicit forbidden overclaim.

## 3. DEFINITION — CP1 chiral axis and poles

The primitive chiral axis is represented as a CP1/Bloch doublet with two poles. The upper pole carries the positive weak-axis component and the lower pole carries the negative component. This is inherited from earlier modules:

`Killing generator -> two CP1 poles -> Berry phase closure -> Euler identity -> spin 1/2`

This module uses that axis as a representation table generator.

## 4. DEFINITION — hypercharge convention

The module uses the convention:

`electric charge = CP1 pole contribution + hypercharge`

The scalar doublet gate is represented by the Higgs hypercharge one half. This is a convention choice fixing the U(1) normalization relative to the neutral upper lepton state and the charged lower lepton state.

## 5. ANSATZ — minimal chiral channel set

The minimal physical one-generation table contains:

- lepton left doublet: neutrino left and charged lepton left;
- charged lepton right singlet;
- quark left doublet with three color copies;
- up-quark right singlet with three color copies;
- down-quark right singlet with three color copies.

The optional sterile right neutrino is included only as a quarantined extension. It is not required for the minimal anomaly cancellation table and it is not promoted here.

## 6. LEMMA — Higgs legality fixes legal left-right transitions

Given the CP1 doublet structure and the scalar doublet gate:

- charged lepton transition is legal through the ordinary scalar gate;
- down-quark transition is legal through the ordinary scalar gate;
- up-quark transition is legal through the conjugate scalar gate.

The script checks the exact rational residuals for these three transitions and obtains zero for each.

## 7. CHECK — anomaly residuals vanish

Right-handed physical channels are converted to left-handed conjugate fields for anomaly accounting. The exact rational checks give zero residual for:

- color-color-hypercharge;
- weak-weak-hypercharge;
- gravitational-hypercharge;
- cubic hypercharge.

This is not a mass prediction. It is a structural consistency gate for the one-generation representation table.

## 8. INTERPRETATION — Debt 11 projection operator

The table is not merely a list of particle names. It is the first version of a projection operator. Each particle channel receives a structured projection through:

- CP1 pole and spin axis;
- chirality;
- color/tetrahedral depth or colorless status;
- hypercharge;
- Higgs transition gate;
- information quantum channel;
- zeta-axis relation;
- Ramanujan scaling role.

This is the missing interface between the geometric action and the mass test. It prevents the next Debt 9 attempt from collapsing all particles into one scalar proportionality.

## 9. DEFINITION — information quantum role

The information operator is not a free numerical weight. It is treated as the quantum of informational-preference fluctuation. In this module it is assigned as a channel property and not used to fit any mass.

## 10. QUARANTINE — optional sterile neutrino

A right-handed sterile neutrino channel is listed separately as optional and quarantined. It may become relevant for the neutrino sector, but it is not required for the minimal chiral representation table and it is not used in anomaly closure.

## 11. VALIDATION GATE

Generated files:

- `results/chiral_representation_table_v3_0.csv`
- `results/projection_channel_table_v3_0.csv`
- `results/anomaly_and_higgs_gate_report_v3_0.json`
- `results/debt11_status_ledger_v3_0.json`

Gate status:

`STRUCTURAL_ENUMERATION_PASS`

## 12. Debt status

Debt 11 is **conditionally closed for the one-generation chiral table**.

It is **not** closed for:

- exact mass ratios;
- generation replication;
- CKM;
- PMNS;
- sterile-neutrino promotion;
- final representation-to-mass projection.

## 13. DO NOT CLAIM

Do not claim that this module derives masses.  
Do not claim that CKM or PMNS is derived.  
Do not claim that the optional sterile neutrino exists.  
Do not claim that the old `tau/eigenvalue` table is imported.  
Do not claim that Debt 9 is solved.

## 14. Next required step

Freeze a mass-projection operator using this representation table before any new one-anchor mass rescore. That operator must be defined independently of validation masses.
