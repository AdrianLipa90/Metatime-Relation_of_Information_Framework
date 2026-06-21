# METATIME / Standard Model Derivation — Debt 8
## Source-Geometric Axis Candidate Grammar v2.3

**Module:** `21_debt8_source_axis_candidate_grammar_v2_3`  
**Status:** `CONDITIONALLY_CLOSED_STRUCTURAL_ENUMERATION`  
**Gate class:** `STRUCTURAL_ENUMERATION_PASS`, not `COMPUTATIONAL_PASS`  
**Purpose:** repay the debt opened by Debt 7: the candidate list for the physical axis must be derived from the source geometry, not borrowed from the finished Standard Model.

---

## 0. Epistemic status

This module is not a numerical mass prediction. It is a structural enumeration module.

- **Definition:** source inventory and admissible axis grammar.
- **Ansatz:** minimal source grammar is sufficient to enumerate the possible axis roles.
- **Lemma:** only one source-derived candidate has the correct two-pole, CP1, chiral, doublet-splitting profile.
- **Proof:** finite exclusion by gate criteria.
- **Interpretation:** the surviving abstract axis is identified with weak isospin only after matching to the SM representation skeleton.
- **Hypothesis:** this abstract axis is forced by source geometry rather than selected from SM hindsight.
- **Do not claim:** no numerical masses, no CKM/PMNS closure, no absolute proof that the primitive inventory is complete.

---

## 1. Definition — source primitives

The source geometry available before using SM hindsight contains the following primitive strata:

1. `CP1_BLOCH_SURFACE`: a projective two-state surface, equivalently a Bloch sphere.
2. `KILLING_FLOW`: a one-parameter isometry flow on that surface.
3. `TWO_FIXED_POLES`: the north/south fixed pair required by the Killing flow on the sphere.
4. `BERRY_CONNECTION`: phase transport around the chosen axis.
5. `ZETA_IMAGINARY_AXIS`: spectral zero / imaginary phase axis.
6. `TETRAHEDRAL_DEPTH`: internal depth before the Poincare disk.
7. `POINCARE_DISK`: derived hyperbolic dynamics surface.
8. `COLLATZ_TERMINAL_AXIS`: the four-two-one-half transition bridge.
9. `TWIN_PRIME_SEED_INDEX`: arithmetic sector index.
10. `RAMANUJAN_SCALING`: asymptotic suppression / modular scaling layer.
11. `CHIRAL_MASS_GATE`: legal left-right transition gate.

These are not all physical gauge groups. They are source roles from which candidate axes may be formed.

---

## 2. Definition — admissible primary axis

A candidate can serve as the primitive physical axis only if it satisfies all of the following criteria:

1. It supports a continuous flow.
2. It has exactly two fixed poles on a CP1/Bloch surface.
3. It can carry chirality.
4. It can split a doublet.
5. It can couple to the mass gate without importing observed masses.
6. It is not merely a transport connection.
7. It is not merely a discrete arithmetic index.
8. It is not merely a spectral-coherence label.
9. It is not merely a higher-depth triplet sector.
10. It is source-derived before SM representation matching.

---

## 3. Ansatz — abstract axis before naming

**Ansatz 8.1.** The primitive axis must first be named abstractly as:

`SOURCE_DERIVED_CHIRAL_CP1_AXIS`

Only after it is matched to the known representation skeleton should it be interpreted as the weak-isospin axis.

This prevents a circular derivation. The derivation does not begin by assuming weak isospin. It begins with a two-pole chiral CP1 axis and then observes that the SM realization of that axis is weak isospin.

---

## 4. Lemma — Berry is not the selector

**Lemma 8.1.** The Berry layer cannot select the primitive pole pair.

**Reason.** Berry phase is a holonomy of transport around an already available axis. It requires a loop and a connection. It does not by itself generate the two fixed points of the Killing flow.

**Status:** `FORMAL_SYMBOLIC_PASS`.

---

## 5. Lemma — twin-prime / Collatz is not the selector

**Lemma 8.2.** The twin-prime/Collatz layer cannot be the primitive continuous axis selector.

**Reason.** It is discrete and arithmetic. It can index sectors, supply trajectory rhythm, and contribute action. It does not provide the continuous CP1 Killing flow required for two fixed poles.

