# Metatime — Euler--Berry Action Closure for the Standard Model Mass Sector v0.2

Status: canonical candidate for the next layer after the gauge skeleton and mass vectorization. This is **not** yet a claimed derivation of the observed fermion mass spectrum.

## 0. Purpose

The previous layer defined the vector state

\[
\mathcal V_f
=\mathbf r_f\oplus\mathbf h_f\oplus\mathbf c_s\oplus\mathbf g_f\oplus\mathbf z_s.
\]

The present layer asks what must be true for the Euler--Berry action

\[
\mathcal S_f^{EB}=\mathcal S^{EB}(\mathcal V_f)
\]

to replace standard Yukawa couplings as primitive mass inputs.

The answer is strict:

\[
\boxed{\text{representation data alone are insufficient.}}
\]

A generation/orbit vector is mathematically required.

## 1. Canonical objects retained

From the previous canonical layers we retain

\[
G_{SM}^{global}
=
\frac{SU(3)_c\times SU(2)_L\times U(1)_Y}{\mathbb Z_6},
\]

\[
\mathcal A_{EBI}
=
\mathcal A_{AB}
+
\mathcal A_{Berry}
+
\mathcal A_{Euler}
+
\mathcal A_{\mathcal I},
\]

\[
\frac{1}{2\pi}\oint_{\gamma_f}\mathcal A_{EBI}
=
D_\Lambda+\epsilon_\nu+N_f,
\qquad N_f\in\mathbb Z,
\]

\[
\kappa=\frac{\ln2}{24\pi}=0.009193150006360484.
\]

The charged-fermion mass projection remains

\[
y_f^{eff}
=
\exp\left(-\frac{\mathcal S_f^{EB}}{\kappa}\right)
\]

up to unitary phase factors and low-energy electroweak projection, hence

\[
m_f=\frac{v}{\sqrt2}|y_f^{eff}|.
\]

Observed masses are validation targets only. They do not define \(\mathcal S_f^{EB}\).

## 2. Why representation data cannot be enough

The Standard Model representation vector

\[
\mathbf r_f=(d_c,d_w,\chi,Y,T_3,Q)
\]

distinguishes sectors such as charged leptons, up-type quarks and down-type quarks, but it does not distinguish generations within a sector strongly enough.

For example, \(e,\mu,\tau\) have the same electroweak representation pattern. Likewise \(u,c,t\) share the same up-type representation pattern, and \(d,s,b\) share the same down-type pattern.

Therefore a mass hierarchy cannot be derived from \(\mathbf r_f\) alone.

The missing independent input is

\[
\mathbf c_s\oplus\mathbf g_f\oplus\mathbf z_s,
\]

namely the Collatz orbit vector, the geometry vector and the spectral/tetrahedral vector.

## 3. Diagnostic rank audit

The script `scripts/eb_action_basis_audit.py` performs a rank audit.

It tests two bases:

1. representation-only basis,
2. full diagnostic basis including Collatz/tau labels and generation/orbit labels.

The result is:

```text
representation-only rank = 3
representation-only RMSE on validation actions = 3.675443
full diagnostic basis rank = 7
full diagnostic RMSE on validation actions = 0.609592
```

Interpretation:

\[
\boxed{\mathbf r_f\text{ alone cannot carry the fermion mass hierarchy.}}
\]

The improvement after adding orbit/generation features is not a derivation; it is a dependency proof. It shows which missing layer is structurally necessary.

## 4. First non-fitted action stress test

A deliberately crude unit-coefficient candidate was tested:

\[
\mathcal A_f^{(0)}
=
\log\frac{100}{\tau_f}
+R_f,
\]

where

\[
R_f
=\log(3)\,\mathbf 1_{d_c=1}
+\frac12|Q_f|
+\frac14(d_w-1)
+\frac14\mathbf 1_{T_3<0}.
\]

and

