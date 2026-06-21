# METATIME SM Mass Action Assembly v0.5

## Status

This artifact continues the Standard Model derivation program by assembling the first generation-level Euler--Berry action hierarchy kernel. It does not claim a completed mass prediction. It establishes a no-mass-input assignment rule for the three generation seeds and verifies that the induced action ordering matches the observed within-family mass ordering only after the assignment has been made.

## Canonical input layers

1. Euler--Berry phase closure v0.1.
2. Standard Model gauge skeleton v0.1.
3. Mass vectorization v0.1.
4. Euler--Berry action closure v0.2.
5. Generation embedding v0.3.
6. Collatz--Poincare action kernel v0.4.

Observed masses are not used to select seeds, coefficients, or the generation assignment.

## No-free-Yukawa rule

The Standard Model Yukawa couplings remain effective low-energy projections. They are not primitive parameters of the present construction. The primitive object is the holonomic mass transition operator acting on the full vectorized state.

## Generation assignment rule

Let the minimal twin-prime seed triplet be

```math
(3,5),\quad (5,7),\quad (11,13).
```

The v0.4 Collatz--Poincare kernel assigns each seed a dimensionless Euler--Berry generation action. The v0.5 rule is:

```math
\text{larger generation action}\Rightarrow\text{stronger exponential suppression}\Rightarrow\text{lighter generation}.
```

Therefore the three generations are assigned by sorting the minimal seed triplet by action in descending order.

## Frozen v0.5 assignment

The resulting structural assignment is:

| Generation | Seed | Role | Status |
|---:|---:|---|---|
| 1 | (3,5) | lightest | structural no-mass-fit assignment |
| 2 | (11,13) | middle | structural no-mass-fit assignment |
| 3 | (5,7) | heaviest | structural no-mass-fit assignment |

This assignment is not obtained from the electron, muon, tau, quark masses, or any fitted Yukawa value.

## Assembled action form

The working Euler--Berry mass action is kept in slot form:

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

Here:

- `G_seed` is the Collatz--Poincare generation action from v0.4.
- `R_rep` is the representation contribution from the Standard Model gauge skeleton.
- `C_chir` is the left-right transition cost.
- `Z_spec` is the zeta/tetrahedral spectral-depth contribution.
- `Omega_EB` is constructive Euler--Berry coherence.

In v0.5 only the generation slot is numerically assembled. The remaining slots are not fitted.

## Validation after assembly

The observed mass-derived action targets are used only after the seed assignment is frozen, and only to check ordering. The v0.5 result is:

| Family | Order check |
|---|---|
| Charged leptons | PASS |
| Up-type quarks | PASS |
| Down-type quarks | PASS |

This is an order-level validation, not a quantitative mass prediction.

## Interpretation

The v0.5 result is important because it shows that the Collatz--Poincare generation kernel can supply the correct qualitative hierarchy direction across all three charged fermion families without using the observed masses to choose the generation seeds.

The result does not yet derive fermion masses. A mass prediction requires freezing the representation contribution, the chiral transition cost, the zeta/tetrahedral contribution, and the constructive Euler--Berry coherence term.

## Open derivation debts

1. Freeze `R_rep` from representation data without fitting masses.
2. Freeze `C_chir` from the Euler spinor closure and the Higgs orientation selector.
3. Freeze `Z_spec` from zeta-polar anchors and tetrahedral depth.
4. Freeze `Omega_EB` from Berry/Euler coherence rather than from mass targets.
5. Run quantitative mass prediction only after all slots are closed.

## Verdict

v0.5 closes the first no-mass-input generation action assembly. It upgrades the generation layer from a diagnostic candidate list to a structural hierarchy kernel. It remains pre-predictive for absolute masses.
