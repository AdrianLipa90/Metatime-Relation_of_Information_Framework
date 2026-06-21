# METATIME SM — Repair 1 from v3.6: Archive Formula Formalization

Created UTC: 2026-06-20T09:22:58Z  
Base: `METATIME_STANDARD_MODEL_DERIVATION_MERGED_REPO_v3_6_NO_NESTED_ZIPS.zip`  
Repo relation: append-only repair from v3.6  
NOEMA SoT: unavailable  
Purpose: return to v3.6 and formalize use of archive formulas correctly  

---

## 0. Status

```text
technical: PASS
formal: PASS
substantive: PARTIAL — this is a repair/formalization, not final proof of emergence
numeric: uses prior archive execution tables as source material; no new mass fitting
provenance: REPO_INTERNAL repair + USER_ARCHIVE_FORMULAS + prior execution tables as external source inputs
red_alert: true — do not call all archive reconstruction pure emergence
```

---

## 1. Correction

The previous path created an artificial obstruction by treating “old archive formulas” as suspicious merely because they were old.

That is wrong.

They are user-owned working formulas and must be used.

The correct requirement is not “old vs new”. The correct requirement is:

```text
formula used -> numerical result -> dependency class -> provenance status
```

The archive formula can be executed. The dependency ledger says what kind of result it is.

---

## 2. What is fixed here

### [FIX]

Archive formulas are accepted as valid working source material.

### [FIX]

The repair does not continue from v3.9 as a conceptual base. It returns to v3.6 and adds a repair layer.

### [FIX]

The repair separates four things:

1. formula execution,
2. table/reference reconstruction,
3. calibration/dependency status,
4. clean-emergence proof.

### [FIX]

The repair does not use “fit-risk” as a refusal to calculate.

It uses dependency status as metadata.

---

## 3. Dependency statuses

The ledger uses these categories:

### copied_reference_or_canonical_table

A mass value is reproduced from a canonical/archive spectrum table.

Useful as reference, not proof of derivation by itself.

### archive_formula_execution_with_dependency_audit_required

A formula/solver from the archive gives a number, but its internal dependency chain must be audited before calling it clean-emergent.

This is allowed as calculation.

### calibrated_once_or_sector_anchor

A formula uses a declared anchor or sector calibration.

This may be valid if the calibration rule is part of the theory, but it must not be mislabeled as anchor-free emergence.

### raw_formula_stress_test

A simplified or raw formula is tested to see what it misses.

Failure here is diagnostic, not global theory failure.

---

## 4. Core principle

The archive formulas are not rejected.

They are used.

The only forbidden move is to collapse all outputs into one label such as “emergent” or “arbitrary”.

Each output gets a dependency status.

---

## 5. Files added

- `results/mass_formula_dependency_ledger_v3_6_repair1.csv`
- `results/archive_formula_formalization_repair1.json`
- `results/repair1_validation_status.json`
- `scripts/validate_repair1_formalization.py`
- copied external source tables under `external_archive_execution_sources/`

---

## 6. Next correct step

The next step is not another philosophical discussion.

The next step is formula-by-formula extraction from the archive documents:

```text
source formula -> variables -> dependencies -> computation -> mass result
```

Then each formula is marked as:

```text
emergent_candidate
calibrated_once
sector_calibrated
reference_reconstruction
fit_dependent
unknown_dependency
```

This keeps calculation moving without pretending that every result has the same epistemic status.
