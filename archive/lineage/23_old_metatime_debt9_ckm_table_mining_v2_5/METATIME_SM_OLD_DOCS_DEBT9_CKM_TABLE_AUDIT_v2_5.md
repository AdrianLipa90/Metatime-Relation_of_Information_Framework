# METATIME SM — Old Documents Mining for Debt 9, CKM, and Fermion Table v2.5

## Status

- **Module type:** audit / source mining / debt preparation.
- **Canonical status:** no new derivation promoted to canon.
- **Gate type:** structural-source PASS.
- **Input surface:** `00_original_metatime/Metatime-main` plus already extracted text from local PDF/text/code sources.
- **No observed masses used as new model input in this module:** true; this module only classifies old documents.

## Executive result

The old Metatime documents do contain usable material for the next debts, especially Debt 9 and CKM. However, the material must be split by epistemic weight.

The strongest useful points are:

1. A one-anchor scaling strategy exists in old material, but in several incompatible forms.
2. CKM has an explicit Berry-phase/cycle-overlap derivation candidate.
3. The old complete fermion table is useful as a tau/eigenvalue spectrum table, not yet as a first-principles gauge-representation table.
4. Several older solvers reproduce masses by using observed masses or fitting several anchors; these must be quarantined as prototypes, not derivations.

## Debt 9 — one Standard Model mass anchor

### Finding

The old root manuscript states that masses are generated from Collatz orbit lengths, with a base length, sector exponents, and scales calibrated to a single point such as electron or charm.

### Interpretation

This confirms the user’s point: allowing **one** Standard Model mass anchor could give a large benefit. It converts the unresolved absolute scale problem into a ratio-prediction problem.

### Required correction for v2.x

The old documents often use separate scales per family or several fitted anchors. That is not acceptable as final Debt 9 closure.

The v2.x path should be:

- choose exactly one mass anchor for dimensional scale;
- use the v2.x structural action for all dimensionless ratios;
- include Ramanujan scaling in the normalization layer;
- include zeta-Heisenberg fluctuation only as uncertainty/coherence width, not as a fitting knob;
- mark the anchored mass as `calibration`, not `prediction`;
- validate all other masses as ratio outputs.

### Preferred first anchor candidate

The electron mass is the best first anchor candidate because it is precise, stable, charged, light, and not dominated by QCD binding. It should be treated as a scale anchor only. The muon, tau, quarks, W, Z, Higgs, and neutrino scales should remain validation targets unless a later formal reason selects a different anchor.

## Quark mixing / CKM

### Finding

The old manuscript has a coherent CKM candidate:

- mixing from Berry-phase differences between quark cycles;
- cycle overlap / geodesic angle controls amplitude;
- Cabibbo angle from resonance peak differences and instability;
- light-heavy elements damped by holonomic/white-thread factors;
- CP phase/Jarlskog from a phase-volume expression.

### Epistemic status

This is **not yet a final proof** because some values are asserted or corrected by hand in prose. It is nevertheless better than a vague note: it is a real derivation candidate and should be migrated into a new CKM debt module.

### Required v2.x rewrite

CKM should be rewritten using:

1. the Debt 1 Killing generator;
2. the v2.4 Euler-identity/Berry-phase spin constraint;
3. the source-axis grammar from Debt 8;
4. zeta-Heisenberg fluctuation as phase uncertainty;
5. Ramanujan scaling for asymptotic damping of distant seed/cycle overlaps;
6. separate gate labels: formal, computational, structural-enumeration.

## PMNS / neutrino mixing

### Finding

The old PMNS simulator inserts known mixing angles and uses the code as an oscillation simulator. That is useful for numerical propagation but not a derivation.

The old Formal_SM material does contain a better debt target: the solar splitting mismatch requires a pairwise white-thread correction, interpreted through Euler-Berry redistribution and neutrino mixing.

### Required v2.x rewrite

Do not promote the old PMNS code as solution. Use it as simulator shell only. The derivation must start from pairwise topology and Euler-Berry phase redistribution.

## Fermion table / representation table

### Finding

Old Formal_SM contains a complete Metatime fermion spectrum table with tau-like eigenvalues, Berry phase, correction factor, model mass, physical mass, and PDG comparison.

Kappa_from_geometry contains a useful interpretation: Yukawa couplings are topological projections of the mass spectrum onto the Higgs sector, and Berry phases produce off-diagonal mixing.

It also gives a guardrail: metatime topology is orthogonal to gauge-sector anomaly cancellation.

### Limitation

This is not yet the full representation table derived from CP1. It is a spectrum/eigenvalue table plus SM-compatibility layer.

### Required v2.x rewrite

Debt 11 should use the old table as reference material, but derive representation rows from:

- CP1 poles and chiral axis;
- doublet/singlet split;
- color triplet vs singlet from tetrahedral depth;
- hypercharge from anomaly-compatible projection;
- Higgs doublet compatibility;
- Euler-Berry spin constraint.

## Quarantined old patterns

The following patterns are useful historically but must not be counted as final derivations:

1. Exact charged-lepton Vandermonde polynomial through three observed masses.
2. Heavy-quark log fit through c, b, t.
3. Light-quark exact correction factors extracted from observed masses.
4. NoParamSM engines that use PDG masses as internal reference and only modulate them.
5. PMNS simulator with observed angles inserted.

These can supply test harnesses and sanity checks, not proof.

## Recommended next module

Create a Debt 9 module with this status:

- **Definition:** one-anchor mass-scale calibration.
- **Ansatz:** electron mass as dimensional anchor for first pass.
- **Lemma:** all other masses must be produced as dimensionless ratios from the v2.x action.
- **Ramanujan scaling:** mandatory normalization/damping layer.
- **Zeta-Heisenberg:** fluctuation/uncertainty layer, not a fitted parameter.
- **Validation:** anchored mass excluded from prediction score; all other masses scored as ratios.
- **Do not claim:** exact numerical mass derivation until ratios are tested.

## Decision

Debt 9 can now move from “open” to “ready for first controlled derivation attempt.” CKM can move from “open search” to “old-source candidate found.” Debt 11 remains open but now has useful old table material and gauge-compatibility guardrails.
