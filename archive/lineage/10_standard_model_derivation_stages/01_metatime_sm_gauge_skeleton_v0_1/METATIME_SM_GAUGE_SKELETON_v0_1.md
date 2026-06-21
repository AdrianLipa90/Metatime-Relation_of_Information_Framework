# Metatime - Standard Model Gauge Skeleton from Euler-Berry Phase Closure v0.1

Status: canonical derivation patch, not a full Standard Model mass-spectrum proof.  
Scope: close the gauge skeleton first: state space, internal bundle, gauge group, one-generation representations, hypercharge ratios, anomaly cancellation, and the role of the Euler-Berry holonomy constraint.

## 0. Source decision

The `Metatime-main.zip` archive contains enough material to define a theory in parts. For this patch the source hierarchy is:

1. `MetaTheory_260218_073120.txt` - primary proto-canonical source for state space, Kähler geometry, White-Thread holonomy, observables, charge, spin, and Hamiltonian.
2. `reports/AGENT6_DERIVATION_PRIORITY_REPORT_2026-03-25.md` and `registries/AGENT6_EQUATION_PRIORITY_REGISTER_2026-03-25.yaml` - internal repository audit showing that the missing element is the canonical equation ladder, not lack of material.
3. `documents/Formal_SM.pdf` - useful sector/phenomenology source; not primary canon, because it contains fitted or calibrated numerical layers.
4. `documents/MetaEFT.pdf` - effective-field-theory layer; treat as downstream unless it conflicts with the more fundamental phase-first construction.

## 1. Frozen primitive layer

The foundational state space is taken as

\[
\mathcal H = L^2(\mathcal M,\mathcal E),
\]

where

\[
\mathcal M \simeq \mathbb{CP}^1 \simeq S^2_{\rm Bloch}
\]

and

\[
(\mathbb{CP}^1,g_{\rm FS},\omega_{\rm FS},J)
\]

is the minimal Kähler state geometry. The bundle \(\mathcal E\) carries the internal degrees of freedom that must become color, weak isospin, and hypercharge.

The phase-first connection is frozen as

\[
\mathcal A_{\rm EBI}
=\mathcal A_{\rm AB}+\mathcal A_{\rm Berry}+\mathcal A_{\rm Euler}+\mathcal A_{\mathcal I}.
\]

The admissibility condition is the Euler-Berry phase closure law

\[
\boxed{
\frac{1}{2\pi}\oint_{\gamma_f}\mathcal A_{\rm EBI}
= D_\Lambda+\epsilon_\nu+N_f,
\qquad N_f\in\mathbb Z.
}
\]

The cosmological and neutrino components are

\[
D_\Lambda = \frac{\Lambda R_H^2}{2}=\frac{3}{2}\Omega_\Lambda,
\]

and

\[
\epsilon^{ij}_\nu = \frac{\Delta m^2_{ij}L}{4\pi E}.
\]

The information scale is

\[
\kappa = \frac{\ln 2}{24\pi}.
\]

## 2. Internal bundle decomposition

To obtain the Standard Model gauge skeleton, the internal bundle is decomposed as

\[
\mathcal E
=\mathcal E_c\otimes\mathcal E_w\otimes\mathcal L_Y,
\]

with

\[
\dim_\mathbb C\mathcal E_c=3,
\qquad
\dim_\mathbb C\mathcal E_w=2,
\qquad
\dim_\mathbb C\mathcal L_Y=1.
\]

Interpretation:

- \(\mathcal E_c\) is the color-depth sector.
- \(\mathcal E_w\) is the Euler spin/polarization sector.
- \(\mathcal L_Y\) is the primitive phase line carrying hypercharge.

The unit-determinant automorphism groups are therefore

\[
\operatorname{Aut}_1(\mathcal E_c)=SU(3)_c,
\]

\[
\operatorname{Aut}_1(\mathcal E_w)=SU(2),
\]

and the line-bundle phase group is

\[
\operatorname{Aut}(\mathcal L_Y)=U(1)_Y.
\]

After the Euler orientation selection, the weak sector acts only on left-handed fields:

