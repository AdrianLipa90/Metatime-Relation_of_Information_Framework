# AGENT6 — File Placement Audit

Date: 2026-03-25  
Repository: `AdrianLipa90/Metatime`  
Branch: `Agent6`

## Purpose
This report classifies the visible repository material by functional role and identifies where the current layout mixes layers that should be separated.

---

## 1. Root-level audit

### `README.md`
**Classification:** theory summary / public-facing framework overview  
**Assessment:** useful entry point, but not suitable as the single live source-of-truth for derivations.  
**Recommended status:** `summary_reference`, not `canonical_derivation`.

### `MetaTheory_260218_073120.txt`
**Classification:** manuscript-scale theory draft  
**Assessment:** strongest candidate for current live theory core, but still a draft-like object rather than a fully indexed derivation tree.  
**Recommended status:** `proto-canon`, pending canonical source selection.

### `Metatime framework summary.pdf`
**Classification:** generated or presentation-level summary artifact  
**Assessment:** useful reference, not stronger than live text/source files.  
**Recommended status:** `reference_pdf`.

### `cielnofft.py`
**Classification:** runtime or exploratory executable object  
**Assessment:** too high-level and too broad to be treated as foundational canon.  
**Recommended status:** `executable_exploratory`.

### `file_0000000074ac720aa48d13b55bb80b5c.png`
**Classification:** loose artifact / image  
**Assessment:** should not sit at root without explanation.  
**Recommended status:** move to `references/figures/` or `archive/` with context.

---

## 2. Top-level directory audit

### `documents/`
**Observed content:** mostly PDFs, at least one short `Docs.md`, mixed theoretical and phenomenological whitepaper-style artifacts.  
**Classification:** reference / archive / whitepaper layer  
**Assessment:** this directory is high-value, but currently too mixed to act as canon.  
**Recommendation:** split conceptually into:
- foundational whitepapers,
- sector whitepapers,
- archive / superseded PDFs.

### `simulations/`
**Observed content:** `Metatime_Framework(1).py`, `Standard Model/`, `PBH/`, `Toy-Model White-Thread Matrix F_ij — Next Steps/`.  
**Classification:** simulation and exploratory executable layer  
**Assessment:** this is not foundational canon. It contains strong exploratory downstream content.  
**Recommendation:** treat as `simulation/experiments`, not derivation source.

### `data/`
**Observed content:** FITS maps, CSVs, PNGs, an ipynb, interpretation markdowns, dated result directories.  
**Classification:** generated data / results / observational inputs  
**Assessment:** this folder is correct in spirit but mixes raw data and generated results too closely.  
**Recommendation:** split conceptually into:
- `inputs/` raw external datasets,
- `results/` generated outputs,
- `notebooks/` exploratory notebooks.

### `NoParamSM/`
**Observed content:** solver scripts and result files (`.txt`, `.json`).  
**Classification:** sector solver / executable realization / phenomenology-facing numerics  
**Assessment:** useful, but downstream of foundational canon.  
**Recommendation:** treat as a sector-implementation package, not as derivation source.

### `ResChem/`
**Observed content:** one PDF and one solver.  
**Classification:** cross-domain exploratory branch  
**Assessment:** semantically separate from the minimal Metatime derivation spine.  
**Recommendation:** mark explicitly as exploratory extension or keep isolated from canonical derivation chain.

---

## 3. Specific mixed-layer issues

### Issue A — theory and summary live too close together
The root currently contains both:
- broad theory-entry summaries,
- a manuscript-scale draft,
- executable code,
- a loose image artifact.

This makes root-level meaning unstable.

### Issue B — `documents/` is overloaded
The folder contains:
- likely important foundational whitepapers,
- sector PDFs,
- cosmology PDFs,
- Standard Model PDFs,
- cross-domain and hardware-related documents,
- miscellaneous markdown.

This should not be treated as one semantic bucket.

### Issue C — simulation content is semantically downstream but visually prominent
The `simulations/` layer contains advanced exploratory material that can easily be mistaken for derivation source.

### Issue D — result files sit near model logic
`NoParamSM/` stores solver code and result files together. That is practical, but weak for long-term canonical hygiene.

---

## 4. AGENT6 classification table

| Path / object | Working classification | Canonical weight | AGENT6 note |
|---|---|---:|---|
| `README.md` | summary_reference | medium | keep as overview, not derivation root |
| `MetaTheory_260218_073120.txt` | proto-canon | high | strongest current live theory candidate |
| `Metatime framework summary.pdf` | reference_pdf | medium | secondary to live text/source |
| `cielnofft.py` | executable_exploratory | low-foundational / medium-exploratory | not a primitive derivation file |
| `documents/` | references_whitepapers_archive | medium-high | must be internally stratified |
| `simulations/` | simulation_experiments | medium | downstream of canon |
| `data/` | inputs_results_mixed | medium | split raw vs generated conceptually |
| `NoParamSM/` | sector_solver_layer | medium | sector implementation, not source-of-truth |
| `ResChem/` | exploratory_extension | low-foundational | keep isolated from derivation spine |

---

## 5. Immediate file-organization priorities

### Priority A — select the live canonical theory source
A decision is needed on which file currently acts as strongest derivation root.
At the moment the best candidate is:
- `MetaTheory_260218_073120.txt`

but it still needs structured indexing and dependency binding.

### Priority B — explicitly demote summaries and PDFs to secondary status
The following should be treated as non-primary until canon is frozen:
- summary PDFs,
- downstream simulation outputs,
- broad sector solver results.

### Priority C — separate raw data from generated results
The `data/` layer should eventually distinguish:
- imported raw observational data,
- generated analysis artifacts,
- notebooks and exploratory visuals.

### Priority D — isolate exploratory sector branches
`ResChem/`, PBH-related work, and some white-thread toy-model pipelines should remain clearly marked as downstream exploratory material.

---

## 6. AGENT6 next recommended action

After this audit, the next useful artifact is:

**a seed equation register**

where the first canonical equations are listed with:
- stable IDs,
- status,
- dependency order,
- likely current source file,
- sector inheritance consequences.

---

## 7. Status
This audit is initial, not final.
It establishes the first file-placement classification for the `Metatime` repository on branch `Agent6` and should guide further canonicalization work.
