# METATIME SM — Debt 9 One-Anchor Rescore with Frozen Projection v3.2

**Status:** technical repo module.  
**Epistemic class:** computational stress test with anti-fit audit.  
**Observed masses used as inputs:** electron only.  
**Observed non-anchor masses:** validation targets only.  
**Old tau/eigenvalue used:** no.  
**v3.1 sector projection edited after residuals:** no.  
**Debt 9 status:** open after v3.2.

## 1. [FAKT] Purpose

v3.1 froze the sector projection operator before any renewed mass test. v3.2 performs the first one-anchor rescore using that frozen operator unchanged.

The purpose is not to close Debt 9. The purpose is to measure whether the v3.1 projection operator reduces the v2.6 numeric gap without hidden fitting.

## 2. [DEFINITION] Inputs

- `24_debt9_one_anchor_mass_scaling_v2_6/results/one_anchor_mass_scaling_predictions_v2_6.csv` using the `EB_MINUS_RAMANUJAN_ZH_CENTER` reference variant.
- `29_debt9_debt11_frozen_sector_projection_operator_v3_1/results/fermion_projected_tau_surface_v3_1.csv`.

The electron remains the only dimensional calibration mass. All other observed masses are validation-only.

## 3. [ANSATZ] Frozen orientation stress test

The v3.1 projection gives a relative projected information eigenvalue channel. v3.2 tests four predeclared orientations:

1. v2.6 reference without v3.1 projection;
2. projection as additional suppression;
3. projection as release/tunnelling;
4. absolute projection distance as suppression.

These orientations are **not** selected by residuals as canonical. They are diagnostic variants.

## 4. [WYNIK] Summary

| orientation | median_abs_log_error | max_abs_log_error | signed_mean | lepton_order | down_order | up_order |
|---|---:|---:|---:|:---:|:---:|:---:|
| `V26_REFERENCE_NO_V31_PROJECTION` | 2.628912 | 5.370477 | -2.054826 | True | True | True |
| `V31_SUPPRESSION_SIGN` | 86.521548 | 176.166577 | 29.658822 | False | False | False |
| `V31_RELEASE_SIGN` | 86.065656 | 177.657235 | -33.768474 | False | False | False |
| `V31_ABS_SUPPRESSION` | 88.565562 | 177.657235 | -92.699183 | False | False | False |

Anti-fit diagnostic best-by-median orientation: `V26_REFERENCE_NO_V31_PROJECTION`.  
Can this be claimed as derivation? **No.**  
Reason: orientation choice is not yet derived from first principles; lower residual alone would be a fit-selection signal.

## 5. [INTERPRETATION]

The frozen projection operator changes the numeric surface, but v3.2 does not close Debt 9. If a projection orientation improves residuals, it is still not canonical until the sign/orientation is derived from the underlying phase geometry rather than chosen from the validation table.

The important methodological point is that v3.2 protects the project from fitting-by-variant-selection.

## 6. [HIPOTEZA]

The remaining defect is likely not in the existence of sector projection itself. It is in the missing derivation of projection orientation: whether the sector eigenvalue acts as suppression, release, oriented phase difference, or a two-basis up/down rotation. This connects directly to the archive diagnosis that CKM needs relative phase bases, not a single scalar channel.

## 7. [VALIDATION GATE]

`COMPUTATIONAL_STRESS_TEST_PASS_WITH_ANTI_FIT_AUDIT`

## 8. [DO NOT CLAIM]

Do not claim that Debt 9 is closed.  
Do not claim charged fermion masses are derived.  
Do not canonize the best residual orientation.  
Do not claim CKM/PMNS is derived.

## 9. Files

- `scripts/one_anchor_frozen_projection_rescore_v3_2.py`
- `results/one_anchor_frozen_projection_rescore_predictions_v3_2.csv`
- `results/one_anchor_frozen_projection_rescore_summary_v3_2.csv`
- `results/one_anchor_frozen_projection_anti_fit_audit_v3_2.json`
- `schemas/ONE_ANCHOR_FROZEN_PROJECTION_RESC0RE_SCHEMA_v3_2.json`