\[
SU(2)\longrightarrow SU(2)_L.
\]

Thus the gauge skeleton is

\[
\boxed{
G_{\rm SM}=SU(3)_c\times SU(2)_L\times U(1)_Y.
}
\]

A more precise global statement, once charge quantization is enforced, is the usual quotient

\[
\boxed{
G_{\rm SM}^{\rm global}
=\frac{SU(3)_c\times SU(2)_L\times U(1)_Y}{\mathbb Z_6}.
}
\]

## 3. Why the three factors arise

### 3.1 Hypercharge from the phase line

The physical state is projective:

\[
|\psi\rangle\sim e^{i\alpha}|\psi\rangle.
\]

Therefore the primitive phase degree of freedom is a \(U(1)\) line-bundle symmetry. The hypercharge generator is the normalized phase-closure operator

\[
\boxed{
\hat Y_f
=\frac{1}{2\pi}\oint_{\gamma_f}\mathcal A_Y.
}
\]

This is not yet electric charge. Electric charge appears only after electroweak orientation selection:

\[
\boxed{
Q=T_3+Y.
}
\]

This convention uses

\[
Y(Q_L)=\frac16,
\qquad
Y(H)=\frac12.
\]

### 3.2 Weak isospin from Euler spin closure

The Euler/spin closure gives spinor behavior:

\[
2\pi: \psi\mapsto -\psi,
\qquad
4\pi: \psi\mapsto \psi.
\]

This enforces the doublet structure

\[
\mathcal E_w\simeq\mathbb C^2,
\]

with local unit-determinant symmetry

\[
SU(2).
\]

The Standard Model needs this as \(SU(2)_L\), not a vectorlike \(SU(2)\). The required canonical statement is:

\[
\boxed{
\Pi_L=\frac{1-\gamma^5}{2}
\quad\text{is the Euler-Berry active weak sector.}
}
\]

Then weak transformations act as

\[
\psi_L\mapsto U_L\psi_L,
\qquad U_L\in SU(2)_L,
\]

while right-handed charged fermions are weak singlets.

### 3.3 Color from tetrahedral depth

The Bloch surface is two-dimensional, but the Metatime construction introduces internal depth. The clean closure rule is:

- a tetrahedral frame has four vertices \(v_0,v_1,v_2,v_3\);
- selecting one vertex as the phase/reference pole leaves three independent internal directions;
- their complex span is

\[
\mathcal E_c\simeq\mathbb C^3.
\]

The transformations preserving the Hermitian color norm and the internal volume phase form

\[
\boxed{
SU(3)_c.
}
\]

This is the cleanest current bridge:

\[
\text{tetrahedral depth}\longrightarrow \mathbb C^3\longrightarrow SU(3)_c.
\]

It should be treated as a canonical lemma requiring a separate proof from the zeta-pole/tetrahedral construction.

## 4. One generation of fermions

Use left-handed Weyl fields. The minimal one-generation content is

\[
Q_L=\begin{pmatrix}u\\ d\end{pmatrix}_L,
\qquad
u_L,e_L,
\qquad
u^c_L\ \text{optional},
\qquad
u^c_L\sim(\mathbf 1,\mathbf 1,0),
\]

and the left-handed conjugates

\[
u^c_L,\quad u^c_L,\quad d^c_L,\quad e^c_L.
\]

The Standard Model representation table is

| Field | \(SU(3)_c\) | \(SU(2)_L\) | \(Y\) |
|---|---:|---:|---:|
| \(Q_L=(u,d)_L\) | \(\mathbf 3\) | \(\mathbf 2\) | \(+1/6\) |
| \(u^c_L\) | \(\bar{\mathbf 3}\) | \(\mathbf 1\) | \(-2/3\) |
| \(d^c_L\) | \(\bar{\mathbf 3}\) | \(\mathbf 1\) | \(+1/3\) |
| \(L_L=(\nu,e)_L\) | \(\mathbf 1\) | \(\mathbf 2\) | \(-1/2\) |
| \(e^c_L\) | \(\mathbf 1\) | \(\mathbf 1\) | \(+1\) |
| \(\nu^c_L\), optional | \(\mathbf 1\) | \(\mathbf 1\) | \(0\) |

