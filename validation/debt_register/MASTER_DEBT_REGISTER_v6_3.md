# v6.3 Master Debt Register / Closure Queue
Created UTC: `2026-06-21T10:26:33Z`
Mode: debt register and closure queue only. No new physics module is introduced here.
## Status enum
- `ACTIVE_NOW`
- `BLOCKED_WITH_REASON`
- `CLOSED`
- `MERGED_INTO_DEPENDENCY`
- `QUARANTINED_WITH_TRACE`

## Debts
### DEBT-000 — Artifact lineage gap / false-continuity risk
- Severity: `CRITICAL`
- Status: `CLOSED`
- Closure action: Use v6.0A as byte parent; quarantine previous gap-branch as non-current; preserve 60B/61/62 only as add-on modules on restored parent.
- Validation: Required dirs 37-59 and 60A present in v6.3 tree.

### DEBT-001 — No nested archives invariant
- Severity: `CRITICAL`
- Status: `CLOSED`
- Closure action: Final package includes unpacked repo tree only; source archives remain outside artifact.
- Validation: Archive extension scan over final ZIP entries.

### DEBT-002 — Gap-branch quarantine
- Severity: `CRITICAL`
- Status: `CLOSED`
- Closure action: Mark old standalone gap artifacts non-current; restored add-ons are retained only through v6.2R/v6.3 lineage.
- Validation: Continuity restore ledger and v6.3 register.

### DEBT-003 — Full module continuity 00-62
- Severity: `CRITICAL`
- Status: `CLOSED`
- Closure action: Freeze v6.3 as first debt-managed restored lineage artifact.
- Validation: Expected directory check generated in validation JSON.

### DEBT-004 — Legacy full-root compile blocker
- Severity: `HIGH`
- Status: `CLOSED`
- Closure action: Preserve exact content and change executability from .py to .py.md; record original SHA and new SHA.
- Validation: Full-root python compileall returns PASS after quarantine.

### DEBT-005 — Exact table / PDG replay provenance classification
- Severity: `HIGH`
- Status: `ACTIVE_NOW`
- Closure action: Classify every exact/replay/benchmark table as SOURCE_DERIVED, STRUCTURAL_HINT, SCORING_ONLY, TAINTED_REPLAY, or UNKNOWN_PROVENANCE before further physics claims.
- Validation: v6.4 table provenance matrix required.

### DEBT-006 — Unit anchors removal ledger
- Severity: `HIGH`
- Status: `ACTIVE_NOW`
- Closure action: Create anchor ledger: input anchors, scoring anchors, derived anchors, forbidden anchors; remove or explicitly quarantine each.
- Validation: v6.5 anchor audit must tag every mass or scale source.

### DEBT-007 — Absolute charged-lepton electron action offset S_e
- Severity: `HIGH`
- Status: `ACTIVE_NOW`
- Closure action: Derive S_e from predeclared geometry without using electron mass as input.
- Validation: v6.6 must freeze formula before scoring against masses.

### DEBT-008 — mu-to-tau release refinement
- Severity: `MEDIUM`
- Status: `MERGED_INTO_DEPENDENCY`
- Merged into: `DEBT-007`
- Closure action: Refine only after S_e and anchor ledger are controlled.
- Validation: Separate v6.x release freeze required.

### DEBT-009 — Hadron and meson sector split
- Severity: `HIGH`
- Status: `BLOCKED_WITH_REASON`
- Blocker: DEBT-005 provenance classification and DEBT-006 anchor ledger must complete first.
- Closure action: After table and anchor gates, freeze baryon triplet and meson pair-state operators separately.
- Validation: Separate baryon/meson validation files.

### DEBT-010 — Absolute E0 normalizer status
- Severity: `HIGH`
- Status: `MERGED_INTO_DEPENDENCY`
- Merged into: `DEBT-007`
- Closure action: Treat E0 as dimensional carrier; close through S_I derivation and anchor ledger.
- Validation: No E0-alone mass claim.

### DEBT-011 — Document operator index: Ramanujan, OI, Collatz, White Thread, sigma/R
- Severity: `HIGH`
- Status: `ACTIVE_NOW`
- Closure action: Create operator-to-document-to-module index; bind each operator to provenance path and module usage.
- Validation: v6.4/v6.5 must cite operator source files in repo artifacts.

### DEBT-012 — Debt process invariant
- Severity: `CRITICAL`
- Status: `CLOSED`
- Closure action: Every future debt must be CLOSED, ACTIVE_NOW, BLOCKED_WITH_REASON, MERGED_INTO_DEPENDENCY, or QUARANTINED_WITH_TRACE.
- Validation: v6.3 validation rejects unknown debt statuses.

## Closure queue
1. `DEBT-005` — Build v6.4 exact-table / replay / PDG provenance matrix. Blocks: DEBT-006, DEBT-007, DEBT-009.
2. `DEBT-011` — Build operator source index across repo docs and modules. Blocks: DEBT-006, DEBT-007.
3. `DEBT-006` — Build unit-anchor ledger and remove/quarantine anchor claims. Blocks: DEBT-007, DEBT-009.
4. `DEBT-007` — Derive absolute electron action S_e from predeclared geometry. Blocks: DEBT-008, DEBT-010.
5. `DEBT-009` — Return to baryon/meson split after provenance and anchor gates. Blocks: none.
