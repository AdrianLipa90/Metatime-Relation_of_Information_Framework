# Metatime / Standard Model Derivation — Collatz--Poincare Action Kernel v0.4

Status: technical derivation candidate, not final canon and not a mass prediction.

## Purpose

This layer continues the Standard Model derivation after the gauge skeleton, mass vectorization, Euler--Berry action closure, and generation embedding layers.

The previous layer established that a generation vector is required. This layer begins replacing the diagnostic generation-depth score by an explicit geometric action kernel built from twin-prime Collatz orbits embedded into the Poincare disk.

No observed fermion masses are used as input.

## Inputs

The inputs are:

1. twin-prime seed pairs;
2. Collatz orbit pairs;
3. a deterministic bounded embedding into the Poincare disk;
4. Poincare path length diagnostics;
5. branch-divergence and parity-closure diagnostics;
6. zeta-alignment diagnostics against low non-trivial zeta-zero heights.

## Canonical working objects

Let a candidate generation seed be a twin-prime pair.

For each branch, compute its Collatz orbit. The pair of orbits defines a discrete two-branch trajectory.

The v0.4 embedding maps each paired Collatz step into a point of the Poincare disk. The radial coordinate is bounded by a hyperbolic tangent of the mean logarithmic amplitude. The angular coordinate is driven by step index, parity imbalance, and relative logarithmic branch displacement. This keeps every point strictly inside the disk and makes the construction deterministic.

The kernel then computes:

- Collatz logarithmic action;
- branch divergence;
- parity closure defect;
- Poincare path length per step;
- mean hyperbolic radius;
- zeta-alignment cost.

These quantities are normalized over the candidate scan and combined as an equal-weight v0.4 action-kernel candidate.

## Non-fitting rule

The v0.4 kernel is explicitly mass-blind. Observed masses are not read by the script. They are not used to choose coefficients, seeds, ranks, or normalizations.

Therefore this layer may select or order seed candidates, but it does not yet predict the fermion mass spectrum.

## Minimal arithmetic triplet

The minimal arithmetic twin-prime triplet is:

- (3, 5);
- (5, 7);
- (11, 13).

This triplet is selected by arithmetic minimality, not by observed masses.

The v0.4 action ordering of this triplet is stored in `results/collatz_poincare_action_summary_v0_4.json` and `results/collatz_poincare_action_table_v0_4.csv`.

## Interpretation

This stage gives the first explicit candidate for the generational action contribution. It upgrades the previous generation embedding from a diagnostic vector to a geometric kernel.

The important conclusion is not yet the numerical mass hierarchy. The important conclusion is that a non-mass structural kernel can now assign different action values to candidate generation seeds.

## Validation boundary

This layer does not claim that the three generations have been fully derived.

This layer does claim that the derivation now has a concrete non-mass action-kernel candidate that can be tested in the next stage against the Euler--Berry mass functional.

## Next required stage

The next stage must connect this action kernel to the full fermion vector.

That means combining:

- the representation vector;
- the chiral transition vector;
- the generation seed action;
- the Poincare geometric path;
- the zeta-tetrahedral spectral layer;
- the Euler--Berry coherence term.

Only after that should observed masses be used as validation targets.
