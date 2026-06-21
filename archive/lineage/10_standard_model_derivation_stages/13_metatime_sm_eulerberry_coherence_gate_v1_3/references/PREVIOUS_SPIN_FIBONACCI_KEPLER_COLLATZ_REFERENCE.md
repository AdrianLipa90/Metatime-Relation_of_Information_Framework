# METATIME SM Spin--Fibonacci--Kepler--Collatz Action Kernel v0.9

## Status

This document is a technical continuation of the Standard Model derivation program. It corrects the previous ordering by placing the tetrahedral layer before the Poincare disk and then extends the generational action kernel by adding spin, Fibonacci rhythm, the information scale, Kepler dynamics, and Collatz dynamics.

This is not yet a numerical derivation of fermion masses. It is a structural kernel for the Euler--Berry action. Observed masses are not used as input.

## Canonical input layers

The active input stack is:

1. Hilbert/Kahler state geometry.
2. Bloch sphere and spin-one-half two-cover closure.
3. Tetrahedral depth inside the Bloch ball.
4. Poincare disk derived from tetrahedral internal projection.
5. Twin-prime seeds and Collatz trajectories.
6. Fibonacci rhythm as a second arithmetic clock.
7. Keplerian orbital motion as a geometric phase clock on the derived disk.
8. Information scale kappa = ln(2)/(24 pi).

## Tetrahedral origin of the disk

The Poincare disk is not inserted independently. A regular tetrahedral frame is embedded inside the Bloch ball. An internal two-plane is generated from tetrahedral edge data. Seed-dependent barycentric coordinates define an interior tetrahedral point. That point is projected into the internal plane and then mapped into the unit disk. The resulting disk coordinate is the allowed stage for Collatz and Kepler dynamics.

## Spin layer

Spin one half is implemented as a two-cover phase condition. The relevant phase closure is not a two-pi closure but a four-pi closure. The kernel therefore carries a spin-half phase and a spin-closure defect. The defect is not fitted to masses. It is computed from the geometric path accumulated by the Kepler and parity dynamics.

## Fibonacci rhythm

The Fibonacci layer is introduced as an independent arithmetic rhythm. It is not a replacement for Collatz. It measures the mismatch between logarithmic Collatz growth and Fibonacci growth on the same discrete clock. This introduces a golden-ratio regularity test into the action kernel.

## Collatz dynamics

For each twin-prime seed, two Collatz trajectories are computed. The pair is treated as a two-branch generational itinerary. The branch length, parity twist, and logarithmic growth profile are used as structural features.

## Kepler dynamics

A Keplerian clock is induced on the derived Poincare disk. The disk radius controls eccentricity and an effective orbital scale. Collatz and Fibonacci data determine discrete mean anomalies. Solving Kepler's equation gives an orbital trajectory and an accumulated orbital action. This supplies a geometric phase-clock contribution to the Euler--Berry action.

## Information operator scale

The action kernel is scaled by

\[
\kappa = \frac{\ln 2}{24\pi}.
\]

The current kernel has the form

\[
S_{s}^{(0.9)}
=
\kappa
\left(
C_s^{\rm Collatz/Fibonacci}
+G_s^{\rm Poincare}
+K_s^{\rm Kepler}
+P_s^{\rm parity}
+\Delta_s^{\rm spin}
\right).
\]

This is a structural action. It is not yet the full fermion mass action because it still lacks the final zeta--tetrahedral spectral term and the constructive Euler--Berry coherence term.

## Validation gates

The v0.9 kernel must satisfy the following gates:

1. It must not use observed fermion masses as inputs.
2. The Poincare disk must be obtained from tetrahedral projection.
3. Collatz trajectories must be computed directly from twin-prime seeds.
4. Fibonacci rhythm must be computed directly and independently.
5. Keplerian motion must be solved explicitly, not represented by a label.
6. The information scale must be the exact ln(2)/(24 pi) value.
7. Spin one half must enter through a four-pi closure defect.

All gates are satisfied by the reference script.

## Interpretation

The important conceptual change is that the generational seed is no longer evaluated only by Collatz depth. It is evaluated by a composite action in which tetrahedral geometry creates the disk, Collatz supplies the discrete itinerary, Fibonacci supplies an independent arithmetic regularity clock, Kepler supplies an orbital phase clock, spin supplies the two-cover closure condition, and kappa supplies the information scale.

## Remaining debts

The following items remain open:

1. Derive the zeta-polar to tetrahedral barycentric map canonically.
2. Add the spectral zeta-depth term.
3. Add constructive Euler--Berry coherence.
4. Attach representation and chiral costs from v0.6 and v0.7.
5. Test whether the resulting full action orders and then predicts fermion mass hierarchy without mass input.
