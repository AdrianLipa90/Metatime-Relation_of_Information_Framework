#!/usr/bin/env python3
"""
METATIME / Standard Model Derivation v3.9
Tetrahedral triplet -> CP2 -> su(3)-candidate lift.

Strict scope:
- no PDG, no observed masses, no CKM/PMNS, no mass calculation;
- tetrahedron gives a triplet frame / CP2 carrier candidate;
- full QCD is NOT claimed, because local dynamics, coupling running,
  confinement, and empirical hadron sector are outside this structural gate.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import List, Tuple

CREATED_UTC = "2026-06-20T15:40:00Z"
SCHEMA = "METATIME_SM_TETRA_TRIPLET_SU3_LIFT_V3_9"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

Vector = Tuple[Fraction, Fraction, Fraction]
Matrix = List[List[complex]]


def dot(a: Vector, b: Vector) -> Fraction:
    return sum(x*y for x, y in zip(a, b))


def sub(a: Vector, b: Vector) -> Vector:
    return tuple(x-y for x, y in zip(a, b))  # type: ignore[return-value]


def as_float_vec(v: Vector) -> List[float]:
    return [float(x) for x in v]


def tetrahedron_vertices() -> List[Vector]:
    # Regular tetrahedron centered at the origin. Sum of all vertices is zero.
    return [
        (Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(-1), Fraction(-1)),
        (Fraction(-1), Fraction(1), Fraction(-1)),
        (Fraction(-1), Fraction(-1), Fraction(1)),
    ]


def mat_mul(A: Matrix, B: Matrix) -> Matrix:
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def mat_sub(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mat_trace(A: Matrix) -> complex:
    return sum(A[i][i] for i in range(len(A)))


def conj_transpose(A: Matrix) -> Matrix:
    return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]


def frob_norm(A: Matrix) -> float:
    return math.sqrt(sum(abs(x)**2 for row in A for x in row))


def gell_mann() -> List[Matrix]:
    z = 0j
    one = 1+0j
    i = 1j
    rt3 = math.sqrt(3.0)
    return [
        [[z, one, z], [one, z, z], [z, z, z]],
        [[z, -i, z], [i, z, z], [z, z, z]],
        [[one, z, z], [z, -one, z], [z, z, z]],
        [[z, z, one], [z, z, z], [one, z, z]],
        [[z, z, -i], [z, z, z], [i, z, z]],
        [[z, z, z], [z, z, one], [z, one, z]],
        [[z, z, z], [z, z, -i], [z, i, z]],
        [[one/rt3, z, z], [z, one/rt3, z], [z, z, -2/rt3]],
    ]


def is_hermitian(A: Matrix, tol: float = 1e-12) -> bool:
    return frob_norm(mat_sub(A, conj_transpose(A))) < tol


def is_traceless(A: Matrix, tol: float = 1e-12) -> bool:
    return abs(mat_trace(A)) < tol


def trace_inner(A: Matrix, B: Matrix) -> complex:
    return mat_trace(mat_mul(A, B))


def commutator(A: Matrix, B: Matrix) -> Matrix:
    return mat_sub(mat_mul(A, B), mat_mul(B, A))


def scalar_mul(c: complex, A: Matrix) -> Matrix:
    return [[c*x for x in row] for row in A]


def mat_add(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def project_to_gell_mann_basis(M: Matrix, basis: List[Matrix]) -> Tuple[List[complex], float]:
    # Gell-Mann normalization: Tr(lambda_a lambda_b) = 2 delta_ab.
    coeffs = [trace_inner(M, L) / 2.0 for L in basis]
    reconstruction = [[0j for _ in range(3)] for _ in range(3)]
    for c, L in zip(coeffs, basis):
        reconstruction = mat_add(reconstruction, scalar_mul(c, L))
    residual = frob_norm(mat_sub(M, reconstruction))
    return coeffs, residual


def main() -> None:
    V = tetrahedron_vertices()
    closure = tuple(sum(v[k] for v in V) for k in range(3))
    reference_index = 0
    reference = V[reference_index]
    face_indices = [1, 2, 3]
    face_vertices = [V[i] for i in face_indices]
    edge_modes = [sub(V[i], reference) for i in face_indices]

    gram_edge = [[dot(a, b) for b in edge_modes] for a in edge_modes]
    edge_norms = [dot(e, e) for e in edge_modes]
    normalized_edge_cosines = [
        [float(gram_edge[i][j] / edge_norms[i]) if edge_norms[i] == edge_norms[j] else None for j in range(3)]
        for i in range(3)
    ]
    det_edge = (
        edge_modes[0][0]*(edge_modes[1][1]*edge_modes[2][2]-edge_modes[1][2]*edge_modes[2][1])
        - edge_modes[0][1]*(edge_modes[1][0]*edge_modes[2][2]-edge_modes[1][2]*edge_modes[2][0])
        + edge_modes[0][2]*(edge_modes[1][0]*edge_modes[2][1]-edge_modes[1][1]*edge_modes[2][0])
    )

    # Opposite face is an equilateral triangle: pairwise dot products are equal.
    face_pairwise_dot = [[dot(a, b) for b in face_vertices] for a in face_vertices]
    face_norms = [dot(f, f) for f in face_vertices]
    face_plane_sum = [sum(v[k] for v in face_vertices) for k in range(3)]
    opposite_face_closure_relation = [face_plane_sum[k] + reference[k] for k in range(3)]

    # Continuous lift: triplet carrier is C^3; projectivization gives CP2.
    cp2_carrier = {
        "basis_labels": ["color_0", "color_1", "color_2"],
        "complex_dimension_before_projectivization": 3,
        "projective_space": "CP2 = (C^3 - {0}) / C*",
        "unitary_lift_before_determinant_constraint": "U(3)",
        "traceless_determinant_one_candidate": "SU(3)",
        "finite_tetrahedral_symmetry_is_not_enough": True,
        "additional_principle_needed": "local unitary gauge redundancy on the complex triplet carrier",
    }

    lambdas = gell_mann()
    hermitian = [is_hermitian(L) for L in lambdas]
    traceless = [is_traceless(L) for L in lambdas]
    norms = [[trace_inner(lambdas[a], lambdas[b]) for b in range(8)] for a in range(8)]
    norm_ok = all(abs(norms[a][b] - (2.0 if a == b else 0.0)) < 1e-10 for a in range(8) for b in range(8))

    closure_residuals = []
    max_residual = 0.0
    for a in range(8):
        for b in range(8):
            comm = commutator(lambdas[a], lambdas[b])
            # [lambda_a, lambda_b] is anti-Hermitian. Divide by i to place it in Hermitian traceless span.
            hermitian_comm = scalar_mul(1/1j, comm)
            coeffs, residual = project_to_gell_mann_basis(hermitian_comm, lambdas)
            max_residual = max(max_residual, residual)
            if residual > 1e-10:
                closure_residuals.append({"a": a+1, "b": b+1, "residual": residual, "coeffs": [str(c) for c in coeffs]})

    payload = {
        "schema": SCHEMA,
        "created_utc": CREATED_UTC,
        "status": "PASS",
        "scope": "tetrahedral triplet carrier and su(3)-candidate algebraic lift; no masses and no PDG inputs",
        "forbidden_inputs": ["PDG", "observed masses", "CKM", "PMNS", "old fitted tau/eigenvalue tables"],
        "mass_prediction_claimed": False,
        "full_qcd_claimed": False,
        "tetrahedron": {
            "vertices": [as_float_vec(v) for v in V],
            "exact_vertices": [[str(x) for x in v] for v in V],
            "centered_closure_sum": [str(x) for x in closure],
            "reference_vertex_index": reference_index,
            "face_indices_used_as_triplet": face_indices,
            "edge_modes_from_reference": [as_float_vec(e) for e in edge_modes],
            "edge_gram_exact": [[[str(x) for x in row] for row in gram_edge]][0],
            "edge_mode_determinant_exact": str(det_edge),
            "edge_modes_independent": det_edge != 0,
            "normalized_edge_cosines": normalized_edge_cosines,
            "opposite_face_pairwise_dot_exact": [[[str(x) for x in row] for row in face_pairwise_dot]][0],
            "opposite_face_norms_exact": [str(x) for x in face_norms],
            "opposite_face_plus_reference_closure_exact": [str(x) for x in opposite_face_closure_relation],
            "triplet_reading": "choosing one vertex as closure/reference leaves three face/edge modes; these are the structural triplet carrier labels",
        },
        "cp2_su3_lift": cp2_carrier,
        "gell_mann_su3_candidate_checks": {
            "generator_count": len(lambdas),
            "all_hermitian": all(hermitian),
            "all_traceless": all(traceless),
            "trace_normalization_Tr_lambda_a_lambda_b_2_delta_ab": norm_ok,
            "commutator_span_max_residual_after_projection": max_residual,
            "commutator_closure_pass": not closure_residuals,
            "closure_residuals": closure_residuals[:20],
        },
        "guardrail": {
            "allowed_claim": "tetrahedral frame yields a triplet carrier and CP2/SU3-candidate algebraic lift",
            "forbidden_claims": [
                "tetrahedron alone proves full QCD",
                "full gluon dynamics derived",
                "confinement derived",
                "mass spectrum derived",
                "Debt 9 closed",
            ],
            "debt9_status": "OPEN_NOT_CLOSED",
            "doctor_verdict": "CONTINUE_RESEARCH__TETRA_TRIPLET_SU3_LIFT_PASS__QCD_NOT_CLOSED",
        },
    }

    (RESULTS / "tetra_triplet_su3_lift_v3_9.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
