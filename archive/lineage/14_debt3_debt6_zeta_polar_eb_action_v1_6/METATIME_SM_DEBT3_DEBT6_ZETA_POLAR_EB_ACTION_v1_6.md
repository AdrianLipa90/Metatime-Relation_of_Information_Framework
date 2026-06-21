# METATIME Standard Model Derivation — Debt 3 and Debt 6 Closure Candidate v1.6

## Abstract

This module addresses two open formal debts left by the Euler--Berry canonical freeze:

1. **Debt 3:** the zeta-polar anchor map.
2. **Debt 6:** the Euler--Berry action needed for the charged-fermion mass hierarchy.

The module is not a separate package. It is part of the merged repository line and is appended as a normal directory. It contains explicit formal-status tags for all promoted statements.

The result is:

- Debt 3 is closed at the level of a precise definition plus a non-fitted ansatz.
- Debt 6 is partially closed at the ordinal hierarchy level for charged fermions.
- Numerical fermion masses remain open and are not claimed here.

Observed fermion masses are not used as model inputs.

---

## 1. Formal status ledger for this module

| Item | Status | Meaning |
|---|---|---|
| Critical-line zeta tower | Definition | Fixed spectral data, not fitted to masses. |
| North/south pairing of zeta zeros | Definition | Paired anchors above and below the critical half-axis. |
| Tetrahedral vertex assignment by zero-index modulo four | Ansatz | Exact, reproducible, non-fitted rule; still requires deeper proof. |
| Zeta as imaginary zero axis | Interpretation | Zeta supplies a stationary imaginary coherence axis, not raw damping. |
| Zeta-polar coherence gate | Ansatz | Bounded coherence factor centered on the half-axis. |
| Debt 3 closure status | Lemma | The zeta-polar map is now explicit and reproducible. |
| Debt 6 ordinal hierarchy test | Validation gate | Charged-fermion ordinal hierarchy is tested without mass inputs. |
| Numerical mass spectrum | Formal debt | Exact mass ratios are not derived in this module. |

---

## 2. Debt 3 — zeta-polar anchors

### Definition 3.1 — Critical half-axis

The zeta-polar axis is the critical half-axis

\[
\Re(s)=\frac12.
\]

This axis is identified with the stationary imaginary zero axis in the phase-closure geometry.

### Definition 3.2 — Paired zeta-polar tower

Let the non-trivial zero ordinates of the Riemann zeta function on the critical line be denoted by \(\gamma_n\), so that

\[
\zeta\left(\frac12+i\gamma_n\right)=0.
\]

The north and south polar anchors are defined by the paired critical-line zeros

\[
N_n := \frac12+i\gamma_n,
\qquad
S_n := \frac12-i\gamma_n.
\]

This makes the zeta-polar structure explicitly two-sided and compatible with the spin-polar north/south structure.

### Ansatz 3.3 — Tetrahedral distribution of the zeta tower

The infinite tower of zeta-polar pairs is distributed over the four tetrahedral directions by the zero index modulo four:

\[
\nu_T(n)=1+((n-1)\bmod 4).
\]

This is not claimed as the final proof of the zeta-to-tetrahedron map. It is promoted only as an exact, reproducible, non-fitted ansatz that makes the Debt 3 map operational.

### Lemma 3.4 — Debt 3 operational closure

Given Definitions 3.1 and 3.2 and Ansatz 3.3, Debt 3 is operationally closed: each zeta zero pair has a north/south polar position and a tetrahedral depth direction.

### Proof

The map is explicit for every positive integer \(n\). Each \(\gamma_n\) determines one north anchor and one south anchor on the critical half-axis. The modulo-four assignment then maps the same index to one tetrahedral direction. Therefore the zeta-polar anchor map is total, deterministic, and reproducible. It uses no observed fermion masses.

---

## 3. Debt 6 — Euler--Berry action and charged-fermion hierarchy

### Definition 6.1 — Prior structural action

The prior structural action is imported from the v1.3 Euler--Berry coherence gate. It already includes:

- generation seed contribution;
- representation contribution;
- chiral transition gate;
- coherence adjustment from the earlier zeta-tetrahedral layer.

This module does not replace that prior action. It appends the explicit Debt 3 zeta-polar anchor map as a bounded coherence correction.

### Ansatz 6.2 — Zeta-polar coherence correction

The zeta-polar coherence correction is a bounded non-negative adjustment derived from the distance of the selected zeta ordinate to the half-axis coordinate after bounded diagnostic embedding.

It is not a free mass parameter. It is computed from:

- the twin-prime seed;
- the seed center;
- the selected zeta tower index;
- the corresponding zeta ordinate;
- the half-axis distance.

### Definition 6.3 — Seed-to-zeta tower selection

For a twin-prime seed \((p,p+2)\), the seed center selects a zeta tower index by a fixed modular rule over the available zeta ordinates. This links the twin-prime generation layer to the zeta-polar imaginary axis without using masses.

### Lemma 6.4 — Debt 6 partial closure

The assembled v1.6 Euler--Berry action gives an ordinal charged-fermion hierarchy candidate without importing observed masses as model inputs.

### Proof

The script `scripts/debt3_debt6_zeta_polar_eb_action_v1_6.py` consumes only structural action tables from earlier non-mass-input modules and the fixed zeta zero ordinates. It writes:

- a zeta-polar anchor table;
- a seed-to-zeta anchor table;
- a charged-fermion Euler--Berry action table;
- an ordinal validation table.

The ordinal validation checks only whether the action decreases from generation one to generation three inside each charged sector. Since the action is interpreted as damping, decreasing action corresponds to increasing mass scale. The validation passes for the charged-lepton, down-quark, and up-quark sectors.

No observed mass value is read by the script.

---

## 4. Interpretation

Debt 3 gives the zeta axis a fixed place: it is not a decorative reference and not a raw mass cost. It is the stationary imaginary zero axis paired with the spin half-axis and distributed through tetrahedral depth.

Debt 6 is not fully solved numerically. What is solved here is the structural and ordinal version: the model now has an Euler--Berry action table that preserves the charged-fermion generational order without using the observed masses as inputs.

The remaining work is to derive numerical mass ratios, CKM mixing, PMNS mixing, and the neutrino mass mechanism.

---

## 5. Validation outputs

Generated outputs:

- `results/zeta_polar_anchor_table_v1_6.csv`
- `results/generation_seed_zeta_anchor_map_v1_6.csv`
- `results/charged_fermion_eb_action_debt6_v1_6.csv`
- `results/debt6_ordinal_validation_v1_6.csv`
- `results/debt3_debt6_summary_v1_6.json`

The validation status is recorded in `VALIDATION_STATUS_v1_6.md`.

---

## 6. Remaining formal debts after v1.6

1. Prove or replace the modulo-four zeta-to-tetrahedron assignment.
2. Derive numerical mass ratios without fitting.
3. Derive the CKM matrix from relative holonomies.
4. Derive the PMNS matrix from neutrino-sector holonomies.
5. Close the neutrino mass mechanism.
6. Connect this action layer to the canonical manuscript as a single uninterrupted derivation.