In right-handed Dirac notation this is equivalent to

\[
u_R\sim(\mathbf1,\mathbf1,0),
\quad
u_R\text{ optional},
\]

\[
u_R\quad\text{optional},\qquad
u_R\sim(\mathbf1,\mathbf1,0),
\]

\[
u_R\text{ does not affect Standard Model anomaly cancellation.}
\]

and

\[
u_R\text{ can be used later for neutrino mass completion if needed.}
\]

For charged right-handed fields:

\[
u_R\text{ aside},
\qquad
u_R\text{ optional},
\]

\[
 u_R\sim(\mathbf3,\mathbf1,+2/3),
\qquad
 d_R\sim(\mathbf3,\mathbf1,-1/3),
\qquad
 e_R\sim(\mathbf1,\mathbf1,-1).
\]

## 5. Hypercharge derivation from anomaly cancellation and holonomic mass transitions

Let the number of color directions be \(N_c\). For the tetrahedral-depth construction,

\[
N_c=3.
\]

Let the Higgs orientation field have hypercharge \(Y_H\). The neutral vacuum condition fixes

\[
Q(H^0)=T_3(H^0)+Y_H=0.
\]

Since the neutral component has \(T_3=-1/2\),

\[
\boxed{Y_H=\frac12.}
\]

Let the unknown hypercharges of one generation be

\[
Y_Q,
Y_u,
Y_d,
Y_L,
Y_e,
\]

where \(u,d,e\) denote the left-handed conjugate singlets \(u^c_L,d^c_L,e^c_L\).

Holonomic mass transitions must be gauge-invariant. The Higgs field is not a free mass insertion; it is the minimal phase-orientation selector. Gauge invariance of the three charged mass transitions gives

\[
Y_Q+Y_H+Y_u=0,
\]

\[
Y_Q-Y_H+Y_d=0,
\]

\[
Y_L-Y_H+Y_e=0.
\]

The mixed weak anomaly gives

\[
[SU(2)_L]^2U(1)_Y:
\qquad
N_cY_Q+Y_L=0.
\]

The gravitational anomaly gives

\[
[\mathrm{grav}]^2U(1)_Y:
\qquad
2N_cY_Q+N_cY_u+N_cY_d+2Y_L+Y_e=0.
\]

Substituting the mass-transition equations and the weak anomaly into the gravitational anomaly yields

\[
-N_cY_Q+Y_H=0.
\]

Therefore

\[
\boxed{Y_Q=\frac{Y_H}{N_c}.}
\]

For \(N_c=3\) and \(Y_H=1/2\),

\[
\boxed{Y_Q=\frac16.}
\]

Then

\[
Y_L=-N_cY_Q=-\frac12,
\]

\[
Y_u=-Y_Q-Y_H=-\frac23,
\]

\[
Y_d=-Y_Q+Y_H=+\frac13,
\]

\[
Y_e=-Y_L+Y_H=+1.
\]

Thus the full one-generation Standard Model hypercharge pattern is obtained.

## 6. Anomaly cancellation check

With

\[
(Y_Q,Y_u,Y_d,Y_L,Y_e)
=\left(\frac16,-\frac23,\frac13,-\frac12,1\right),
\]

we get

\[
[SU(3)_c]^2U(1)_Y:
\quad
2Y_Q+Y_u+Y_d=0,
\]

\[
[SU(2)_L]^2U(1)_Y:
\quad
3Y_Q+Y_L=0,
\]

\[
[\mathrm{grav}]^2U(1)_Y:
\quad
6Y_Q+3Y_u+3Y_d+2Y_L+Y_e=0,
\]

\[
[U(1)_Y]^3:
\quad
6Y_Q^3+3Y_u^3+3Y_d^3+2Y_L^3+Y_e^3=0.
\]

This is an exact algebraic closure of the hypercharge sector.

## 7. Electric charge closure

Using

\[
Q=T_3+Y,
\]

