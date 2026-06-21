# METATIME v6.4 — Exact Table / Replay / PDG Provenance Matrix
Created UTC: `2026-06-21T16:50:52Z`
## Status
```text
technical: PASS
formal: PASS_PROVENANCE_MATRIX_INSTALLED
substantive: DEBT_005_CLOSED_EXACT_REPLAY_TABLES_CLASSIFIED
Debt 9 numeric spectrum: OPEN_NOT_CLOSED
canon_allowed: false
CURRENT promotion: DENY_CURRENT
```
## Purpose
This module closes DEBT-005 by assigning every known exact/replay/benchmark table a hard provenance class before any further physics work. It does not create a new mass formula. It blocks reference replay, PDG leakage, and hidden benchmark reuse.
## Allowed classes
- `SOURCE_DERIVED` — Can be used as a pre-benchmark structural source if not mass-table-derived.
- `STRUCTURAL_HINT` — May guide a future frozen operator; cannot serve as direct prediction/scale input.
- `SCORING_ONLY` — May be used only after formula freeze for scoring; forbidden as operator input.
- `TAINTED_REPLAY` — Reference/PDG/replay/input-leakage risk confirmed; quarantined from derivation.
- `UNKNOWN_PROVENANCE` — Potentially useful but blocked until executable source route is shown.

## Summary
```json
{
  "row_count": 22,
  "by_classification": {
    "TAINTED_REPLAY": 5,
    "STRUCTURAL_HINT": 4,
    "UNKNOWN_PROVENANCE": 1,
    "SCORING_ONLY": 10,
    "SOURCE_DERIVED": 2
  },
  "unclassified_rows": 0,
  "floating_rows": 0,
  "canon_allowed": false,
  "debt005_status": "CLOSED_BY_MATRIX",
  "debt9_numeric_spectrum": "OPEN_NOT_CLOSED"
}
```
## Key decisions
- `ARCHIVE_CANONICAL_SPECTRUM` is `TAINTED_REPLAY`: exact reference replay confirmed.
- `NoParamSM` and module36 monolith families are `TAINTED_REPLAY`: PDG/reference input leakage risk confirmed.
- Exact baryon table from `SM_and_M_Theory_generalisation.pdf` is not rejected for accuracy, but is `UNKNOWN_PROVENANCE` until an executable non-mass MeV-scale route is shown.
- `F_hadron`, Formal_SM binding formula, and prime-product sigma/R(n) route are preserved as structural sources/hints, not benchmark inputs.
- v4.4, v4.6, v5.2, v5.3, v5.4, v6.0A, v6.1, v6.2 result tables are `SCORING_ONLY` unless separately reclassified by a future freeze-before-benchmark gate.

