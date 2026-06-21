# METATIME Standard Model Derivation — v6.9 Sealed Charged-Lepton Reconstruction Benchmark

Created UTC: `2026-06-21T20:22:28Z`

## Purpose

v6.9 reconstructs the charged-lepton sector through a frozen pipeline, after the earlier gates:

1. `S_e` from v6.7.
2. `R_e_mu` from the frozen v6.2 Euler-Berry/kappa release gate.
3. `R_mu_tau` from the refined v6.8 White-Thread/OI release gate.

The benchmark references measured masses only after the rules are frozen.

## Frozen pipeline

```text
S_mu = S_e - R_e_mu
S_tau = S_mu - R_mu_tau
E_i = E_P * exp(-S_i/OI)
```

## Input policy

```text
electron mass as input: false
muon mass as input: false
tau mass as input: false
PDG table as input: false
exact replay table as input: false
v6.1 target actions as input: false
```

## Results

| particle | derived action | predicted MeV | scoring reference MeV | abs rel error % |
|---|---:|---:|---:|---:|
| electron | 0.473691600121165 | 0.511642050984 | 0.510998950000 | 0.125852 |
| muon | 0.424243592804165 | 110.903254628363 | 105.658380000000 | 4.963993 |
| tau | 0.398273248953487 | 1869.871654360978 | 1776.860000000000 | 5.234608 |


## Metrics

```json
{
  "particle_count": 3,
  "mean_abs_relative_error_percent": 3.4414842288192085,
  "max_abs_relative_error_percent": 5.23460792414586,
  "electron_abs_relative_error_percent": 0.12585172327104704,
  "muon_abs_relative_error_percent": 4.963993039040719,
  "tau_abs_relative_error_percent": 5.23460792414586,
  "predicted_mu_over_e": 216.75945988991637,
  "scoring_mu_over_e": 206.76829179394596,
  "mu_over_e_relative_error_percent": 4.8320600848833495,
  "predicted_tau_over_mu": 16.8603857535734,
  "scoring_tau_over_mu": 16.817028616187375,
  "tau_over_mu_relative_error_percent": 0.2578168734534314,
  "predicted_tau_over_e": 3654.648109480211,
  "scoring_tau_over_e": 3477.228280018971,
  "tau_over_e_relative_error_percent": 5.102334824571031
}
```

## Decision

```text
technical: PASS
formal: PASS_SEALED_CHARGED_LEPTON_RECONSTRUCTION_BENCHMARK_INSTALLED
substantive: SEALED_CHARGED_LEPTON_RECONSTRUCTION_PARTIAL_PASS_E_TO_MU_RELEASE_REFINEMENT_REQUIRED
Debt 9 numeric spectrum: OPEN_NOT_CLOSED
canon_allowed: false
mass_spectrum_closure_claimed: false
```

The electron result is strong. The muon and tau errors remain dominated by the older `e→mu` release gate inherited from v6.2. The refined `mu→tau` gate remains stable in the full reconstruction.

## Required next step

```text
v7.0 — e→mu release refinement gate
```

The next gate must refine `R_e_mu` from predeclared operators, without using the muon/electron measured ratio as an input.
