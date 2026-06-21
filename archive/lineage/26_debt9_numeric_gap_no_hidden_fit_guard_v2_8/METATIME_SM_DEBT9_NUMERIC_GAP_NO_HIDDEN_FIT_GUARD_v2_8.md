# METATIME SM — Debt 9 Numeric Gap and No-Hidden-Fit Guard v2.8

## Status

- **Module type:** methodological guard / numerical-gap ledger.
- **Debt:** Debt 9 — mass-ratio derivation; Debt 11 dependency remains active.
- **Canonical status:** **guard installed; no numerical mass derivation claim**.
- **Gate type:** `METHODOLOGICAL_GUARD_PASS`.
- **Observed mass inputs:** still exactly one anchor mass, the electron.
- **Non-anchor masses:** validation targets only.
- **Purpose:** prevent a post-hoc dynamic-range correction from becoming a hidden fit.

## [FAKT] Current v2.6 one-anchor result

The best v2.6 variant is `EB_MINUS_RAMANUJAN_ZH_CENTER`.

It has median absolute log-error `2.628912` and maximum absolute log-error `5.370477` across non-anchor charged fermions.

In ordinary factor language this is roughly a median factor error of `13.859` and a maximum factor error of `214.965`.

This is a real numerical gap. It is not a cosmetic residual.

## [WYNIK] Why this module exists

v2.7 found that the old Metatime `tau/eigenvalue` layer has the kind of dynamic range that v2.6 lacks. However, the old source sits too close to mass tables, fits, and historical prototypes. Therefore it cannot be promoted directly.

The correct next move is not to tune a new term until the gap disappears. The correct next move is to derive a clean `tau_v2` or information-eigenvalue layer from v2.x primitives before re-scoring the masses.

## [DEFINITION] Hidden-fit risk

A hidden fit is any new term that appears structurally named but is selected, scaled, widened, or normalized by looking at non-anchor masses while still claiming a derivation.

This includes:

1. adding a second mass anchor while calling the result one-anchor;
2. choosing a Ramanujan factor by minimizing mass error;
3. widening zeta-Heisenberg uncertainty until targets are covered;
4. importing the old `tau/eigenvalue` table without re-derivation;
5. changing representation weights after inspecting the mass residuals.

## [DEFINITION] Information operator as fluctuation quantum

The information operator is not merely a numerical weight. In this layer it is the quantum of informational-preference fluctuation. It may scale allowed preference fluctuations, but it may not be freely rescaled to repair a mass error.

## [ANSATZ] Allowed next dynamic-range layer

The allowed next layer is a clean `tau_v2` / information-eigenvalue construction derived from:

1. CP1 / Bloch axis;
2. Killing generator;
3. Euler-Berry spin closure;
4. Collatz transition axis;
5. zeta imaginary axis;
6. Ramanujan modular/asymptotic scaling;
7. information quantum of preference fluctuation.

It must be frozen before comparing against non-anchor masses.

## [VALIDATION GATE]

This module passes because it:

- reads the v2.6 one-anchor result;
- records the numerical gap explicitly;
- blocks a Debt 9 numerical-closure claim;
- preserves the one-anchor rule;
- records old `tau/eigenvalue` as a quarantined bridge, not a result;
- adds an explicit anti-fit policy before any next mass attempt.

## [DO NOT CLAIM]

Do not claim:

- that Debt 9 is numerically closed;
- that the old `tau/eigenvalue` layer has been promoted;
- that the mass gap is solved;
- that zeta-Heisenberg width can be tuned to cover targets;
- that the information operator is a free adjustable coefficient.

## Files

- `scripts/no_hidden_fit_guard_v2_8.py`
- `results/debt9_numeric_gap_no_hidden_fit_guard_v2_8.json`
- `results/debt9_numeric_gap_summary_v2_8.csv`
- `results/no_hidden_fit_guard_run_v2_8.json`
- `schemas/NO_HIDDEN_FIT_GUARD_SCHEMA_v2_8.json`
