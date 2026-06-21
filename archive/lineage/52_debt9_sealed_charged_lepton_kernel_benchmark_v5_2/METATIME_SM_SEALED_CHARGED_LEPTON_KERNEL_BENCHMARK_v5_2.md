# METATIME SM v5.2 — Sealed Charged-Lepton Kernel Benchmark

## Purpose

v5.1 produced a candidate White-Thread quadratic root-relative amplitude map. v5.2 freezes that candidate into a single charged-lepton benchmark pass. The formula is not adjusted after scoring.

## Frozen formula

- electron: inherited unit baseline from v4.7/v4.8;
- muon: baseline multiplied by the v5.1 root screening gate and the existing half-action tau gate;
- tau: baseline divided by the v5.1 root release gate and multiplied by the existing half-action tau gate.

Sealed formula fingerprint:

```text
cc635e803222fddac5a121398e055d91740f2e6c118aa9c5e6887f6e66ced1e9
```

## Result

- technical: PASS
- formal: PASS_SEALED_FORMULA_WITH_EXPLICIT_BOUNDARIES
- substantive: PARTIAL_IMPROVEMENT_FAIL_AS_DEBT9_NUMERIC_CLOSURE
- Debt 9 numeric spectrum: OPEN_NOT_CLOSED
- canon/current: DENIED

## Benchmark rows

| slot | predicted MeV | benchmark MeV | ratio | absolute relative error |
|---|---:|---:|---:|---:|
| e | 0.51099895 | 0.51099895 | 1 | 0 |
| mu | 204.346792755 | 105.6583755 | 1.93403307393 | 0.934033073931 |
| tau | 2750.35600852 | 1776.86 | 1.54787434492 | 0.547874344922 |

## Metrics

- mean absolute relative error excluding electron anchor: `0.740953709426497`
- median absolute relative error excluding electron anchor: `0.740953709426497`
- max absolute relative error excluding electron anchor: `0.9340330739314846`

## Interpretation

The v5.1 root gates improve the v4.8 document-F diagnostic slightly, but the muon and tau errors remain order-one. The branch is promising as a screen/release mechanism, not as a completed mass-spectrum derivation.

The electron unit remains inherited from an earlier unit anchor, so this is not a no-parameter closure even if the heavy rows had been better.

## Decision

Debt 9 remains open. The next step must not tune this same formula after seeing residuals. It should either derive the missing generational exponent/normalization from existing structures or mark this branch insufficient.
