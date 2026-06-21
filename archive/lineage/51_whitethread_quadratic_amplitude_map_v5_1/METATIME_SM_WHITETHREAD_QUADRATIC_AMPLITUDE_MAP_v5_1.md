# METATIME SM v5.1 — White-Thread Quadratic Amplitude Map Candidate

## Purpose

v5.0 showed that a pure short-doc phase map `W_ij = exp(i∫A)` cannot derive the strong charged-lepton screen/release factors. v5.1 tests a more explicit amplitude map built from existing project quantities rather than from observed masses.

## Candidate formula

The candidate treats White-Thread attenuation as a quadratic open-path action over the already-frozen `tau_v2` preference-quanta separation:

```text
S_ij = (Delta tau_v2 preference quanta)^2 / (2 * L3 * DeltaGeneration)
F_ij = exp(-OIB * S_ij)
OIB = ln2/(24π)
L3 = 7
```

This is a candidate Fubini-Study / diffusion-like open holonomy action. It is not a mass-spectrum solver and it is not canon.

## Result

- technical: PASS
- formal: PASS_WITH_CANDIDATE_STATUS
- substantive: PARTIAL_DERIVATION_CANDIDATE_ROOT_GATES_PASS_ALLPAIR_FAIL
- mass prediction: NOT_CLAIMED
- benchmark: NOT_PERFORMED
- Debt 9 numeric spectrum: OPEN_NOT_CLOSED
- canon/current: DENIED

## Main diagnostic

Root-relative gates are close to the large document diagnostic F targets:

- `e→mu`: derived `0.142587691698` vs diagnostic target `0.145`
- `e→tau`: derived `0.314531863377` vs diagnostic target `0.302`

But the all-pair map fails:

- `mu→tau`: derived `0.000202136408` vs diagnostic target `0.203`

## Interpretation

The candidate explains the two electron-root screen/release gates at few-percent level, but it does not derive the full all-pair F table. This points to a root-relative open-path gate, not a compositional all-pair metric.

## Boundary

This module was built after the v5.0 diagnostic target audit, so it cannot be advertised as independent confirmation. It is a candidate map to be frozen and then tested in a later sealed charged-lepton kernel pass.

## Next step

v5.2 should either:

1. freeze this root-relative quadratic map and use it in one sealed charged-lepton kernel test, or
2. reject it if the root-relative/non-compositional interpretation is unacceptable.
