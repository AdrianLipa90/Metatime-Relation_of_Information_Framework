# Cleanup Report

Source checkpoint: `v6.9 — Sealed Charged-Lepton Reconstruction Benchmark`

## Cleanup policy applied

- removed technical build noise only
- preserved validation as a public layer
- preserved alternative document representations unless they were obvious
  technical duplicates
- recorded path moves and drops in `CLEAN_IMPORT_MANIFEST.json`

## Observed technical noise in source bundle

- `__pycache__` directories: `84`
- `*.pyc` files: `125`
- LaTeX build-noise files: `12`
- rendered assets retained in first import: `19`

## Known deliberate exclusions

- `LICENSE.txt`
  - reason: `duplicate`
- Python caches and compiled bytecode
  - reason: `build-noise`
- LaTeX auxiliary files
  - reason: `build-noise`

## Notes

The repository intentionally keeps `.tex`, `.pdf`, and `.md` side by side where
they represent source, rendered output, and explanatory context rather than
technical duplication.
