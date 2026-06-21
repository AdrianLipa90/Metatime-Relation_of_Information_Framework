# v6.5 — Unit Anchor Ledger

Status: VERIFIED module.

This module closes DEBT-006 as a process debt by installing an explicit hard-policy ledger for all known unit anchors, mass anchors, dimensional normalizers, scoring anchors, and quarantined scale candidates.

It does **not** close Debt 9, derive S_e, derive hadron scale, or promote CURRENT.

## Installed rule

No measured mass, PDG/exact table, inherited quark value, proton denominator, or inverse target ledger may be used as a derivation input before formula fingerprint freeze.

Allowed dimensional normalizers such as Planck E0, Landauer scale, and Schumann quantum are dimensional carriers only. They do not prove spectrum closure without independently derived dimensionless information action.

## Outputs

- `results/UNIT_ANCHOR_LEDGER_v6_5.json`
- `results/UNIT_ANCHOR_LEDGER_v6_5.csv`
- `results/VALIDATION_MODULE65_v6_5.json`
- `data/MASTER_DEBT_REGISTER_DELTA_v6_5.json`
- `scripts/validate_v6_5_unit_anchor_ledger.py`
