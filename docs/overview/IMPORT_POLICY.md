# Import Policy

This repository is imported from the verified internal bundle
`v6.9 — Sealed Charged-Lepton Reconstruction Benchmark`.

## Rules

1. Remove technical build noise only:
   - `__pycache__/`
   - `*.pyc`
   - LaTeX build artifacts such as `*.aux`, `*.log`, `*.out`, `*.toc`,
     `*.fls`, `*.fdb_latexmk`, `*.synctex.gz`
2. Do not remove alternative document representations without an explicit
   source-to-derivative map.
3. Preserve validation material in a separate public layer.
4. Record every moved or dropped file in `CLEAN_IMPORT_MANIFEST.json`.

## Document classes

- `source` — primary source such as `.tex`
- `rendered-output` — publication or compiled output such as `.pdf`
- `explanatory-doc` — repository guidance, reports, or notes such as `.md`
- `validation-report` — validation output and audit notes
- `archive-record` — lineage-preserving historical materials
