# METATIME Standard Model — v5.4 Ramanujan Component-Split Lepton Refinement

## Purpose

Debt 9 was not closed in v5.3 because the tau channel became close, but the muon remained too high. v5.4 tests whether that residual can be reduced by splitting the already-frozen `tau_v2` Ramanujan layer into its documented components rather than treating it as one fused action.

## Formula under test

For charged leptons after the electron root:

```text
C_i = exp(-R_i) * exp(OIB * L3 * E_i)
m_i(v5.4) = m_i(v5.3) * C_i
```

where `R_i` is the `ramanujan_resonance_release_component`, `E_i` is the `ramanujan_entropy_component`, `OIB = ln2/(24π)`, and `L3 = 7`.

## Source boundary

The components are taken from the frozen v2.9 `tau_v2` structural information table. No benchmark masses, PDG table, NoParamSM solver, or reference spectrum is used in the operator. Benchmark masses are used only after fingerprinting for scoring.

## Result

The refinement strongly improves the charged-lepton diagnostic, especially the muon residual, but it is still not a Debt 9 closure because it is a post-v5.3 refinement, electron remains an inherited unit anchor, and quark/full-spectrum validation is not included.

## Decision

Debt 9 numeric spectrum remains `OPEN_NOT_CLOSED`. Canon/current promotion remains denied.
