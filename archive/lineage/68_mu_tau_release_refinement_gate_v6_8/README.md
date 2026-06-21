# v6.8 — μ→τ Release Refinement Gate

Created: 2026-06-21T17:51:00+00:00

## Purpose

Refine the charged-lepton `μ→τ` information-action release without using the muon mass, tau mass, PDG table, exact replay table, or v6.1 action targets as derivation inputs.

This module follows the debt invariant introduced in v6.3: no floating debt, no hidden benchmark input, no canon promotion.

## Frozen non-mass candidate

```text
R_mu_tau = 3*OI - OI/L3 - (L3/2)*OI^2
```

Term interpretation:

- `3*OI` — three preference quanta for the second charged-lepton release layer.
- `OI/L3` — `L3 = 7` return/channel subtraction.
- `(L3/2)*OI^2` — spin-half weighted `L3` quadratic White Thread correction.

## Numeric result

```text
OI = 0.009193150006360484
L3 = 7.0
R_mu_tau(derived) = 0.025970343850677605
predicted tau/muon ratio = 16.860385753573
```

## Scoring-only comparison

The following values are forbidden as formula inputs and appear only after the formula is frozen.

```text
target tau/muon ratio = 16.817028616187
energy-ratio relative error = 0.257817%
action relative error = 0.091229%
```

## Status boundary

```text
technical: PASS
formal: PASS_MU_TAU_RELEASE_REFINEMENT_GATE_INSTALLED
substantive: MU_TAU_RELEASE_REFINED_DERIVATION_GATE_PASS_NOT_CANON
canon_allowed: false
mass_spectrum_closure_claimed: false
```

This closes the `μ→τ` release debt as a derivation-gate artifact, not as full charged-lepton spectrum closure.
