# METATIME / Standard Model Derivation — Debt 5 Ramanujan Seed Suppression v2.1

## Scope

This module is an append-only update to the merged repository. It does **not** create a nested archive and it does **not** replace the previous derivation layers. It addresses the remaining debt: why extended twin-prime candidates should not automatically become additional Standard Model generations.

The user correction is binding for this layer:

> scaling requires Ramanujan.

Therefore scaling is not allowed to be an arbitrary fitted coefficient. It must be represented by a Ramanujan-type arithmetic/asymptotic layer.

---

## Formal status ledger

### [DEFINITION] Canonical information preference

The information preference scale remains

\[
\kappa=\frac{\ln 2}{24\pi}.
\]

It is not a fitted parameter.

### [DEFINITION] Seed integer

For a twin-prime seed

\[
s=(p,p+2),
\]

we assign the symmetric seed integer

\[
N_s=p(p+2).
\]

The product is used because it preserves both poles of the twin-prime pair and grows with the seed sector.

### [ANSATZ] Ramanujan scaling layer

The suppression of extended seed candidates is controlled by a Ramanujan scaling layer, not by observed masses.

The layer has two pieces:

1. a Hardy--Ramanujan asymptotic scale

\[
\sigma_R(N_s)=\pi\sqrt{\frac{2N_s}{3}},
\]

2. a Ramanujan-sum resonance diagnostic

\[
c_q(N_s)=\sum_{1\leq a\leq q,\, (a,q)=1}e^{2\pi i aN_s/q}.
\]

The first component supplies asymptotic growth. The second component allows arithmetic resonance to be recorded without confusing resonance with a mass fit.

### [LEMMA] Canonical three-seed visibility is not a mass input

The canonical minimal seed set

\[
(3,5),\quad(5,7),\quad(11,13)
\]

is not selected from fermion masses in this module. It is inherited from the preceding structural layers: tetrahedral depth, Collatz transition axis, Poincare disk embedding, spin, Fibonacci and Kepler timing, and Euler--Berry coherence.

### [PROOF / VALIDATION] No observed mass values are read

The script `scripts/ramanujan_seed_suppression_v2_1.py` uses only:

- integer primality,
- twin-prime candidates,
- Collatz orbit diagnostics,
- Hardy--Ramanujan asymptotic scaling,
- Ramanujan-sum resonance,
- the fixed information preference scale.

It does not read charged fermion masses, observed Yukawa couplings, CKM parameters, or PMNS parameters.

### [INTERPRETATION] Extended seeds are not deleted; they are gated

This layer does not say that all noncanonical seeds are impossible. It says they must pass a stricter Ramanujan-resonance and asymptotic suppression gate before they can be considered physically active.

Therefore the proper status of extra seeds is:

\[
\text{quarantined candidate sector},
\]

not

\[
\text{additional generation}.
\]

### [FORMAL DEBT]

This module does not yet prove exactly three generations. It introduces a controlled scaling gate and a ledger for extended seed candidates. The deeper theorem must show that only three seed sectors remain stable under the full Euler--Berry/Ramanujan/zeta-Heisenberg coherence constraints.

---

## Relation to previous modules

This module depends on the following already merged layers:

- Debt 1: Killing generator and polar axis.
- Debt 2: Euler--Berry coherence gate.
- Debt 3: zeta-polar axis and tetrahedral anchoring.
- Debt 4: seed assignment under coherence.
- Debt 6: Euler--Berry action ordering for masses.
- Preference and zeta-Heisenberg fluctuation layer v2.0.

It does not supersede them. It supplies the missing scaling layer required before mass ratios can be tested honestly.

---

## Validation status

See:

- `results/ramanujan_seed_suppression_table_v2_1.csv`
- `results/ramanujan_seed_suppression_summary_v2_1.json`
- `results/ramanujan_seed_suppression_validation_v2_1.txt`

The expected status is **controlled partial pass**, not final proof. This is correct: the module installs a non-fitted Ramanujan gate but does not yet prove the final three-generation theorem.
