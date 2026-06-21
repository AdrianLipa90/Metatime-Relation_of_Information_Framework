# METATIME SM — Repair3 Forensic PDG Reimport Quarantine v3.7

Created UTC: 2026-06-20T12:36:05Z  
Base: `METATIME_STANDARD_MODEL_DERIVATION_MERGED_REPO_v3_6_REPAIR2_NO_NESTED_ZIPS`  
NOEMA SoT: unavailable; artifact-grounded audit only.  

## Status

```text
technical: PASS — files were unpacked and checked
formal: PASS — evidence is path/line anchored
substantive: FAIL / REGRESSION — v3.6 Repair2 reimports reference-dependent mass sources
Debt 9: OPEN_NOT_CLOSED
canon_allowed: false
CURRENT promotion: DENY_CURRENT
Doctor verdict: QUARANTINE_MODULE36_DENY_CANON_DENY_CURRENT
```

## Executive verdict

Repair2 module 36 is not a valid Debt 9 closure. It confirms execution/provenance mechanics, but the mass numbers used for the apparent success come from two inadmissible classes:

1. `ARCHIVE_CANONICAL_SPECTRUM` is a reference table replay: all 12 rows have `mass_calc == reference` and zero residual.
2. `ARCHIVE_NOPARAMSM_ENSEMBLE` is generated from `NoParamSM/noparamSMsolver.py`, which v2.5 already classified as `prototype_with_input_leakage` because the mass engine uses PDG masses as internal reference and modulates them by `O_I` fluctuations.

The regression is procedural as well as numerical: module 36 explicitly says dependency status is reported but not used as a refusal/blocker. That contradicts the v2.8 no-hidden-fit guard and the v3.2 anti-fit discipline.

## Evidence summary

### v2.5 quarantine was explicit

- `23_old_metatime_debt9_ckm_table_mining_v2_5/METATIME_SM_OLD_DOCS_DEBT9_CKM_TABLE_AUDIT_v2_5.md`, lines 115–123: old solvers using observed masses/fits must not count as derivations; line 120 specifically names NoParamSM engines using PDG masses internally.
- `23_old_metatime_debt9_ckm_table_mining_v2_5/results/old_metatime_reference_findings_v2_5.csv`, line 6: `NoParamSM/noparamSMsolver.py` is classified as `prototype_with_input_leakage` and says not to count it as derivation.

### v2.8/v3.2 guard was explicit

- v2.8 defines hidden fit as a structurally named term selected/scaled/normalized by looking at non-anchor masses while claiming derivation.
- v3.2 keeps Debt 9 open and says not to canonize the best residual orientation.

### Repair2 neutralized the blocker

- `CURRENT_STATUS.md`, line 11: `red_alert: dependency class reported but not used as blocker`.
- module 36 ledger lines 12–19: `technical: PASS`, `formal: PASS`, and `red_alert: true — source/dependency status is reported, not used as a refusal`.
- module 36 validation script lines 14–22 sets `old_vs_new_blocker_used: False` and only checks dependency status is attached.

### Reference replay confirmed

`ARCHIVE_CANONICAL_SPECTRUM` stats:

```json
{
  "n": 12,
  "all_mass_calc_equal_reference": true,
  "equal_count": 12,
  "max_abs_relative_error": 0.0,
  "examples": [
    {
      "particle": "e",
      "mass_calc": "0.511",
      "reference": "0.511",
      "relative_error": "0.0",
      "source": "MetaTheory archive canonical spectrum table / v3.8 extraction"
    },
    {
      "particle": "mu",
      "mass_calc": "105.7",
      "reference": "105.7",
      "relative_error": "0.0",
      "source": "MetaTheory archive canonical spectrum table / v3.8 extraction"
    },
    {
      "particle": "tau",
      "mass_calc": "1776.9",
      "reference": "1776.9",
      "relative_error": "0.0",
      "source": "MetaTheory archive canonical spectrum table / v3.8 extraction"
    },
    {
      "particle": "nu1",
      "mass_calc": "0.001",
      "reference": "0.001",
      "relative_error": "0.0",
      "source": "MetaTheory archive canonical spectrum table / v3.8 extraction"
    },
    {
      "particle": "nu2",
      "mass_calc": "0.008",
      "reference": "0.008",
      "relative_error": "0.0",
      "source": "MetaTheory archive canonical spectrum table / v3.8 extraction"
    }
  ]
}
```

Representative rows from `METATIME_ARCHIVE_FORMULA_MASS_EXECUTION_v3_9.csv` show top quark `172760.0 == 172760.0`, and every canonical spectrum row behaves the same.

### PDG input confirmed in NoParamSM

`noparamSMsolver.py` contains:

- lines 42–49: `PDG = {...}` reference mass dictionary;
- lines 154–158: docstring says reference masses come from PDG and are modulated by topological factors;
- lines 167–174: `self.mass_ref = {**PDG['leptons'], **PDG['quarks']}`, then returns `m_ref * yukawa_factor(...)`.

Deterministic mutation test:

```json
{
  "modified_PDG": {
    "e": 123.456,
    "c": 9999.0,
    "t": 42.0
  },
  "outputs_after_reinstantiation_at_OI_ref": {
    "e": 123.456,
    "c": 9999.0,
    "t": 42.0
  }
}
```

At `O_I_REF`, the solver returns the PDG references exactly. If the internal PDG dictionary is mutated, the solver output follows the mutation. Therefore the mass reference is an input, not a derived output.

## Correct classification

| Source/result class | Correct classification | Canon use |
|---|---|---|
| `ARCHIVE_CANONICAL_SPECTRUM` | `REFERENCE_TABLE_REPLAY` | denied as prediction/execution |
| `ARCHIVE_NOPARAMSM_ENSEMBLE` | `PDG_REFERENCE_INPUT_LEAKAGE` | quarantined |
| `ARCHIVE_EXTENDED_MONOLITH_*` | `REFERENCE_DEPENDENCY_AUDIT_REQUIRED` | quarantined until PDG-free proof |
| module 36 status | `REGRESSION_FROM_GUARD_DISCIPLINE` | deny current/canon |

## Required repair rule

Dependency class is not metadata when it indicates reference leakage. It is a blocker.

A mass-spectrum row may be promoted only if:

1. its inputs exclude non-anchor observed masses and copied reference tables;
2. any single allowed anchor is explicitly marked as calibration, not prediction;
3. formula selection, scaling, damping, and normalization are frozen before comparison to non-anchor masses;
4. PDG/reference values appear only after execution as benchmarks;
5. a rerun with reference tables removed still produces the same dimensionless ratios.

## Decision

```text
Debt 9: OPEN_NOT_CLOSED
Module 36: QUARANTINE
Repair2 CURRENT: invalid as canonical current
Canon promotion: DENY_CANON
Current promotion: DENY_CURRENT
Next valid step: build PDG-free mass-ratio derivation from CP1 / Killing / Collatz / Ramanujan / information operator, then benchmark externally.
```
