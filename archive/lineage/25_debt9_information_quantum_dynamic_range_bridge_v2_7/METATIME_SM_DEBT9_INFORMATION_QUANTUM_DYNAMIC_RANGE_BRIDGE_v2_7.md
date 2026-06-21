# METATIME SM — Debt 9 Information-Quantum Dynamic-Range Bridge v2.7

## Status

- **Module type:** audit bridge / dynamic-range diagnosis / old-source quarantine.
- **Debt:** Debt 9 — one-anchor mass scaling and missing dynamic range.
- **Canonical status:** **not closed**. This module does not derive numerical masses.
- **Gate type:** `AUDIT_BRIDGE_PASS`, not `NUMERIC_MASS_DERIVATION_PASS`.
- **Observed masses used as model inputs:** exactly one anchor inherited from v2.6: electron.
- **Old tau/eigenvalue table used as model input:** false.
- **Information operator status:** `ln(2)/(24*pi)` is treated as the quantum of informational preference fluctuation.

## Executive result

The user correction is now explicit: the information operator is not merely a small coefficient. It is the elementary quantum of preference-fluctuation used to count action differences in the exponent.

The old Metatime solver contains a `tau` / eigenvalue table with much larger dynamic range than the current v2.6 action. That is useful, but it is not clean enough to import as canon because the old table is colocated with observed masses and several fitting routines.

Therefore v2.7 creates a bridge:

1. keep the v2.6 one-anchor policy;
2. treat the information operator as the preference fluctuation quantum;
3. measure how many information-preference quanta are still missing for each non-anchor mass;
4. audit the old `tau`/eigenvalue table as a candidate dynamic-range layer;
5. quarantine old `tau` until it is re-derived from v2.x primitives.

## [DEFINITION] Informational preference quantum

Let the information operator scale be

```text
kappa_I = ln(2)/(24*pi)
```

In v2.7 this is not only a coefficient. It is the unit quantum of informational preference fluctuation. Equivalently, when the mass map uses an exponential action form, an action difference divided by `kappa_I` is counted in preference-fluctuation quanta.

## [INTERPRETATION] Relation to the old solver

The old monolithic solver used a literal information operator value near `0.009`. The exact v2.x value is `ln(2)/(24*pi)`, which is close but not identical.

Computed comparison:

- exact v2.x value: `0.009193150006360`
- old literal value: `0.009000000000000`
- old/exact ratio: `0.978990`
- relative difference: `0.021010`

This supports using the old solver as a historical source for the information-operator role, but the exact v2.x operator replaces the old literal numeric approximation.

## [AUDIT] Old tau/eigenvalue dynamic range

The old solver assigns `tau` values across charged fermions. The range is large:

- old tau dynamic range: `2000.000000`
- old tau log dynamic range: `7.600902`
- target charged-fermion log dynamic range, validation only: `12.730641`
- v2.6 predicted log dynamic range: `7.361057`

This confirms the earlier diagnosis: v2.6 preserves order but lacks dynamic range. The old tau/eigenvalue layer has the right kind of range to investigate.

## [HIPOTEZA] Missing layer

The missing dynamic range may be an informational-preference eigenvalue layer. It should not be imported from the old `tau` table as-is. It should be reconstructed from:

1. the Debt 1 Killing generator;
2. the Euler-identity/Berry spin constraint;
3. the Collatz transition axis `4 -> 2 -> 1 -> 1/2`;
4. the zeta imaginary axis;
5. Ramanujan scaling;
6. zeta-Heisenberg fluctuation width;
7. the information operator as the quantum of preference fluctuation.

## [VALIDATION RESULT]

The bridge computes the required missing release, in preference-quanta, between the v2.6 predictions and validation targets. It also compares that requirement with the old tau/eigenvalue table.

Important result:

- median required release for non-anchor masses, in log/preference-quanta units: `2.628912`
- median residual if raw old tau is used as bridge, validation only: `2.647330`
- correlation between old tau relative logs and required release, non-anchor: `0.878982`

Raw old tau is therefore **not** a solved mass layer. It is a useful candidate surface, but it must be re-derived.

## [DO NOT CLAIM]

Do not claim:

- that Debt 9 is closed;
- that old tau values are now canonical;
- that charged-fermion masses are numerically derived;
- that the old monolithic solver is clean proof;
- that the information operator has been fitted to masses.

## [NEXT REQUIRED STEP]

Create the clean v2.x replacement for old `tau`:

```text
informational eigenvalue tau_v2 = function(CP1 axis, Killing flow, Collatz transition, zeta axis, Ramanujan scale, zeta-Heisenberg fluctuation)
```

Only after that can the one-anchor mass test be rerun without importing old fitted tables.

## Files

- `scripts/information_quantum_dynamic_range_bridge_v2_7.py`
- `results/old_tau_eigenvalue_bridge_audit_v2_7.csv`
- `results/information_quantum_dynamic_range_summary_v2_7.csv`
- `results/information_quantum_dynamic_range_summary_v2_7.json`
- `schemas/INFO_QUANTUM_DYNAMIC_RANGE_SCHEMA_v2_7.json`
