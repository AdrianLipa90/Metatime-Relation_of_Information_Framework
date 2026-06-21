# METATIME SM Chiral Holonomy Cost v0.6

## Status

This artifact continues the Metatime Standard Model derivation by closing the first non-fitted chiral transition cost layer. It does not claim a completed fermion mass prediction. It freezes the gauge-invariant left--right transition gate that replaces primitive Yukawa couplings by holonomic mass-transition amplitudes.

## Input layers

1. Euler--Berry canonical closure v0.1.
2. Standard Model gauge skeleton v0.1.
3. Mass vectorization v0.1.
4. Euler--Berry action closure v0.2.
5. Generation embedding v0.3.
6. Collatz--Poincare action kernel v0.4.
7. Mass action assembly v0.5.

Observed fermion masses are not used in this artifact.

## Purpose

The v0.5 action assembly left the chiral slot open:

```math
\mathcal S^{EB}_{f,g}
=
\kappa\,[
\mathcal G_{seed}(g)
+
\mathcal R_{rep}(f)
+
\mathcal C_{chir}(f)
+
\mathcal Z_{spec}(f,g)
-
\Omega_{EB}(f,g)
]_+.
```

This v0.6 artifact freezes the first canonical version of

```math
\mathcal C_{chir}(f).
```

The key rule is that a fermion mass transition is not produced by a primitive Yukawa parameter. It is an allowed holonomic bridge between a left chiral state and a right chiral state through the electroweak orientation selector.

## Chiral transition gate

Let a physical Dirac transition be written as

```math
f_L \xrightarrow{H_\sigma} f_R,
```

where

```math
H_\sigma\in\{H,\widetilde H\}.
```

The transition is allowed only if it satisfies the gauge-invariant phase balance

```math
-Y_L(f)+Y(H_\sigma)+Y_R(f)=0.
```

The direct Higgs selector has

```math
Y(H)=+\frac12,
```

and the conjugate selector has

```math
Y(\widetilde H)=-\frac12.
```

The executable transition classes are:

| class | left state | right state | selector | status |
|---|---|---|---|---|
| charged_lepton | `e_L` | `e_R` | `H` | allowed |
| down_quark | `d_L` | `d_R` | `H` | allowed |
| up_quark | `u_L` | `u_R` | `H_conj` | allowed |
| neutrino_dirac_optional | `nu_L` | `nu_R` | `H_conj` | optional_extension |

The optional Dirac neutrino row is included only as a future extension hook. It is not promoted to a canonical neutrino mass mechanism in this artifact.

## Canonical v0.6 chiral cost

The first frozen chiral transition cost is universal for all allowed Dirac mass bridges:

```math
\mathcal C_{chir}^{(0)}(f)=1+|T_3(f_L)|+|Y(H_\sigma)|.
```

For all allowed Standard Model charged transitions:

```math
\mathcal C_{chir}^{(0)}(f)=2.
```

The physical meaning is:

1. one unit for crossing the left--right chiral boundary;
2. one half-unit for selecting a weak-isospin component inside the left doublet;
3. one half-unit for the Higgs orientation selector.

This cost is not fitted to fermion masses. It is fixed by representation topology and the electroweak orientation selector.

## What this closes

The v0.6 artifact closes the universal chiral bridge gate. It determines which left--right transitions are allowed, which Higgs orientation is required, and what the first universal chiral cost is.

It does not yet close the flavor-specific mass hierarchy. Because the v0.6 cost is universal across charged Dirac fermions, generation splitting and sector splitting must come from the non-universal slots:

```math
\mathcal G_{seed},\quad
\mathcal R_{rep},\quad
\mathcal Z_{spec},\quad
\Omega_{EB}.
```

## Validation

The executable validation script verifies:

1. all charged transitions have zero hypercharge residual;
2. electric charge is preserved across the selected transition;
3. color representation is preserved for quark mass bridges;
4. the optional Dirac neutrino row is not promoted to a canonical neutrino mass claim;
5. the v0.6 chiral cost is universal and equals 2 for allowed transitions.

## Verdict

v0.6 closes the chiral transition gate but remains non-predictive for masses by itself. It is an essential constraint layer: it ensures that any later mass action is built only from gauge-allowed Euler--Berry left--right bridges rather than primitive Yukawa parameters.
