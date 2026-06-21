# Validation Status v0.8

Status: PASS for structural derivation correction; NOT A MASS PREDICTION.

## Checks performed

1. Regular tetrahedral frame constructed inside the Bloch ball.
2. Gram matrix verifies the regular tetrahedron pattern.
3. Tetrahedral barycentric internal points are mapped into the Bloch/Klein ball.
4. Klein-to-Poincare conversion keeps projected disk points strictly inside the unit disk.
5. Twin-prime Collatz branches are routed through tetrahedral weights before disk coordinates are computed.
6. Observed fermion masses are not used.

## Best candidate in v0.8 diagnostic scan

Best seed by the candidate tetrahedral-Poincare action:

`[11, 13]`

This is not a final generation assignment.

## Minimal triplet rank data

```json
[
  [
    11,
    13,
    1
  ],
  [
    5,
    7,
    3
  ],
  [
    3,
    5,
    5
  ]
]
```

## Boundary

This layer corrects the dependency order from tetrahedra to disk.  It does not yet close the zeta-polar tetrahedral operator and does not claim numerical mass prediction.