\[
\mathcal S_f^{(0)}=\kappa\mathcal A_f^{(0)}.
\]

This stress test is not a prediction claim. It is intentionally included because it fails to reproduce the validation targets with sufficient precision. The failure is useful: it proves that the real action cannot be just a naive Collatz-depth plus elementary representation penalty.

## 5. Correct canonical form for the next layer

The next valid action must have the form

\[
\boxed{
\mathcal S_f^{EB}
=
\kappa\left[
\mathcal C_s
+
\mathcal G_f
+
\mathcal Z_s
+
\mathcal R_f
-\mathcal \Omega_f
\right]_+
}
\]

where:

\[
\mathcal C_s
\]

is the normalized Collatz orbit cost,

\[
\mathcal G_f
\]

is the Fubini--Study / Poincare geodesic contribution,

\[
\mathcal Z_s
\]

is the zeta-polar / tetrahedral-depth spectral contribution,

\[
\mathcal R_f
\]

is the representation and chiral-transition contribution,

\[
\mathcal\Omega_f
\]

is the constructive Euler--Berry / white-thread coherence contribution.

The bracket \([\cdot]_+\) indicates that the real damping action is non-negative. Constructive coherence can reduce the action but cannot make the damping action negative.

## 6. Required geometric definitions

To turn v0.2 into an actual mass-spectrum derivation, the following maps must be defined without using observed masses:

### 6.1 Collatz orbit embedding

\[
z_s(k):\mathcal O_s(k)\to\mathbb D,
\]

where \(\mathbb D\) is the Poincare disk.

### 6.2 Orbit cost

\[
\mathcal C_s
=
\lim_{K\to K_s}
\frac1K\sum_{k=0}^{K-1}
\log\left(1+|C^k(p)|+|C^k(p+2)|\right),
\]

or another explicitly frozen Collatz functional. The choice must be made before comparison with masses.

### 6.3 Geometric distance

\[
\mathcal G_f
=
 d_{FS}(\psi_L,\psi_R)+d_{\mathbb D}(z_0,z_f).
\]

### 6.4 Euler--Berry coherence

\[
\mathcal \Omega_f
=
\left|\int_{\Gamma_f}\mathcal A_{Berry}
+\mathcal A_{Euler}\right|
\]

or, for pairwise mixing,

\[
\mathcal \Omega_{ij}
=
\left|W_{ij}\right|^2e^{-S_{cl}[\Gamma_{ij}]}.
\]

### 6.5 Spectral/tetrahedral contribution

\[
\mathcal Z_s
=Z(\gamma_n,T_s),
\]

where \(\gamma_n\) are zeta-zero labels and \(T_s\) is the tetrahedral-depth frame. This is still an open formal map.

## 7. Relation to Metatime source documents

The older Metatime documents already contain the correct direction:

\[
\hat M\Psi
=\delta\alpha\sum_{i=0}^{\hat L-1}\log_2(\hat n_i)\Psi,
\]

and pairwise white-thread factors

\[
F_{ij}=|W_{ij}|^2e^{-S_{cl}[\gamma_{ij}]}.
\]

They also correctly identify that bounded corrections are insufficient for the neutrino sector and that exponential corrections are geometrically forced by the effective fractal/topological dimension.

The v0.2 correction is that these pieces are not yet allowed to claim a full mass derivation until the maps \(z_s(k)\), \(\mathcal C_s\), \(\mathcal G_f\), \(\mathcal Z_s\), and \(\mathcal\Omega_f\) are fixed without fitting to masses.

## 8. Status

What is now established:

\[
\boxed{\text{the mass sector requires orbit/vector geometry beyond SM representations.}}
\]

What is not yet established:

\[
\boxed{\text{the observed fermion mass spectrum has not yet been derived.}}
\]

The next step is therefore not another fit. The next step is an explicit Collatz-to-Poincare embedding and an Euler--Berry action integral evaluated on that embedding.
