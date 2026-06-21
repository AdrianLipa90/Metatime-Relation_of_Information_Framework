# METATIME Standard Model Derivation
## Zeta-Polar to Tetrahedral Anchor Kernel v1.1

### Status

This layer continues the Standard Model derivation program after the full-action seed arbitration layer v1.0.  It corrects the remaining open dependency by inserting the zeta-polar spectral map before the tetrahedral depth is used as the source of the Poincare disk.

The ordering frozen in this layer is:

\[
S^2_{\rm Bloch}\longrightarrow (N,S)_{\rm polar}\longrightarrow \{\rho_n=1/2+i\gamma_n\}_{n\ge 1}\longrightarrow T_4\longrightarrow \mathbb D_T\longrightarrow \mathcal S_f^{EB}.
\]

The Poincare disk is therefore not primitive.  It is reached only after the zeta-polar data have been routed through the tetrahedral internal-depth frame.

### Canonical tetrahedral frame

Use the regular tetrahedral frame in the Bloch ball

\[
T_4=\{v_0,v_1,v_2,v_3\}\subset B^3_{\rm Bloch}
\]

with

\[
v_i\cdot v_j=-\frac13\quad(i\ne j),\qquad \|v_i\|=1.
\]

The polar vertex \(v_0\) is assigned to the Bloch polar axis.  The three base vertices span the internal face whose conformal/projective image defines the two-dimensional Poincare disk used by later Collatz and Kepler layers.

### Zeta-polar anchor rule

Let

\[
\rho_n=\frac12+i\gamma_n
\]

be the non-trivial zeta zeros on the critical line.  This layer uses the first 64 zeros as a finite spectral sampling surface.  Each zero is converted into a tetrahedral barycentric weight vector

\[
w_n=(w_{n0},w_{n1},w_{n2},w_{n3}),
\qquad
\sum_iw_{ni}=1,
\qquad w_{ni}\ge0.
\]

The depth coordinate is derived from the logarithmic position of \(\gamma_n\) relative to the first and last sampled zero.  The angular coordinate is the phase of \(\gamma_n\) modulo \(2\pi\).  The polar vertex receives the shallow-depth weight; the three base vertices receive angular soft assignments.  This gives a deterministic zeta-to-tetrahedron map without using fermion masses.

### Seed sampling

For a twin-prime seed \(s=(p,p+2)\), two Collatz orbits are generated.  At each step the paired orbit values select a zeta-zero index by a deterministic symmetric sampling rule.  The sampled zeta-zero weights define a seed-level average tetrahedral spectral signature.

The resulting seed features include:

- zeta-tetrahedral entropy,
- vertex asymmetry,
- polar-apex weight,
- base-face balance,
- tetrahedral spectral path length,
- mean zeta depth,
- phase winding.

These features are combined into a candidate zeta-tetrahedral spectral action.  The coefficients are structural and fixed in the script; no observed mass is used.

### Relationship to previous layers

Layer v0.8 established that tetrahedral depth precedes the Poincare disk.  Layer v0.9 added spin, Fibonacci rhythm, Kepler dynamics, Collatz dynamics, and the information scale.  Layer v1.0 assembled the first charged-fermion structural action.

Layer v1.1 adds the missing spectral-depth term:

\[
\mathcal S_f^{EB, v1.1}
=
\mathcal S_f^{EB, v1.0}
+
\kappa\,Z_s^{\zeta\to T_4}.
\]

This is still an ordinal and structural action layer.  It is not yet a numerical mass prediction.

### Validation results

The computation produces:

- a zeta-zero tetrahedral weight table,
- seed-level zeta-tetrahedral feature table,
- charged-fermion action table with the added zeta term,
- validation summary JSON.

No observed fermion mass is used as an input.  The charged-fermion ordinal hierarchy remains structurally checked after adding the zeta term, with the caveat that this is still an ordinal validation, not a mass-spectrum derivation.

### Open derivation debts

The following debts remain open:

1. derive the final zeta-polar anchor rule directly from the self-adjoint information operator rather than treating the phase assignment as a candidate finite sampling rule;
2. derive the constructive Euler-Berry coherence term;
3. convert ordinal structural action into numerical mass prediction;
4. extend the mechanism to neutrino mass and mixing;
5. determine whether additional twin-prime seeds are dynamically suppressed or represent higher inaccessible sectors.

### Generated artifacts

- `results/zeta_zero_tetrahedral_weights_v1_1.csv`
- `results/seed_zeta_tetrahedral_table_v1_1.csv`
- `results/charged_fermion_action_with_zeta_v1_1.csv`
- `results/zeta_tetrahedral_summary_v1_1.json`
- `scripts/zeta_tetrahedral_anchor_v1_1.py`
