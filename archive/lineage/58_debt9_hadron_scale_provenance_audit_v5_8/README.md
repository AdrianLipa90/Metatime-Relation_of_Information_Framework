# METATIME SM v5.8 — Hadron Scale Provenance Audit

## Verdict

`technical: PASS`  
`formal: PASS_WITH_STRONGER_PROVENANCE_DISTINCTION`  
`substantive: HADRON_TABLE_NOT_REJECTED_FOR_SMALL_ERROR_BUT_NOT_PROMOTED_WITHOUT_SCALE_PROVENANCE`  
`Debt 9 numeric spectrum: OPEN_NOT_CLOSED`

## Correction integrated

This module corrects the audit rule around hadron tables:

Small or even marginal errors are **not** a reason for rejection by themselves. A very accurate result can be real. The audit question is narrower:

```text
Can the table expose an executable route from non-mass constants to the MeV scale before benchmark comparison?
```

If yes, the result can be promoted for further sealed testing. If no, the table remains a structural clue or scoring table, not a Debt 9 closure.

## Source audit

The checked source layer supports several structural ingredients:

- `F_hadron` as a geometric mean over quark-pair `F_ij` values.
- Baryons as triplet states, not isolated quarks.
- Binding energy as topological / Collatz / holonomic contribution.
- Prime-product sigma/R(n) route for baryons, including proton `u↔3`, `d↔5`, `n_p=45`, `sigma(45)=78`, `R(45)=1.73`.
- The 21 percent confinement/instability boundary as a plausible diagnostic budget.

But the checked source layer does **not** yet expose a clean executable hadron MeV scale independent of mass anchors.

## Table classification

`SM_and_M_Theory_generalisation.pdf` contains the clean structural `F_hadron` prescription, but its baryon table exactly matches the displayed benchmark values. That is not impossible; it is simply not promotable without executable provenance.

`Formal_SM.pdf` contains a mixed baryon binding table. Proton/neutron/Sigma/Xi are close, while Lambda is not. This is useful because it shows real residual structure, but it also means the table is not a universal closure.

`Calabi_Yau2.pdf` contains explicit calibration / iteration language and underbound baryon masses around 100 MeV for light baryons. This is valuable as a warning: small binding corrections alone do not produce the nucleon scale.

`Perfect_numbers_and_rhe_strings.pdf` gives the cleanest next route: baryons as prime products and sigma/R(n) objects, but it explicitly acknowledges mismatch and says harmonic corrections are required.

## Decision

```text
small errors as such: NOT_A_REASON_FOR_REJECTION
exact hadron table: HOLD_AS_PROVENANCE_REQUIRED
F_hadron geometric mean: PRESERVE_AS_STRUCTURAL_OPERATOR_CANDIDATE
prime-product sigma/R(n): PRESERVE_AS_CLEAN_NEXT_DERIVATION_ROUTE
hadron MeV scale: NOT_YET_DERIVED_FROM_NON_MASS_CONSTANTS
Debt 9: OPEN_NOT_CLOSED
```

## Next step

v5.9 should try to derive a hadron-scale candidate from:

```text
prime-product sigma/R(n)
+ harmonic L(n) correction
+ tetrahedral triplet
+ W_ij holonomic links
+ OIB / Ramanujan normalization
+ confinement budget
```

Only after this scale is frozen should baryon benchmarks be used.