**Status:** `STRUCTURAL_ENUMERATION_PASS`.

---

## 6. Lemma — zeta is not the selector

**Lemma 8.3.** The zeta layer is not the primitive real generator axis.

**Reason.** In this model zeta is placed as the imaginary zero axis at the half transition. It labels spectral coherence and phase compatibility. It is not the real two-pole Killing field itself.

**Status:** `STRUCTURAL_ENUMERATION_PASS`.

---

## 7. Lemma — color/tetrahedral depth is not the selector

**Lemma 8.4.** The color/tetrahedral sector cannot be the primitive CP1 axis selector.

**Reason.** Tetrahedral depth is prior to the Poincare disk and can support internal triplet/color-like structure. A triplet depth sector does not select exactly the two fixed poles of a CP1/Bloch surface.

**Status:** `STRUCTURAL_ENUMERATION_PASS`.

---

## 8. Lemma — hypercharge is not the selector

**Lemma 8.5.** Hypercharge is not the primitive CP1 axis selector.

**Reason.** Hypercharge is an abelian charge label. It does not by itself split a two-state chiral doublet into north/south pole states on CP1.

**Status:** `STRUCTURAL_ENUMERATION_PASS`.

---

## 9. Theorem — surviving source-derived axis

**Theorem 8.1.** Under the source grammar above, the only candidate that satisfies the primitive-axis gate is the abstract two-pole chiral CP1 axis.

**Proof sketch.**

- Berry is transport, not selection.
- Twin-prime/Collatz is discrete arithmetic indexing, not continuous selection.
- Zeta is spectral/imaginary coherence, not the real Killing generator.
- Tetrahedral/color depth is triplet-like, not two-pole CP1 selection.
- Hypercharge is abelian labeling, not doublet splitting.
- The remaining source-derived candidate is a two-pole chiral CP1 axis generated by a Killing flow and able to carry the mass gate.

Therefore the primitive axis is not selected from the SM by name. It is derived as `SOURCE_DERIVED_CHIRAL_CP1_AXIS`; the SM interpretation of that abstract axis is weak isospin.

**Status:** `CONDITIONALLY_CLOSED_STRUCTURAL_ENUMERATION`.

---

## 10. Interpretation for Debt 7

Debt 7 should be updated from:

> weak isospin selected by ansatz among known SM-like axes

into:

> source geometry forces an abstract chiral CP1 two-pole axis; weak isospin is the SM realization of that axis.

This is stronger and less circular. It does not yet prove the full SM gauge sector from nothing, but it removes the immediate defect that the candidate list was simply imported from known SM sectors.

---

## 11. Validation-gate taxonomy update

This module also updates the validation language introduced after the v2.1 audit.

- `FORMAL_SYMBOLIC_PASS`: proof or symbolic/topological accounting.
- `STRUCTURAL_ENUMERATION_PASS`: finite candidate enumeration under explicit source criteria.
- `COMPUTATIONAL_PASS`: real numerical/table computation over generated data.
- `EMPIRICAL_TARGET_CHECK`: comparison to observed values, not used as model input.

Debt 8 uses structural enumeration. It is not a computational pass.

---

## 12. Updated debt status

| Debt | Topic | Status after v2.3 |
|---:|---|---|
| 1 | Killing generator / polar axis | conditionally closed |
| 2 | Euler-Berry coherence | operationally closed |
| 3 | zeta-polar anchoring | operationally closed |
| 4 | seed assignment after zeta coherence | partially closed |
| 5 | Ramanujan suppression of surplus seeds | partially closed |
| 6 | mass action hierarchy | partially closed |
| 7 | physical weak-axis derivation | strengthened; conditionally closed through abstract source-derived CP1 axis |
| 8 | source derivation of candidate axis list | conditionally closed in v2.3 |
| 9 | exact mass ratios without fitted masses | open |
| 10 | CKM/PMNS and neutrino sector | open |

---

## 13. Do not claim

Do not claim that v2.3 proves exact masses.

Do not claim that v2.3 proves all of SU(2) from a complete independent theorem.

Do not claim that v2.3 is an empirical confirmation.

Do claim that v2.3 prevents the immediate circularity: the axis candidate list is now derived from the source-role grammar before SM naming.