one obtains

\[
Q(u_L)=+\frac12+\frac16=+\frac23,
\]

\[
Q(d_L)=-\frac12+\frac16=-\frac13,
\]

\[
Q(\nu_L)=+\frac12-\frac12=0,
\]

\[
Q(e_L)=-\frac12-\frac12=-1.
\]

The right-handed Dirac fields have the same electric charges after conjugation.

Therefore the electroweak charge structure is recovered.

## 8. Final gauge-covariant derivative

The low-energy Standard Model covariant derivative is

\[
\boxed{
D_\mu
=\partial_\mu
-i g_s G^A_\mu T^A_c
-i g W^a_\mu T^a_L
-i g' B_\mu Y.
}
\]

In the Metatime interpretation these gauge connections are the projected sector components of the deeper Euler-Berry phase structure:

\[
\mathcal A_{\rm EBI}
\leadsto
(G_\mu^A,W_\mu^a,B_\mu)
\]

under the decomposition

\[
\mathcal E=\mathcal E_c\otimes\mathcal E_w\otimes\mathcal L_Y.
\]

## 9. What is closed now

This patch closes the Standard Model gauge skeleton:

\[
\boxed{
\mathcal H=L^2(\mathcal M,\mathcal E),
\quad
\mathcal M\simeq\mathbb{CP}^1,
\quad
\mathcal E=\mathcal E_c\otimes\mathcal E_w\otimes\mathcal L_Y
}
\]

\[
\boxed{
\Rightarrow
SU(3)_c\times SU(2)_L\times U(1)_Y
}
\]

\[
\boxed{
\Rightarrow
\text{one-generation representation table}
}
\]

\[
\boxed{
\Rightarrow
Y_Q=1/6,
Y_u=-2/3,
Y_d=1/3,
Y_L=-1/2,
Y_e=1
}
\]

\[
\boxed{
\Rightarrow
Q=T_3+Y
}
\]

\[
\boxed{
\Rightarrow
\text{all gauge and gravitational anomalies cancel.}
}
\]

## 10. What remains open

This is not yet the full Standard Model derivation. Remaining derivation debts:

1. Prove \(N_c=3\) directly from the zeta-pole/tetrahedral-depth construction, not only from the current tetrahedral reference-vertex lemma.
2. Prove the Euler-Berry chirality selection \(SU(2)\to SU(2)_L\), rather than treating it as the active weak-sector lemma.
3. Derive the gauge couplings \(g_s,g,g'\) and the Weinberg angle from the phase geometry.
4. Derive the Higgs potential from the phase-orientation sector.
5. Derive the holonomic mass action \(\mathcal S_f^{\rm EB}\) rather than fitting or reverse-engineering it from observed masses.
6. Derive CKM and PMNS matrices as relative holonomies of the quark and lepton mass operators.
7. Integrate the frozen cosmological and neutrino closure terms \(D_\Lambda\) and \(\epsilon_\nu\) into the sector equations without adjustable parameters.

## 11. Next derivation target

The next canonical target should be

\[
\boxed{
\mathcal S_f^{\rm EB}
\quad\text{and}\quad
\hat{\mathcal M}^{(f)}_{\rm hol}
}
\]

because once the gauge skeleton is closed, the real Standard Model problem becomes the mass and mixing sector.

The mass operator should not be written as free Yukawa couplings. It should be written as

\[
\boxed{
\hat{\mathcal M}^{(f)}_{\rm hol}
=
M_0\,
\Pi_{R,f}\,
\mathcal P
\exp\left(i\oint_{\gamma_f}\mathcal A_{\rm EBI}\right)
\Pi_{L,f}\,
\exp\left(-\frac{\mathcal S_f^{\rm EB}}{\kappa}\right).
}
\]

The effective Yukawa couplings are only low-energy names for eigenvalues of this operator:

\[
\boxed{
y_f^{\rm eff}
=
\frac{\sqrt2}{v}
\left|
\lambda_f\left(\hat{\mathcal M}^{(f)}_{\rm hol}\right)
\right|.
}
\]
