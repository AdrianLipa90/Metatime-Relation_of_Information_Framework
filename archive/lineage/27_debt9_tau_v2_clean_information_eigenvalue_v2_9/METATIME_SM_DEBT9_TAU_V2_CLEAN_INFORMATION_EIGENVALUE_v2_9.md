# METATIME SM — Debt 9 Clean `tau_v2` Information-Eigenvalue Layer v2.9

## Status

- **Module type:** structural derivation candidate / pre-mass-rescoring frozen layer.
- **Debt:** Debt 9 — missing dynamic range after one-anchor scaling.
- **Canonical status:** **tau_v2 frozen as a structural ansatz; no numerical mass claim**.
- **Gate type:** `PRE_MASS_RESCORING_STRUCTURAL_PASS`.
- **Observed masses used:** false.
- **Old tau/eigenvalue table used:** false.
- **Purpose:** construct the next dynamic-range layer from v2.x primitives before any comparison to non-anchor masses.

## [FAKT] Why this module exists

v2.6 showed that one-anchor mass scaling with the existing action has a large numerical gap. v2.7 identified the old Metatime `tau/eigenvalue` layer as a useful historical bridge, but not clean enough to import. v2.8 installed a no-hidden-fit guard.

Therefore v2.9 performs only the allowed next step: derive a clean structural `tau_v2` table from the v2.x primitive stack, freeze it, and explicitly postpone mass re-scoring.

## [DEFINITION] Information operator

The information operator is `ln(2)/(24*pi)`. In this module it is the quantum of informational-preference fluctuation. It is not a fitted coefficient and it is not rescaled to reduce mass residuals.

## [ANSATZ] `tau_v2`

`tau_v2` is defined as an informational-preference eigenvalue assembled from mass-blind components: Killing / Euler--Berry, Ramanujan entropy, Ramanujan resonance release, Collatz terminal axis, zeta spacing, zeta--Heisenberg width, and representation component.

All component weights are frozen before mass re-scoring. This module does not inspect observed non-anchor masses.

## [LEMMA] No old tau promotion

The old `tau/eigenvalue` layer is not used as a formula input. It remains a quarantined historical bridge. The v2.9 table is computed from current structural artifacts only.

## [PROOF / VALIDATION]

The validation script reads only structural v2.x artifacts:

- Euler--Berry action table v1.6;
- zeta--Heisenberg seed diagnostics v2.0;
- Ramanujan seed suppression table v2.1;
- structural class/generation labels already present in the action table.

It does not read the mass validation target CSV. It does not read the old tau table. It writes a frozen `tau_v2` table and summary.

## [WYNIK]

- Gate: `PRE_MASS_RESCORING_STRUCTURAL_PASS`.
- Debt 9 status: `dynamic_range_layer_frozen_but_not_mass_validated`.
- Information quantum: `0.009193150006360`.
- `tau_v2` dynamic range in preference quanta: `160.245827`.
- Formula frozen before mass re-scoring: `True`.
- Observed masses used: `False`.
- Old tau used: `False`.

## [INTERPRETATION]

This module creates the clean replacement surface that v2.7 asked for. It does **not** yet test whether the surface fixes the charged-fermion mass gap. That must be done in a later module without changing the `tau_v2` formula.

## [VALIDATION GATE]

This module passes as a pre-mass structural gate because it creates a `tau_v2` table from v2.x primitives, treats the information operator as a fluctuation quantum, does not use observed masses, does not import old tau, and freezes the formula before the next mass test.

## [DO NOT CLAIM]

Do not claim Debt 9 is numerically closed, charged-fermion masses are derived, `tau_v2` is validated against observed masses, the old tau table has been promoted, or the dynamic range layer is final.

## [NEXT REQUIRED STEP]

The next allowed step is a new one-anchor mass-rescoring module that uses this frozen `tau_v2` table unchanged. If the formula is edited after seeing mass residuals, that must be marked as a fit attempt, not a derivation.

## Files

- `scripts/tau_v2_structural_information_eigenvalue_v2_9.py`
- `results/tau_v2_structural_information_eigenvalue_table_v2_9.csv`
- `results/tau_v2_structural_information_eigenvalue_summary_v2_9.json`
- `results/tau_v2_structural_information_eigenvalue_summary_v2_9.csv`
- `schemas/TAU_V2_STRUCTURAL_INFORMATION_EIGENVALUE_SCHEMA_v2_9.json`
