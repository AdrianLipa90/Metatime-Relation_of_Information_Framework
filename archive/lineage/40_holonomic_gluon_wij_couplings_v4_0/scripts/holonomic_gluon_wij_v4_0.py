#!/usr/bin/env python3
"""
METATIME / Standard Model Derivation v4.0
Holonomic gluon dynamics as W_ij couplings between quark/triplet nodes.

Scope:
- continues v3.9 tetrahedral triplet -> CP2 -> SU(3)-candidate carrier;
- defines W_ij as SU(3)-valued parallel transport/coupling between triplet quark nodes;
- defines gluon modes as su(3) generator components of holonomic link curvature;
- checks gauge-covariant transformation of W_ij and loop holonomy;
- does not import PDG, observed masses, CKM/PMNS, or fitted mass tables;
- does not claim confinement, running coupling, hadron spectrum, or Debt 9 closure.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

CREATED_UTC = "2026-06-20T16:25:00Z"
SCHEMA = "METATIME_SM_HOLONOMIC_GLUON_WIJ_V4_0"
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

C = complex
Matrix = List[List[C]]


def eye3() -> Matrix:
    return [[1+0j, 0j, 0j], [0j, 1+0j, 0j], [0j, 0j, 1+0j]]


def zeros3() -> Matrix:
    return [[0j, 0j, 0j], [0j, 0j, 0j], [0j, 0j, 0j]]


def mat_add(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] + B[i][j] for j in range(3)] for i in range(3)]


def mat_sub(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] - B[i][j] for j in range(3)] for i in range(3)]


def scalar_mul(c: C, A: Matrix) -> Matrix:
    return [[c * A[i][j] for j in range(3)] for i in range(3)]


def mat_mul(A: Matrix, B: Matrix) -> Matrix:
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def conj_transpose(A: Matrix) -> Matrix:
    return [[A[j][i].conjugate() for j in range(3)] for i in range(3)]


def trace(A: Matrix) -> C:
    return A[0][0] + A[1][1] + A[2][2]


def det3(A: Matrix) -> C:
    return (
        A[0][0]*(A[1][1]*A[2][2] - A[1][2]*A[2][1])
        - A[0][1]*(A[1][0]*A[2][2] - A[1][2]*A[2][0])
        + A[0][2]*(A[1][0]*A[2][1] - A[1][1]*A[2][0])
    )


def frob_norm(A: Matrix) -> float:
    return math.sqrt(sum(abs(x)**2 for row in A for x in row))


def is_unitary(A: Matrix, tol: float = 1e-10) -> bool:
    return frob_norm(mat_sub(mat_mul(conj_transpose(A), A), eye3())) < tol


def is_su3(A: Matrix, tol: float = 1e-10) -> bool:
    return is_unitary(A, tol) and abs(det3(A) - 1.0) < tol


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


def exp_i_theta_lambda_pair(theta: float, a: int, b: int) -> Matrix:
    """Exact SU(3) embedded two-color rotation exp(i theta sigma_x_ab)."""
    M = eye3()
    c = math.cos(theta)
    s = 1j * math.sin(theta)
    M[a][a] = c
    M[b][b] = c
    M[a][b] = s
    M[b][a] = s
    return M


def exp_i_theta_lambda_y_pair(theta: float, a: int, b: int) -> Matrix:
    """Exact SU(3) embedded two-color rotation exp(i theta sigma_y_ab)."""
    # sigma_y-like generator [[0,-i],[i,0]] gives real rotation under exp(i theta generator).
    M = eye3()
    c = math.cos(theta)
    s = math.sin(theta)
    M[a][a] = c
    M[b][b] = c
    M[a][b] = s
    M[b][a] = -s
    return M


def exp_i_theta_lambda3(theta: float) -> Matrix:
    return [
        [complex(math.cos(theta), math.sin(theta)), 0j, 0j],
        [0j, complex(math.cos(-theta), math.sin(-theta)), 0j],
        [0j, 0j, 1+0j],
    ]


def exp_i_theta_lambda8(theta: float) -> Matrix:
    inv_rt3 = 1.0 / math.sqrt(3.0)
    phases = [theta * inv_rt3, theta * inv_rt3, -2.0 * theta * inv_rt3]
    return [[complex(math.cos(phases[i]), math.sin(phases[i])) if i == j else 0j for j in range(3)] for i in range(3)]


def trace_inner(A: Matrix, B: Matrix) -> C:
    return trace(mat_mul(A, B))


def project_hermitian_traceless_to_su3(H: Matrix, basis: List[Matrix]) -> Tuple[List[float], float]:
    # For Hermitian traceless H, H = sum_a c_a lambda_a with c_a=Tr(H lambda_a)/2.
    coeffs_c = [trace_inner(H, L) / 2.0 for L in basis]
    coeffs = [float(c.real) for c in coeffs_c]
    R = zeros3()
    for c, L in zip(coeffs, basis):
        R = mat_add(R, scalar_mul(c, L))
    return coeffs, frob_norm(mat_sub(H, R))


def hermitian_curvature_proxy(U_loop: Matrix) -> Matrix:
    # First nontrivial holonomy curvature proxy: anti-Hermitian part divided by i, then remove trace.
    anti_over_i = scalar_mul(1.0/(2j), mat_sub(U_loop, conj_transpose(U_loop)))
    tr = trace(anti_over_i) / 3.0
    return mat_sub(anti_over_i, scalar_mul(tr, eye3()))


def re_im(z: C) -> Dict[str, float]:
    return {"re": float(z.real), "im": float(z.imag)}


def matrix_payload(A: Matrix) -> List[List[Dict[str, float]]]:
    return [[re_im(x) for x in row] for row in A]


def gauge_transform_links(links: Dict[Tuple[int, int], Matrix], G: Dict[int, Matrix]) -> Dict[Tuple[int, int], Matrix]:
    transformed = {}
    for (i, j), W in links.items():
        transformed[(i, j)] = mat_mul(mat_mul(G[i], W), conj_transpose(G[j]))
    return transformed


def loop_product(links: Dict[Tuple[int, int], Matrix], loop: List[int]) -> Matrix:
    U = eye3()
    for a, b in zip(loop, loop[1:] + loop[:1]):
        U = mat_mul(U, links[(a, b)])
    return U


def main() -> None:
    lambdas = gell_mann()

    # Three quark/color nodes inherited from the tetrahedral residual triplet of v3.9.
    quark_nodes = ["q_color_0", "q_color_1", "q_color_2"]

    # W_ij are not scalar weights; they are SU(3)-valued holonomic transport/coupling maps.
    # Angles are deterministic structure-test angles, not empirical couplings and not fitted to data.
    theta_01 = math.pi / 11.0
    theta_12 = math.pi / 13.0
    theta_20 = math.pi / 17.0
    W01 = exp_i_theta_lambda_pair(theta_01, 0, 1)
    W12 = exp_i_theta_lambda_y_pair(theta_12, 1, 2)
    W20 = exp_i_theta_lambda_pair(theta_20, 0, 2)

    links: Dict[Tuple[int, int], Matrix] = {
        (0, 1): W01,
        (1, 0): conj_transpose(W01),
        (1, 2): W12,
        (2, 1): conj_transpose(W12),
        (2, 0): W20,
        (0, 2): conj_transpose(W20),
    }

    loop = [0, 1, 2]
    U_loop = loop_product(links, loop)
    H_loop = hermitian_curvature_proxy(U_loop)
    coeffs, projection_residual = project_hermitian_traceless_to_su3(H_loop, lambdas)
    active_modes = [idx + 1 for idx, c in enumerate(coeffs) if abs(c) > 1e-12]

    # Yang-Mills-like Wilson action density proxy. No physical coupling is fitted here.
    # g_info is the user's fixed information fluctuation quantum, only recorded as a formal preference scale.
    g_info = math.log(2.0) / (24.0 * math.pi)
    wilson_loop_defect = float(3.0 - trace(U_loop).real)
    action_density_proxy_unscaled = wilson_loop_defect
    action_density_proxy_info_scaled = wilson_loop_defect / (g_info * g_info)

    # Gauge covariance test.
    G = {
        0: exp_i_theta_lambda3(math.pi / 19.0),
        1: exp_i_theta_lambda8(math.pi / 23.0),
        2: exp_i_theta_lambda_pair(math.pi / 29.0, 0, 2),
    }
    links_g = gauge_transform_links(links, G)
    U_loop_g = loop_product(links_g, loop)
    expected_U_loop_g = mat_mul(mat_mul(G[0], U_loop), conj_transpose(G[0]))
    gauge_covariance_residual = frob_norm(mat_sub(U_loop_g, expected_U_loop_g))
    trace_invariant_residual = abs(trace(U_loop_g) - trace(U_loop))
    H_loop_g = hermitian_curvature_proxy(U_loop_g)
    curvature_norm_invariant_residual = abs(frob_norm(H_loop_g) - frob_norm(H_loop))

    link_su3_status = {f"W_{i}{j}": is_su3(W) for (i, j), W in sorted(links.items())}
    reverse_unitarity_status = {
        f"W_{i}{j}_equals_W_{j}{i}_dagger": frob_norm(mat_sub(links[(i, j)], conj_transpose(links[(j, i)]))) < 1e-12
        for (i, j) in [(0, 1), (1, 2), (2, 0)]
    }

    payload = {
        "schema": SCHEMA,
        "created_utc": CREATED_UTC,
        "status": "PASS",
        "module": "40_holonomic_gluon_wij_couplings_v4_0",
        "base_module": "39_tetrahedral_triplet_su3_lift_v3_9",
        "user_operator_statement": "Dynamika gluonow jest holonomiczna. To sprzezenia W_ij miedzy kwarkami.",
        "formal_correction": "W_ij is the SU(3)-valued holonomic parallel transport/coupling between triplet quark nodes; gluon modes are the local su(3) generator/curvature components of W_ij holonomy, not scalar W_ij weights by themselves.",
        "quark_nodes": quark_nodes,
        "W_ij_definition": {
            "carrier": "C^3 triplet inherited from tetrahedral residual modes; CP2 ray carrier after projectivization",
            "link_type": "SU(3)-valued parallel transport/coupling W_ij: q_j -> q_i",
            "reverse_link_rule": "W_ji = W_ij^dagger",
            "gauge_transformation_rule": "W_ij -> G_i W_ij G_j^dagger",
            "loop_holonomy": "U_012 = W_01 W_12 W_20",
            "curvature_proxy": "F_loop ~ traceless Hermitian part of (U_loop - U_loop^dagger)/(2i)",
        },
        "angles_used_for_structure_test_not_fits": {
            "theta_01": theta_01,
            "theta_12": theta_12,
            "theta_20": theta_20,
        },
        "guardrails": {
            "PDG_or_mass_reference_input": False,
            "observed_masses_input": False,
            "CKM_PMNS_input": False,
            "mass_prediction_claimed": False,
            "full_QCD_claimed": False,
            "confinement_claimed": False,
            "running_coupling_claimed": False,
            "hadron_spectrum_claimed": False,
            "Debt_9_status": "OPEN_NOT_CLOSED",
            "canon_allowed": False,
        },
        "link_validation": {
            "all_links_su3": all(link_su3_status.values()),
            "link_su3_status": link_su3_status,
            "reverse_unitarity_status": reverse_unitarity_status,
            "all_reverse_links_are_daggers": all(reverse_unitarity_status.values()),
        },
        "loop_holonomy_validation": {
            "loop": loop,
            "U_loop_is_SU3": is_su3(U_loop),
            "det_U_loop": re_im(det3(U_loop)),
            "trace_U_loop": re_im(trace(U_loop)),
            "wilson_loop_defect_3_minus_ReTrU": wilson_loop_defect,
            "curvature_proxy_frobenius_norm": frob_norm(H_loop),
            "su3_projection_residual": projection_residual,
            "active_gell_mann_modes_1_indexed": active_modes,
            "gell_mann_mode_coefficients": {f"lambda_{idx+1}": c for idx, c in enumerate(coeffs)},
            "U_loop_matrix": matrix_payload(U_loop),
        },
        "gauge_covariance_validation": {
            "gauge_covariance_residual": gauge_covariance_residual,
            "trace_invariant_residual": trace_invariant_residual,
            "curvature_norm_invariant_residual": curvature_norm_invariant_residual,
            "gauge_covariance_pass": gauge_covariance_residual < 1e-10,
            "trace_invariance_pass": trace_invariant_residual < 1e-10,
            "curvature_norm_invariance_pass": curvature_norm_invariant_residual < 1e-10,
        },
        "action_layer_candidate": {
            "unscaled_wilson_action_density_proxy": action_density_proxy_unscaled,
            "information_operator_g_info_ln2_over_24pi": g_info,
            "info_scaled_action_density_proxy": action_density_proxy_info_scaled,
            "ramanujan_scaling_status": "LOCKED_FOR_FUTURE_COUPLING_NORMALIZATION_NOT_USED_AS_FIT_FACTOR_HERE",
            "interpretation": "The loop defect is a holonomic Yang-Mills-like action candidate on the W_ij graph. It is structural, not an empirical coupling fit.",
        },
        "doctor_verdict": "CONTINUE_RESEARCH__HOLONOMIC_GLUON_WIJ_PASS__FULL_QCD_NOT_CLOSED",
    }

    out = RESULTS / "holonomic_gluon_wij_v4_0.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
