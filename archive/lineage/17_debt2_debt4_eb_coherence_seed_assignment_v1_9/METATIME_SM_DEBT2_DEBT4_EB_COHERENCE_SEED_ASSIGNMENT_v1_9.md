# METATIME SM DEBT 2 / DEBT 4: EULER--BERRY COHERENCE AND SEED ASSIGNMENT v1.9

**Layer status:** canonical working module appended to the merged repository.

**Repository rule:** this module is a directory inside the merged repository. No nested archive is permitted.

## 0. Purpose

This module addresses two formal debts from the v1.5 ledger:

- **Debt 2:** define the Euler--Berry constructive coherence functional.
- **Debt 4:** derive the final seed-to-generation assignment after zeta coherence is promoted.

This module does **not** claim exact numerical fermion masses. It pays the structural part of the debt: the Euler--Berry coherence layer is defined and tested as a phase-ordering gate, not as a fitted mass model.

## 1. Definitions

### Definition 1.1 — Euler--Berry coherence channel

Let the phase transport channel be

\[
\mathcal A_{EBI}=\mathcal A_E+\mathcal A_B+\mathcal A_{AB}+\mathcal A_{\mathcal I}.
\]

The Euler--Berry coherence channel is the component of the full phase transport that measures whether the spinorial half-axis, Berry transport, zeta imaginary axis, and tetrahedral depth frame are mutually aligned.

### Definition 1.2 — zeta coherence is not raw damping

The zeta contribution is represented as an alignment factor

\[
\Omega_\zeta(s) \in [0,1],
\]

not as an unrestricted positive mass-action cost.

### Definition 1.3 — seed assignment after coherence

A seed-to-generation assignment is valid only if it preserves strict ordering under the assembled structural action after applying Euler--Berry coherence.

## 2. Ansatz layer

### Ansatz 2.1 — constructive coherence functional

For a seed sector \(s\), define the constructive coherence score

\[
\Omega_{EB}(s)=\Omega_{K}(s)\,\Omega_{\zeta}(s)\,\Omega_{\frac12}(s)\,\Omega_T(s),
\]

where:

- \(\Omega_K\) measures alignment with the Killing generator polar axis;
- \(\Omega_\zeta\) measures alignment with the imaginary zeta zero axis;
- \(\Omega_{1/2}\) measures compatibility with the projective half-axis;
- \(\Omega_T\) measures compatibility with the tetrahedral depth frame.

The coherence score acts as a reduction of destructive phase defect rather than a raw additive damping cost.

### Ansatz 2.2 — coherence action modifier

Let \(S_{base}(s)\) be the structural action assembled from tetrahedral/Poincare, Collatz, Fibonacci, Kepler, spin, chiral, and representation components. The coherence-corrected action is

\[
S_{EB}(s)=S_{base}(s)-\kappa\,\log\left(1+\alpha\,\Omega_{EB}(s)\right),
\]

where \(\kappa=\ln(2)/(24\pi)\) and \(\alpha\) is not fitted to masses in this module. In the validation script, \(\alpha=1\) is used as a fixed structural probe.

## 3. Lemmas and proofs

### Lemma 3.1 — coherence cannot be promoted as raw damping

**Statement.** Zeta-axis data cannot be added as a monotone raw mass-action cost at this stage.

**Proof.** Prior modules showed that direct raw zeta addition can disrupt the generational ordering preserved by the structural action. A term that breaks a validated ordering cannot be promoted as a canonical additive cost. Treating zeta as an alignment factor avoids this failure mode. QED.

### Lemma 3.2 — Euler--Berry coherence preserves the status of mass values as validation targets

**Statement.** The v1.9 coherence functional does not use observed fermion masses as inputs.

**Proof.** The executable validation script constructs coherence scores from seed labels, Collatz terminal behavior, zeta-index-derived phase labels, tetrahedral classes, and fixed constants. Observed fermion masses do not enter the construction. They are not used in the current seed-assignment check. QED.

### Lemma 3.3 — Debt 2 is operationally paid

**Statement.** Debt 2 is operationally paid at v1.9.

**Proof.** Debt 2 required a defined Euler--Berry constructive coherence functional. Definitions 1.1--1.3 and Ansätze 2.1--2.2 define such a functional and specify how it modifies the structural action without raw zeta damping. The validation script implements it. QED.

### Lemma 3.4 — Debt 4 is partially paid at the structural-order level

**Statement.** Debt 4 is structurally paid for generation ordering, but not yet for exact mass ratios.

**Proof.** The seed assignment after coherence is computed without mass inputs and validated against strict ordering classes rather than mass values. Exact ratios are not claimed. Therefore the ordering part is paid, while numerical mass prediction remains an open formal debt. QED.

## 4. Interpretation

### Interpretation 4.1 — what coherence means

Euler--Berry coherence is the phase compatibility between the polar Killing generator, the spinorial half-axis, the Berry transport channel, and the zeta imaginary zero axis. It is a gate of admissibility and constructive alignment, not a new free force.

### Interpretation 4.2 — why this pays the right debt

The missing piece was not another scalar cost. The missing piece was the rule deciding when spectral zeta data improve phase closure and when they should be blocked from acting as damping. This module provides that rule.

## 5. Validation gates

### Gate 5.1 — no nested archives

The merged repository must contain no archive files internally.

### Gate 5.2 — no mass-as-input

The executable validation must not read or fit observed fermion masses.

### Gate 5.3 — status discipline

All major statements are tagged as definition, ansatz, lemma, proof, interpretation, validation gate, or formal debt.

### Gate 5.4 — ordering preservation

The coherence-corrected action must preserve a strict three-generation structural order for charged fermion sectors.

## 6. Remaining formal debts

1. Derive the physical weak-isospin axis from first principles rather than adopting it as the canonical axis ansatz.
2. Turn the seed-ordering result into exact or bounded mass-ratio predictions.
3. Extend the coherence functional to neutrino masses and mixing.
4. Define CKM and PMNS matrices as relative holonomies of sectoral mass operators.
5. Prove or reject the suppression of twin-prime candidates beyond the minimal admissible triplet.

## 7. Status

Debt 2: **operationally paid**.

Debt 4: **partially paid** for seed ordering after coherence; not paid for exact mass ratios.

Mass values: **not predicted yet**.

Yukawa couplings: still treated as effective low-energy shadows, not fundamental inputs.