## Matrix
| id | classification | name | permitted use | blocked use |
|---|---|---|---|---|
| TABLE-001 | `TAINTED_REPLAY` | ARCHIVE_CANONICAL_SPECTRUM | Quarantine evidence only; never mass derivation input; never Debt 9 closure. | No formula selection, no scale fitting, no current/canon promotion. |
| TABLE-002 | `TAINTED_REPLAY` | ARCHIVE_NOPARAMSM_ENSEMBLE / NoParamSM solver outputs | Regression test and quarantine marker only. | No predictive mass-spectrum claim; no Debt 9 closure. |
| TABLE-003 | `TAINTED_REPLAY` | ARCHIVE_EXTENDED_MONOLITH_BOSON_ENSEMBLE | Quarantine evidence; compare only after independent derivation is supplied. | No direct derivation, no canon/current promotion. |
| TABLE-004 | `TAINTED_REPLAY` | ARCHIVE_EXTENDED_MONOLITH_NUCLEON_ENSEMBLE | Quarantine evidence; compare only after independent derivation is supplied. | No direct derivation, no canon/current promotion. |
| TABLE-005 | `TAINTED_REPLAY` | ARCHIVE_EXTENDED_MONOLITH_BINDING_ENSEMBLE | Quarantine evidence; compare only after independent derivation is supplied. | No direct derivation, no canon/current promotion. |
| TABLE-006 | `STRUCTURAL_HINT` | F_hadron geometric mean prescription | Can seed future operator family after freeze; no MeV scale input. | No mass prediction or Debt 9 closure until independent route is frozen and benchmarked. |
| TABLE-007 | `UNKNOWN_PROVENANCE` | SM_and_M_Theory exact baryon table | Hold as provenance-required result table only; exact equality is not rejected, but cannot promote without executable scale route. | No mass prediction or Debt 9 closure until independent route is frozen and benchmarked. |
| TABLE-008 | `STRUCTURAL_HINT` | Formal_SM baryon binding formula | Formula/operator clue only; E_bind needs independent derivation. | No mass prediction or Debt 9 closure until independent route is frozen and benchmarked. |
| TABLE-009 | `SCORING_ONLY` | Formal_SM mixed baryon binding table | Diagnostic residual table only; mixed accuracy blocks universal closure. | No mass prediction or Debt 9 closure until independent route is frozen and benchmarked. |
| TABLE-010 | `SCORING_ONLY` | Calabi_Yau2 calibrated baryon table/warning | Calibration/iteration evidence; useful warning against underbound scale, not derivation. | No mass prediction or Debt 9 closure until independent route is frozen and benchmarked. |
| TABLE-011 | `STRUCTURAL_HINT` | Perfect numbers prime-product sigma/R(n) baryon route | Clean route candidate for v5.9-like operator; not a benchmark table input. | No mass prediction or Debt 9 closure until independent route is frozen and benchmarked. |
| TABLE-012 | `SCORING_ONLY` | v4.4 sealed M_MT benchmark | Scoring-only after freeze; regression tests; historical evidence. | No operator construction or scale normalization from this table unless explicitly reclassified in a future provenance audit. |
| TABLE-013 | `SCORING_ONLY` | v4.6 document formula selection benchmark | Scoring-only after freeze; regression tests; historical evidence. | No operator construction or scale normalization from this table unless explicitly reclassified in a future provenance audit. |
| TABLE-014 | `SCORING_ONLY` | v5.2 sealed charged-lepton kernel benchmark | Scoring-only after freeze; regression tests; historical evidence. | No operator construction or scale normalization from this table unless explicitly reclassified in a future provenance audit. |
| TABLE-015 | `SCORING_ONLY` | v5.3 Ramanujan/OI lepton normalizer benchmark table | Scoring-only after freeze; regression tests; historical evidence. | No operator construction or scale normalization from this table unless explicitly reclassified in a future provenance audit. |
| TABLE-016 | `SCORING_ONLY` | v5.4 Ramanujan component-split lepton refinement table | Scoring-only after freeze; regression tests; historical evidence. | No operator construction or scale normalization from this table unless explicitly reclassified in a future provenance audit. |
| TABLE-017 | `SCORING_ONLY` | v6.0A hadron ratio benchmark table | Scoring-only after freeze; regression tests; historical evidence. | No operator construction or scale normalization from this table unless explicitly reclassified in a future provenance audit. |
| TABLE-018 | `SCORING_ONLY` | v6.1 Planck information-action target ledger | Scoring-only after freeze; regression tests; historical evidence. | No operator construction or scale normalization from this table unless explicitly reclassified in a future provenance audit. |
| TABLE-019 | `SCORING_ONLY` | v6.2 lepton information-action release scoring | Scoring-only after freeze; regression tests; historical evidence. | No operator construction or scale normalization from this table unless explicitly reclassified in a future provenance audit. |
| TABLE-020 | `SOURCE_DERIVED` | v3.8 PDG-free structural signature | Structural operator/source ingredient only under freeze-before-benchmark rule. | No hidden mass-scale calibration; no direct Debt 9 closure. |
| TABLE-021 | `SOURCE_DERIVED` | v5.9 prime-product hadron carrier candidate | Structural operator/source ingredient only under freeze-before-benchmark rule. | No hidden mass-scale calibration; no direct Debt 9 closure. |
| TABLE-022 | `STRUCTURAL_HINT` | v6.0B information-energy normalizer formula ledger | Structural operator/source ingredient only under freeze-before-benchmark rule. | No hidden mass-scale calibration; no direct Debt 9 closure. |

## Closure effect
`DEBT-005` is closed by explicit matrix coverage. `DEBT-006` becomes next active debt: unit-anchor ledger. `DEBT-009` remains blocked until anchor and sector gates are complete.
