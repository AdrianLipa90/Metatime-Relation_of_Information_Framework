# METATIME / Standard Model Derivation — Tetrahedral Triplet and SU(3)-Candidate Lift v3.9

Created UTC: 2026-06-20T15:40:00Z  
Base: v3.8 PDG-free gauge-chiral skeleton.  
NOEMA SoT: unavailable; artifact-grounded append-only module only.  
Canon status: **not canonized**.  
Debt 9 status: **OPEN_NOT_CLOSED**.  

## 0. Executive status

```text
technical: PASS
formal: PASS
substantive: PARTIAL STRUCTURAL PROGRESS
numeric_mass_prediction: NOT_ATTEMPTED
PDG/reference input: FORBIDDEN AND ABSENT FROM ACTIVE EXECUTION
full_QCD_claimed: false
canon_allowed: false
current_promotion: DENY_CURRENT
Doctor verdict: CONTINUE_RESEARCH__TETRA_TRIPLET_SU3_LIFT_PASS__QCD_NOT_CLOSED
```

v3.9 continues from the Repair3/v3.8 guard boundary. It does **not** produce a mass table and does **not** claim that QCD has been fully derived. Its purpose is narrower and necessary: formalize the statement that the projective/tetrahedral layer can carry a triplet and that the local complex lift of that triplet has the correct `su(3)` candidate algebra.

The valid statement is:

```text
tetrahedral centered frame
  -> choose one vertex as closure/reference
  -> three residual face/edge modes
  -> complex triplet carrier C^3
  -> CP2 projective carrier
  -> local unitary lift U(3), determinant-one traceless candidate SU(3)
```

The forbidden statement is:

```text
tetrahedron alone proves full QCD / gluon dynamics / confinement / hadron phenomenology
```

---

## 1. Guard boundary inherited from v3.8

### [GUARD]

Forbidden as active inputs:

- PDG or any experimental mass table;
- observed fermion masses;
- CKM or PMNS numeric matrices;
- old fitted tau/eigenvalue tables;
- any hidden mass reference dictionary.

### [RULE]

This module is a geometry/algebra carrier test only. It is not a mass derivation and not a full QCD derivation.

---

## 2. Tetrahedral source of the triplet

Use the centered regular tetrahedron in real three-space:

```math
v_0=(1,1,1),\quad
v_1=(1,-1,-1),\quad
v_2=(-1,1,-1),\quad
v_3=(-1,-1,1).
```

The closure condition is:

```math
v_0+v_1+v_2+v_3=0.
```

Choosing `v_0` as reference/closure leaves three residual modes:

```math
e_1=v_1-v_0,
\quad e_2=v_2-v_0,
\quad e_3=v_3-v_0.
```

The computed determinant of the edge-mode matrix is:

```text
-16
```

Therefore the three residual modes are linearly independent. This is the precise sense in which the tetrahedral frame yields a triplet. The triplet is not read from “four vertices becoming three by rhetoric”; it is read from one closure/reference vertex plus three independent residual modes.

The edge Gram matrix is:

```text
[[8, 4, 4],
 [4, 8, 4],
 [4, 4, 8]]
```

The normalized off-diagonal cosine is `1/2`, so the modes retain tetrahedral symmetry rather than an arbitrary coordinate basis.

---

## 3. Opposite face and CP2 carrier

The face opposite `v_0` is an equilateral triangle formed by `v_1,v_2,v_3`. These three labels provide the carrier labels:

```text
color_0, color_1, color_2
```

Promote the three real structural labels into a complex internal carrier:

```math
\mathcal{H}_c \cong \mathbb{C}^3.
```

Physical internal rays are projectivized:

```math
\mathbb{CP}^2=(\mathbb{C}^3\setminus\{0\})/\mathbb{C}^{*}.
```

This is the clean projective reason the terminal triplet naturally points to a CP2-like color carrier. However, the finite tetrahedral symmetry by itself is only a discrete frame symmetry. The continuous gauge lift requires a further local-unitary principle.

---

## 4. Local unitary lift and `su(3)` candidate algebra

Once the internal triplet is represented as `C^3`, the structure-preserving local transformations are unitary transformations of this carrier:

```math
U(3).
```

Removing the overall determinant phase leaves the traceless determinant-one candidate:

```math
SU(3).
```

The active script verifies the standard eight Gell-Mann generators as a basis of the traceless Hermitian generator space. Checks performed:

- generator count equals 8;
- every generator is Hermitian;
- every generator is traceless;
- normalization satisfies `Tr(lambda_a lambda_b)=2 delta_ab`;
- commutators close in the Gell-Mann span after division by `i`.

Numerical residual for commutator closure:

```text
4.965068306494546e-16
```

This is floating-point zero for the structural algebra check.

---

## 5. What this proves and what it does not prove

### Proven / established inside v3.9

1. A centered tetrahedron has a zero closure relation.
2. Choosing one vertex as reference leaves three independent residual modes.
3. Those three modes can serve as a triplet carrier.
4. The complex projective carrier is CP2.
5. The local unitary lift of the complex triplet has an SU(3)-candidate traceless sector.
6. The eight-generator algebraic basis passes Hermitian, traceless, normalization, and commutator closure tests.

### Not proven / still open

1. Full QCD dynamics.
2. Gluon kinetic term from the Metatime action.
3. Gauge coupling origin and running.
4. Confinement.
5. Hadron spectrum.
6. Fermion mass spectrum.
7. Debt 9 closure.

---

## 6. Relation to Standard Model derivation path

v3.8 established a PDG-free gauge-chiral skeleton and one-generation hypercharge/anomaly consistency. v3.9 adds a PDG-free color-carrier bridge:

```text
v3.8: CP1 / weak doublet / U(1) axis / hypercharge anomaly skeleton
v3.9: tetrahedral residual triplet / CP2 carrier / SU(3)-candidate algebraic lift
```

Together these support the structural Standard Model skeleton:

```text
SU(3)-candidate x SU(2)-candidate x U(1)-candidate
```

but the word “candidate” remains mandatory until the action-level gauge dynamics are derived.

---

## 7. Validation summary

Generated files:

- `scripts/tetra_triplet_su3_lift_v3_9.py`
- `scripts/validate_module39_v3_9.py`
- `results/tetra_triplet_su3_lift_v3_9.json`
- `results/tetra_triplet_su3_lift_v3_9.stdout.json`
- `results/VALIDATION_MODULE39_v3_9.json`
- `results/VALIDATION_MODULE39_v3_9.stdout.json`

Validation status:

```text
PASS
```

Validation checks:

- mass prediction not claimed;
- full QCD not claimed;
- tetrahedral edge modes independent;
- tetrahedral center closure zero;
- CP2 carrier dimension equals three;
- finite tetrahedral symmetry not enough is explicitly declared;
- Gell-Mann generator count equals eight;
- generators Hermitian, traceless, normalized;
- commutator closure passes;
- no active forbidden code patterns;
- no active forbidden numeric mass tokens;
- no nested archives.

---

## 8. Next required step

The next module should not jump to masses. It should derive the gauge-field/action layer:

```text
triplet carrier -> local connection -> curvature -> Yang-Mills-like kinetic term -> coupling/gauge-source status
```

Only after that should the derivation return to masses or CKM-like mixing. Otherwise the project risks repeating the earlier failure mode: numerically attractive outputs without a closed structural path.
