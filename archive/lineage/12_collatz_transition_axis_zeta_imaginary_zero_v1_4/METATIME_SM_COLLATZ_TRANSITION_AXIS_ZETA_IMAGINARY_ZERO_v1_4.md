# METATIME Standard Model Derivation — Collatz Transition Axis and Zeta Imaginary-Zero Axis v1.4

## Status

This module supersedes the previous treatment in which the Poincare disk and the
Collatz trajectory were allowed to appear too early in the derivation chain.  The
canonical order is now:

1. projective Hilbert/Kahler state space;
2. zeta-polar anchoring;
3. tetrahedral depth inside the Bloch ball;
4. derived internal Poincare disk;
5. Collatz trajectory on the derived disk;
6. terminal transition axis;
7. zeta imaginary-zero axis;
8. Euler--Berry coherence gate.

## Main correction

The terminal Collatz structure is not merely the integer cycle

```text
4 -> 2 -> 1
```

The model requires the extended transition axis

```text
4 -> 2 -> 1 -> 1/2
```

The endpoint `1/2` is not an ordinary integer Collatz iterate.  It is the
projective spin-half endpoint where the integer terminal cycle is tied to
Euler spin closure, Bloch polarity, and the Riemann critical-line anchor.

## Zeta axis placement

The zeta layer is now placed as an axis, not as an additive raw mass cost.  The
axis is the imaginary spectral direction over the common half-anchor:

```text
s_n = 1/2 + i gamma_n,
where zeta(s_n) = 0.
```

Thus the same `1/2` anchor appears in two places:

1. as the terminal projective endpoint of the Collatz transition axis;
2. as the real coordinate of the zeta critical line.

This binds the Collatz terminal structure and the zeta spectral structure at the
same phase-axis anchor.

## Operator scale

The information-operator scale is kept fixed:

```text
kappa = ln(2)/(24*pi).
```

This module does not introduce a new fitted numerical parameter.

## Interpretation

The zeta term must not be added as a naive damping cost in the mass action.  The
previous v1.1 test already showed that naive insertion of the raw zeta term can
break the generational order.  In v1.4, zeta is treated as a coherence-axis gate:
it decides whether a terminal transition is phase-compatible rather than simply
increasing the mass suppression.

## Validation results

The script `scripts/transition_axis_zeta_imaginary_zero_v1_4.py` checks the
minimal twin-prime candidate set.  Each candidate reaches the terminal Collatz
axis and is extended to the spin-half endpoint.  Each selected zeta coordinate
is explicitly kept on the critical line.

Generated files:

- `results/transition_axis_zeta_imaginary_zero_v1_4.csv`
- `results/transition_axis_summary_v1_4.json`
- `results/script_stdout_v1_4.txt`

## Canonical effect on later modules

Later mass-action modules must use this axis order:

```text
tetrahedral depth -> Poincare disk -> Collatz trajectory -> 4->2->1->1/2 axis -> zeta imaginary-zero coherence axis
```

Any module that treats zeta as a direct raw mass cost is marked as pre-v1.4 and
must not be promoted as the final mass law.

## Open derivation debts

1. Formal proof of the zeta-polar assignment from Bloch poles to tetrahedral vertices.
2. Full Euler--Berry coherence functional using the zeta imaginary-zero axis.
3. Mass-value prediction without using observed fermion masses as input.
4. Extension to mixing matrices and neutrino masses.
