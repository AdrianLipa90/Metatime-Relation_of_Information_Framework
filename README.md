# Metatime-Relation_of_Information_Framework

This repository contains an active research framework with open validation debts.
It is not presented as a closed final proof.

The current public import is based on the verified internal line
`v6.9 — Sealed Charged-Lepton Reconstruction Benchmark`.

## Repository layout

- `core/` — executable code, scripts, configs, and minimal imported data.
- `docs/` — overview, framework-facing documents, publications, and figures.
- `theory/` — formal theory materials and foundational notes.
- `archive/lineage/` — numbered lineage modules and frozen stages.
- `validation/` — manifests, reports, provenance, and debt register records.
- `tools/` — import, cleanup, audit, and validator helpers.

## Import policy

- Technical build noise is removed.
- Alternative document representations are preserved unless there is an explicit
  source-to-derivative mapping.
- Validation material is retained as a first-class public layer.
- Every dropped file must have a documented reason in
  `CLEAN_IMPORT_MANIFEST.json`.

See [docs/overview/IMPORT_POLICY.md](docs/overview/IMPORT_POLICY.md) for the
working import rules.
