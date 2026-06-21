# METATIME / Standard Model Derivation
## Tetrahedral Depth to Poincare Disk Kernel v0.8

Status: technical derivation layer, not a final mass prediction and not a final canon promotion.

### 0. Purpose

The previous derivation sequence introduced a Collatz--Poincare action kernel before explicitly freezing the tetrahedral origin of the disk.  The present layer corrects that ordering.

The canonical dependency is now:

\[
S^2_{\rm Bloch}\ \longrightarrow\ B^3_{\rm Bloch}\ \longrightarrow\ T_4\ \longrightarrow\ \Pi_T\ \longrightarrow\ \mathbb D_{\rm Poincare}\ \longrightarrow\ {\rm Collatz\ dynamics}.
\]

Thus the Poincare disk is not an externally appended stage.  It is derived as the two-dimensional conformal/projective disk associated with the tetrahedral internal depth frame inside the Bloch ball.

Observed fermion masses are not used in this layer.

### 1. Canonical tetrahedral frame

Use a regular tetrahedron embedded in the Bloch ball with one polar apex and one equilateral base face:

\[
 v_0=(0,0,1),
\]

\[
 v_1=\left({2\sqrt2\over3},0,-{1\over3}\right),
\quad
 v_2=\left(-{\sqrt2\over3},{\sqrt6\over3},-{1\over3}\right),
\quad
 v_3=\left(-{\sqrt2\over3},-{\sqrt6\over3},-{1\over3}\right).
\]

The frame satisfies

\[
 v_i\cdot v_j=
 \begin{cases}
 1,& i=j,\\
 -1/3,& i\ne j.
 \end{cases}
\]

This is the first rigid three-dimensional internal-depth object.  It is the minimal non-planar frame and therefore the minimal candidate for generating an internal triplet from a polar spinor geometry.

### 2. From tetrahedral depth to disk

Let an internal point be represented by positive tetrahedral weights

\[
w=(w_0,w_1,w_2,w_3),\qquad w_i>0,
\]

and define the Bloch-ball point

\[
X(w)={\sum_i w_i v_i\over \sum_i w_i}.
\]

The Bloch ball is treated as a projective/Klein ball.  The corresponding Poincare-ball point is

\[
Y(X)={X\over 1+\sqrt{1-|X|^2}}.
\]

The two-dimensional disk is obtained by projection onto the base-face plane spanned by two orthonormal tetrahedral basis vectors.  If these basis vectors are \(e_1,e_2\), then

\[
z_T(w)=\langle Y(X(w)),e_1\rangle+i\langle Y(X(w)),e_2\rangle,
\qquad |z_T|<1.
\]

This gives the corrected order: tetrahedral depth produces the Poincare disk coordinate.

### 3. Collatz enters after the tetrahedral projection

For a twin-prime generation seed

\[
s=(p,p+2),
\]

compute paired Collatz branches

\[
(a_k,b_k)=\left(C^k(p),C^k(p+2)\right).
\]

The paired step \((a_k,b_k)
\) is not mapped directly into an ad hoc disk.  Instead it is first mapped into tetrahedral weights:

\[
w_k=W_T(a_k,b_k,k).
\]

The v0.8 implementation uses a mass-blind candidate rule: the polar weight is driven by parity disagreement and branch asymmetry, while the three base weights are driven by residues modulo three and a small cyclic route marker.  This is deliberately marked as a candidate kernel, not a final physical law.

The disk trajectory is then

\[
z_k=z_T(w_k).
\]

### 4. Hyperbolic action diagnostics

Once the tetrahedral projection has produced the disk trajectory, the kernel computes hyperbolic path diagnostics on \(\mathbb D\):

- Poincare path length per step,
- mean disk radius,
- maximum disk radius,
- turning per step,
- cycle-closure distance,
- tetrahedral entropy,
- polar weight,
- base-face balance.

These are combined into a v0.8 candidate tetrahedral--Poincare action.  The coefficients are fixed inside the diagnostic script and are not fitted to fermion masses.

### 5. Relationship to the previous Collatz--Poincare layer

The v0.4 artifact remains useful, but its conceptual order is corrected.

Old order:

\[
{\rm Collatz}\ \rightarrow\ \mathbb D.
\]

Corrected order:

\[
T_4\ \rightarrow\ \mathbb D_T\ \rightarrow\ {\rm Collatz\ route\ on\ }\mathbb D_T.
\]

In other words, the disk is now a consequence of tetrahedral depth, not a primitive chosen independently of it.

### 6. Validation boundary

This layer does not predict masses.

This layer does claim:

1. the tetrahedral frame is a mathematically rigid internal-depth object;
2. the Poincare disk can be derived from the tetrahedral depth frame through the Bloch/Klein/Poincare mapping;
3. Collatz dynamics should be evaluated on that derived disk, not on an externally assumed disk;
4. twin-prime seeds receive non-mass, structure-only action scores from this corrected route.

### 7. Results

The script writes:

- `results/tetra_poincare_depth_table_v0_8.csv`,
- `results/tetra_poincare_depth_summary_v0_8.json`,
- `results/tetra_poincare_minimal_triplet_paths_v0_8.svg`.

The results distinguish candidate twin-prime seeds without reading observed masses.  Therefore the layer is eligible to enter the later Euler--Berry mass-action functional as a structural predictor, not as a fitted mass label.

### 8. What is frozen in v0.8

Frozen as a derivation correction:

- tetrahedral depth precedes the Poincare disk;
- the disk is the conformal/projective two-dimensional geometry induced from the tetrahedral frame inside the Bloch ball;
- Collatz dynamics must be routed through tetrahedral weights before disk coordinates are computed.

Not frozen:

- the final tetrahedral weight rule;
- the final zeta-polar/tetrahedral-depth operator;
- exact mass predictions;
- final generation-to-seed assignment.

### 9. Next required stage

The next layer must replace the current candidate tetrahedral weight rule by a zeta-polar constrained map:

\[
\zeta\hbox{-polar anchors}\ \rightarrow\ T_4\ \rightarrow\ \mathbb D_T\ \rightarrow\ \mathcal S_f^{EB}.
\]

Only after this is done should the full mass-action assembly be evaluated against observed fermion mass hierarchy.
