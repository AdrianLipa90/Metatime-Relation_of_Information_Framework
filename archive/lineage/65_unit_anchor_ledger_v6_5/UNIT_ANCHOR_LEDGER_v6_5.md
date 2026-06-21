# v6.5 — Unit Anchor Ledger

Generated: `2026-06-21T16:56:14.364990+00:00`

## Verdict

- technical: PASS
- DEBT-006: CLOSED_AS_LEDGER / ENFORCEMENT_ACTIVE
- spectrum closure: NOT CLAIMED
- CURRENT promotion: DENY_CURRENT

## Global rule

Measured masses and benchmark tables are not derivation inputs. They are scoring surfaces only after formula fingerprint freeze.

## Anchor status table

| id | name | role | status | input before freeze | scoring after freeze |
|---|---|---|---|---:|---:|
| ANCHOR-001 | electron mass as normalization anchor | mass_anchor | FORBIDDEN_INPUT_FOR_DERIVATION | False | True |
| ANCHOR-002 | muon and tau measured masses | benchmark_table | SCORING_ONLY_AFTER_FREEZE | False | True |
| ANCHOR-003 | proton mass as hadron scale denominator | ratio_denominator | SCORING_ONLY_AFTER_FREEZE | False | True |
| ANCHOR-004 | u-quark and c-quark inherited anchors | mass_anchor | FORBIDDEN_INPUT_FOR_DERIVATION | False | True |
| ANCHOR-005 | Planck energy E0 from accepted dimensional constants | dimensional_normalizer | ALLOWED_DIMENSIONAL_NORMALIZER | True | True |
| ANCHOR-006 | Landauer scale kBT ln2 and Schumann quantum h f0 | dimensional_normalizer | ALLOWED_DIMENSIONAL_NORMALIZER | True | True |
| ANCHOR-007 | F_hadron / exact hadron scale candidates | calibration_scale | QUARANTINED | False | False |
| ANCHOR-008 | PDG / measured particle tables | benchmark_table | SCORING_ONLY_AFTER_FREEZE | False | True |
| ANCHOR-009 | v6.1 information-action target ledger generated from measured masses | target_ledger | SCORING_ONLY_AFTER_FREEZE | False | True |
| ANCHOR-010 | Information Operator OI = ln2/(24*pi) | operator_constant | BLOCKED_PENDING_SOURCE_INDEX | True | True |
| ANCHOR-011 | Ramanujan scaling component | operator_constant | BLOCKED_PENDING_SOURCE_INDEX | True | True |
| ANCHOR-012 | sigma(n)/R(n) prime-product hadron carrier | operator_constant | BLOCKED_PENDING_SOURCE_INDEX | True | True |

## Remaining dependent debts

- DEBT-007 absolute electron action offset S_e
- DEBT-009 hadron and meson sector split
- DEBT-011 document operator index

## Next queue

- DEBT-011 document operator index
- DEBT-007 absolute S_e derivation
- DEBT-009 hadron/meson sector split
