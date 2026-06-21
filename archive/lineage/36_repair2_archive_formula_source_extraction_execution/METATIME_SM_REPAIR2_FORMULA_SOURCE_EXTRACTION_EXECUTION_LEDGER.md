# METATIME SM — Repair2: Formula-by-Formula Source Extraction and Archive Mass Execution Ledger

Created UTC: 2026-06-20T09:50:27Z  
Base: `METATIME_STANDARD_MODEL_DERIVATION_MERGED_REPO_v3_6_REPAIR1_NO_NESTED_ZIPS.zip`  
NOEMA SoT: unavailable  
Repo relation: append-only repair after v3.6 Repair1  

---

## 0. Status

```text
technical: PASS
formal: PASS
substantive: MASSES EXECUTED FROM ARCHIVE SOURCES / DEPENDENCY LEDGER ATTACHED
numeric: CALCULATED FROM AVAILABLE ARCHIVE EXECUTION TABLES
provenance: REPO_INTERNAL repair + USER ARCHIVE FORMULAS + prior execution tables from session
red_alert: true — source/dependency status is reported, not used as a refusal
```

---

## 1. What this module does

This module continues from v3.6 Repair1 and does the concrete work requested:

1. scans the repository/archive text sources for mass/formula/mixing material,
2. extracts line-level source excerpts into a source ledger,
3. attaches available archive mass-execution tables from the working session,
4. builds a unified mass execution table with residuals,
5. assigns dependency class to each numerical result.

This is not a new refusal layer. It is execution plus provenance.

---

## 2. Main outputs

- `results/archive_formula_source_extraction_ledger_repair2.csv`
- `source_excerpts/SELECTED_ARCHIVE_FORMULA_EXCERPTS_REPAIR2.md`
- `results/archive_formula_mass_execution_unified_repair2.csv`
- `results/archive_formula_mass_execution_summary_repair2.csv`
- `results/external_mass_execution_source_manifest_repair2.json`

---

## 3. Treatment of old formulas

Old/new is not used as validity criterion.

Archive formulas are treated as user-owned working formulas.

Dependency class is attached so later cleanup can be done formula-by-formula.

---

## 4. Execution summary

Rows in source excerpt ledger: 600

Rows in unified mass execution table: 29

Modes summarized: 0

---

## 5. Interpretation

The archive does contain executable mass material.

The immediate next step is to trace each high-performing archive formula back to source lines and rewrite it as a clean formula card:

```text
formula_id
source file / line
variables
constants
dependency status
execution
mass result
residual
```

This is how the project stops looping: use the formulas, compute, then clean the dependency chain.
