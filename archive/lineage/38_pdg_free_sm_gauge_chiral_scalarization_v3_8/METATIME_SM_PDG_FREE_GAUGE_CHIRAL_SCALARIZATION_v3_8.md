# METATIME / Standard Model Derivation — PDG-Free Gauge-Chiral Skeleton and Frozen Pre-Mass Scalarization v3.8

Created UTC: 2026-06-20T13:30:00Z  
Base: v3.7 Repair3 forensic quarantine.  
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
canon_allowed: false
current_promotion: DENY_CURRENT
Doctor verdict: CONTINUE_RESEARCH__PDG_FREE_SM_SKELETON_PASS
```

v3.8 does **not** try to repair v3.6 Repair2 by producing another mass table. Repair3 proved that the previous apparent success was polluted by reference replay and PDG input leakage. Therefore v3.8 moves one layer earlier: it develops the Standard Model derivation as a gauge-chiral and pre-mass operator skeleton.

The module establishes two valid advances:

1. a PDG-free one-generation gauge/chiral hypercharge derivation using anomaly cancellation and Yukawa gauge invariance;
2. a frozen pre-mass structural signature layer for future mass-action testing using CP1/Bloch, CP2 terminal cell, Collatz valuation words, Ramanujan-theta residues, zeta-axis semantics, and the information quantum `ln(2)/(24*pi)`.

It makes no claim that fermion masses have been derived.

---

## 1. Repair3 boundary carried forward

### [GUARD]

The following sources remain quarantined for mass prediction:

- copied canonical spectrum tables where `mass_calc == reference`;
- `NoParamSM` engines that contain internal PDG/reference mass dictionaries;
- old tau/eigenvalue tables if their normalization or selection used observed masses;
- CKM/PMNS numerical values unless they are used only after execution as external benchmarks.

### [RULE]

Dependency class is a blocker when it indicates reference leakage. It is not merely metadata.

### [CONSEQUENCE]

v3.8 is not allowed to use non-anchor observed masses, PDG tables, CKM, PMNS, or old fitted tau/eigenvalue spectra as inputs. In this module there is also no electron anchor, because no dimensional mass test is performed.

---

## 2. Source-provenance map from the uploaded set

The module used the full uploaded set as source material, but only in the safe form below.

| Source class | Used for | Forbidden use |
|---|---|---|
| Repair3 v3.7 repo | quarantine state and anti-fit guard | none |
| `Download.zip` step notes | CP1 Bloch-Fubini-Study, Collatz terminal cell, Ramanujan-theta, zeta-axis/CP2 geometry | no hidden mass target extraction |
| `Metatime-main.zip` old docs | historical formulas and warning labels | no old spectrum table as prediction |
| `Informational-Dynamics-of-Metatime-main.zip` | Bloch/orbital/semantic topology context | no runtime/SoT claim |

Concrete hashes are stored in:

- `provenance/input_archive_sha256_v3_8.txt`
- `provenance/source_document_sha256_v3_8.txt`

This is artifact-grounded provenance, not an external NOEMA CURRENT.

---

## 3. Gauge group skeleton from projective geometry

### [DEFINITION] Local spinor/Bloch sector

The local projective spinor sector is represented by a CP1 chart. Its natural unitary lift is an SU(2) action on the two-component spinor, with a U(1) stabilizer corresponding to phase around a selected axis.

```math
CP^1 \simeq SU(2)/U(1).
```

### [INTERPRETATION]

This gives a controlled reason why a weak SU(2)-like doublet structure appears before masses are discussed. The CP1/Bloch layer supplies the doublet geometry; it does not yet determine the complete Standard Model by itself.

### [DEFINITION] Polar / Killing U(1) stabilizer

The selected north-south Killing/polar axis carries a residual phase stabilizer. The corresponding phase channel is treated as a U(1)-type holonomy channel.

This is the geometric layer that later supports hypercharge/electric-charge bookkeeping.

### [DEFINITION] CP2 terminal cell and color warning

The terminal Collatz cell `4 -> 2 -> 1` is represented as a CP2 projective cell with local CP1 edges. CP2 has the homogeneous description

```math
CP^2 \simeq SU(3)/(SU(2)\times U(1)).
```

This is **not automatically a proof of QCD color SU(3)**. It supplies a triplet projective terminal-cell geometry. A full color derivation must prove why the determinant-one unitary lift acts as a local internal gauge symmetry rather than only as a terminal-cell coordinate symmetry.

### [STATUS]

```text
SU(2)_weak-like CP1 doublet geometry: structurally supported
U(1)_axis/hypercharge-like phase channel: structurally supported
SU(3)_color: candidate lift from CP2 terminal triplet, not yet proven as local color gauge principle
```

This is deliberate discipline: CP2 evidence is not oversold as a complete QCD derivation.

---

## 4. Chiral representation skeleton

### [DEFINITION] One-generation left-handed Weyl convention

The active one-generation field skeleton is:

```math
Q      : (3,2,Y_Q),
\quad u^c : (\bar 3,1,Y_u),
\quad d^c : (\bar 3,1,Y_d),
```

```math
L      : (1,2,Y_L),
\quad e^c : (1,1,Y_e),
\quad H   : (1,2,Y_H).
```

All fermions are represented as left-handed Weyl fields; `u^c`, `d^c`, and `e^c` are left-handed conjugates of the usual right-handed fields.

### [CONSTRAINT] Yukawa gauge invariance

The allowed Higgs couplings impose:

```math
Y_Q + Y_H + Y_u = 0,
```

```math
Y_Q - Y_H + Y_d = 0,
```

```math
Y_L - Y_H + Y_e = 0.
```

### [CONSTRAINT] Anomaly cancellation

The gauge/gravitational anomaly constraints are:

```math
2Y_Q + Y_u + Y_d = 0,
```

```math
3Y_Q + Y_L = 0,
```

```math
6Y_Q + 3Y_u + 3Y_d + 2Y_L + Y_e = 0,
```

```math
6Y_Q^3 + 3Y_u^3 + 3Y_d^3 + 2Y_L^3 + Y_e^3 = 0.
```

### [LEMMA] Hypercharge ratios are fixed up to normalization

From `3Y_Q + Y_L = 0`, we have:

```math
Y_L = -3Y_Q.
```

The Yukawa constraints give:

```math
Y_u = -Y_Q - Y_H,
```

```math
Y_d = -Y_Q + Y_H,
```

```math
Y_e = Y_H - Y_L.
```

The gravitational anomaly then forces:

```math
Y_H = 3Y_Q.
```

Thus the ratios are fixed up to an overall U(1) normalization. Choosing the conventional Higgs normalization

```math
Y_H = \frac12
```

gives:

```math
Y_Q=\frac16,
\quad
Y_u=-\frac23,
\quad
Y_d=\frac13,
\quad
Y_L=-\frac12,
\quad
Y_e=1.
```

### [VALIDATION]

The script `scripts/sm_hypercharge_anomaly_derivation_v3_8.py` derives these values using only representation multiplicities, anomaly equations, Yukawa gauge-invariance equations, and the Higgs normalization convention. It reads no masses.

Output:

- `results/sm_hypercharge_anomaly_derivation_v3_8.json`
- `results/sm_hypercharge_anomaly_derivation_v3_8.stdout.json`

Validation status:

```text
all anomaly and Yukawa checks zero: true
mass input: none
CKM/PMNS input: none
```

### [RESULT]

This is a genuine Standard Model structural step: it recovers the chiral hypercharge pattern of one generation without importing the fermion mass spectrum.

It is not a mass derivation.

---

## 5. Electric charge check

Using

```math
Q_{em}=T_3+Y,
```

the derived hypercharges produce the expected charge pattern in the left-handed Weyl convention:

```text
u_L: 0
e_L: -1
u/e doublet split: by T3
u/e singlet conjugate: e_c has charge +1 in left-handed conjugate notation
u quark doublet components: +2/3 and -1/3
```

This confirms that the hypercharge skeleton is internally coherent.

---

## 6. Pre-mass scalarization rule: frozen but not canonized

### [PROBLEM]

v3.6 established that a sector projection operator must not be collapsed directly into a scalar mass correction. v3.8 therefore freezes a safer pre-mass layer before any mass benchmark.

### [DEFINITION] Structural signature vector

For a twin-prime seed `s=(p,p+2)` with seed integer

```math
N_s=p(p+2),
```

define a structural signature vector:

```math
\Xi_s =
\left(
D_p,
D_{p+2},
\sigma_R(N_s),
\vec c_R(N_s),
\Theta_s,
\kappa
\right).
```

The components are:

- `D_p`, `D_{p+2}`: Collatz valuation-word compensation defects;
- `sigma_R(N_s)`: Hardy-Ramanujan asymptotic scale;
- `vec c_R(N_s)`: Ramanujan-sum residue vector for fixed small modular channels;
- `Theta_s`: theta-residue diagnostic around the compensation balance;
- `kappa = ln(2)/(24*pi)`: information preference fluctuation quantum.

### [DEFINITION] Frozen diagnostic scalar

A frozen pre-mass scalar diagnostic is defined as:

```math
A^{pre}_s
=
\frac{\bar D_s}{\kappa}
+
\frac{\log(1+\sigma_R(N_s))}{24}
-
\Theta_s
-
\frac{c_{24}(N_s)}{24}.
```

This is **not** a mass law. It is a frozen diagnostic used to prevent future silent refitting of the scalarization rule.

### [GUARD]

The diagnostic cannot be edited after non-anchor mass residuals are computed. If future work changes it after seeing residuals, the result is a fit and must be quarantined.

### [VALIDATION]

The script `scripts/pdg_free_structural_signature_v3_8.py` produces:

- `results/pdg_free_structural_signature_v3_8.json`
- `results/pdg_free_structural_signature_v3_8.csv`
- `results/pdg_free_structural_signature_v3_8.stdout.json`

Every row has:

```text
mass_prediction_claimed: false
```

### [CURRENT OUTPUT]

The canonical visible seeds are preserved as structural seeds:

```text
(3,5), (5,7), (11,13)
```

Additional twin-prime seeds up to the scan limit are not deleted; they remain extended-sector quarantine candidates.

---

## 7. What v3.8 does and does not prove

### [PROVEN / EXECUTED]

- Hypercharge ratios for one SM generation follow from anomaly cancellation plus Yukawa gauge invariance, up to U(1) normalization.
- The active computation uses no PDG masses, no observed fermion masses, no CKM, no PMNS, and no old tau/eigenvalue mass tables.
- A pre-mass structural signature layer using Collatz/Ramanujan/theta/kappa has been frozen for future tests.
- No nested archives are present in the repo.

### [NOT PROVEN]

- Full SU(3) color as a local QCD gauge principle is not yet proven from CP2 terminal-cell geometry.
- Three generations are not yet proven; the canonical three seeds remain visible, while extended seeds are quarantined candidates.
- Fermion mass ratios are not yet derived.
- CKM and PMNS matrices are not yet derived.
- Higgs potential parameters are not yet derived.

---

## 8. Validation report

`results/VALIDATION_MODULE38_v3_8.json` reports:

```text
status: PASS
active code forbidden PDG-table patterns absent: true
active outputs forbidden mass tokens absent: true
structural signature claims no masses: true
hypercharge anomaly and Yukawa checks zero: true
no nested archives: true
Doctor verdict: CONTINUE_RESEARCH__MODULE38_GUARD_PASS
```

---

## 9. Next step for v3.9

The next valid module should not weaken this guard. It should do one of two things:

1. prove the CP2 terminal triplet lift into a true local SU(3) color gauge principle; or
2. apply the frozen pre-mass scalarization to a one-anchor mass-ratio test, with the scalarization rule immutable before reading residuals.

If the mass route is chosen, the only admissible dimensional anchor must be declared before execution, and every other observed mass must appear only as an external benchmark after the output is already generated.

---

## 10. Decision

```text
v3.8: ACCEPT_AS_RESEARCH_PROGRESS
Debt 9: OPEN_NOT_CLOSED
Mass derivation: NOT_CLAIMED
Gauge-chiral skeleton: PDG_FREE_STRUCTURAL_PASS
Pre-mass scalarization: FROZEN_DIAGNOSTIC_PASS
Canon promotion: DENY_CANON
Current promotion: DENY_CURRENT
```
