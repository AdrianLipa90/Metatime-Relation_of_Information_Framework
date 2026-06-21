#!/usr/bin/env python3
"""
METATIME / Standard Model Derivation v4.1
Holonomic Yang-Mills local connection from W_ij / W_mu(x) couplings.

Scope:
- continues v4.0 W_ij holonomic gluon-coupling layer;
- reinterprets W_ij as local lattice parallel transport W_mu(x) on the triplet carrier;
- extracts a curvature proxy F_mu_nu from plaquette holonomy;
- validates local gauge covariance, Wilson trace invariance, and small-loop scaling;
- no PDG/reference masses, flavour-mixing matrices, NoParamSM, fitted spectra, or mass prediction;
- does not claim confinement, running coupling, hadron spectrum, or full QCD closure.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

CREATED_UTC = "2026-06-20T17:15:00Z"
SCHEMA = "METATIME_SM_HOLONOMIC_YANG_MILLS_LOCAL_CONNECTION_V4_1"
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

C = complex
Matrix = List[List[C]]
Site = Tuple[int, int]
Dir = str


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


def exp_i_theta_pair(theta: float, a: int, b: int, kind: str = "x") -> Matrix:
    """Exact embedded SU(2) rotations inside SU(3). kind='x' uses lambda_x; kind='y' uses lambda_y."""
    M = eye3()
    c = math.cos(theta)
    if kind == "x":
        s = 1j * math.sin(theta)
        M[a][a] = c
        M[b][b] = c
        M[a][b] = s
        M[b][a] = s
    elif kind == "y":
        s = math.sin(theta)
        M[a][a] = c
        M[b][b] = c
        M[a][b] = s
        M[b][a] = -s
    else:
        raise ValueError(kind)
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
    coeffs_c = [trace_inner(H, L) / 2.0 for L in basis]
    coeffs = [float(c.real) for c in coeffs_c]
    R = zeros3()
    for c, L in zip(coeffs, basis):
        R = mat_add(R, scalar_mul(c, L))
    return coeffs, frob_norm(mat_sub(H, R))


def plaquette(links: Dict[Tuple[Site, Dir], Matrix], x: Site, mu: Dir, nu: Dir) -> Matrix:
    dx = {"x": (1, 0), "y": (0, 1)}
    def add_site(s: Site, d: Dir) -> Site:
        return (s[0] + dx[d][0], s[1] + dx[d][1])
    x_mu = add_site(x, mu)
    x_nu = add_site(x, nu)
    W_mu_x = links[(x, mu)]
    W_nu_xmu = links[(x_mu, nu)]
    W_mu_xnu = links[(x_nu, mu)]
    W_nu_x = links[(x, nu)]
    return mat_mul(mat_mul(mat_mul(W_mu_x, W_nu_xmu), conj_transpose(W_mu_xnu)), conj_transpose(W_nu_x))


def curvature_from_plaquette(U: Matrix, area: float) -> Matrix:
    # For U = exp(i area F + ...), Hermitian traceless proxy F ~= (U-U^dagger)/(2 i area), trace removed.
    anti_over_i = scalar_mul(1.0/(2j * area), mat_sub(U, conj_transpose(U)))
    tr = trace(anti_over_i) / 3.0
    return mat_sub(anti_over_i, scalar_mul(tr, eye3()))


def make_constant_links(a: float, alpha: float, beta: float) -> Dict[Tuple[Site, Dir], Matrix]:
    # W_x = exp(i a alpha lambda_1); W_y = exp(i a beta lambda_2). Noncommuting pair creates curvature.
    Wx = exp_i_theta_pair(a * alpha, 0, 1, "x")
    Wy = exp_i_theta_pair(a * beta, 0, 1, "y")
    sites = [(0, 0), (1, 0), (0, 1), (1, 1)]
    links: Dict[Tuple[Site, Dir], Matrix] = {}
    for s in sites:
        links[(s, "x")] = Wx
        links[(s, "y")] = Wy
    return links


def gauge_at(site: Site) -> Matrix:
    m, n = site
    G1 = exp_i_theta_lambda3((m + 2*n + 1) * math.pi / 31.0)
    G2 = exp_i_theta_lambda8((2*m - n + 2) * math.pi / 37.0)
    G3 = exp_i_theta_pair((m - n + 1) * math.pi / 41.0, 0, 2, "x")
    return mat_mul(mat_mul(G1, G2), G3)


def gauge_transform_links(links: Dict[Tuple[Site, Dir], Matrix]) -> Dict[Tuple[Site, Dir], Matrix]:
    dx = {"x": (1, 0), "y": (0, 1)}
    out: Dict[Tuple[Site, Dir], Matrix] = {}
    for (site, direction), W in links.items():
        target = (site[0] + dx[direction][0], site[1] + dx[direction][1])
        out[(site, direction)] = mat_mul(mat_mul(gauge_at(site), W), conj_transpose(gauge_at(target)))
    return out


def matrix_payload(A: Matrix) -> List[List[Dict[str, float]]]:
    return [[{"re": float(x.real), "im": float(x.imag)} for x in row] for row in A]


def scaling_diagnostics(alpha: float, beta: float) -> Dict[str, object]:
    rows = []
    for a in [1e-2, 2e-2, 4e-2, 8e-2]:
        links = make_constant_links(a, alpha, beta)
        U = plaquette(links, (0, 0), "x", "y")
        area = a * a
        F = curvature_from_plaquette(U, area)
        wilson_defect = float(3.0 - trace(U).real)
        action_density = float(0.5 * trace(mat_mul(F, F)).real)
        rows.append({
            "a": a,
            "area": area,
            "wilson_defect_3_minus_ReTrU": wilson_defect,
            "wilson_defect_over_area_squared": wilson_defect / (area * area),
            "curvature_norm": frob_norm(F),
            "action_density_proxy_half_Tr_F2": action_density,
        })
    ratios = []
    for r1, r2 in zip(rows, rows[1:]):
        ratios.append({
            "a_ratio": r2["a"] / r1["a"],
            "wilson_defect_ratio": r2["wilson_defect_3_minus_ReTrU"] / r1["wilson_defect_3_minus_ReTrU"],
            "expected_for_area_squared": (r2["a"] / r1["a"]) ** 4,
            "curvature_norm_ratio": r2["curvature_norm"] / r1["curvature_norm"],
        })
    return {"rows": rows, "ratios": ratios}


def main() -> None:
    lambdas = gell_mann()
    alpha = math.sqrt(2.0) / 7.0
    beta = math.sqrt(3.0) / 11.0
    a = 1e-3
    area = a * a

    links = make_constant_links(a, alpha, beta)
    U = plaquette(links, (0, 0), "x", "y")
    F = curvature_from_plaquette(U, area)
    coeffs, projection_residual = project_hermitian_traceless_to_su3(F, lambdas)
    active_modes = [idx + 1 for idx, c in enumerate(coeffs) if abs(c) > 1e-9]

    links_g = gauge_transform_links(links)
    U_g = plaquette(links_g, (0, 0), "x", "y")
    expected_U_g = mat_mul(mat_mul(gauge_at((0, 0)), U), conj_transpose(gauge_at((0, 0))))
    gauge_covariance_residual = frob_norm(mat_sub(U_g, expected_U_g))
    trace_invariance_residual = abs(trace(U_g) - trace(U))
    F_g = curvature_from_plaquette(U_g, area)
    curvature_norm_invariance_residual = abs(frob_norm(F_g) - frob_norm(F))

    wilson_defect = float(3.0 - trace(U).real)
    action_density = float(0.5 * trace(mat_mul(F, F)).real)
    g_info = math.log(2.0) / (24.0 * math.pi)
    ym_candidate_info_scaled = action_density / (g_info * g_info)

    link_status = {f"W_{site}_{direction}": is_su3(W) for (site, direction), W in sorted(links.items())}
    scaling = scaling_diagnostics(alpha, beta)

    checks = {
        "all_local_links_are_su3": all(link_status.values()),
        "plaquette_is_su3": is_su3(U),
        "curvature_projects_to_su3_basis": projection_residual < 1e-8,
        "nontrivial_curvature": frob_norm(F) > 0.0,
        "gauge_covariance_residual_small": gauge_covariance_residual < 1e-10,
        "wilson_trace_invariant": trace_invariance_residual < 1e-10,
        "curvature_norm_gauge_invariant": curvature_norm_invariance_residual < 1e-8,
        "wilson_defect_positive": wilson_defect > 0.0,
        "action_density_positive": action_density > 0.0,
        "small_loop_scaling_area_squared": all(
            abs(r["wilson_defect_ratio"] / r["expected_for_area_squared"] - 1.0) < 0.01
            for r in scaling["ratios"]
        ),
    }

    payload = {
        "schema": SCHEMA,
        "created_utc": CREATED_UTC,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "lineage": {
            "previous_module": "40_holonomic_gluon_wij_couplings_v4_0",
            "current_module": "41_holonomic_yang_mills_local_connection_v4_1",
            "structural_path": "tetrahedron -> triplet carrier -> CP2/C3 -> SU(3) carrier -> W_ij holonomy -> W_mu(x) local connection -> plaquette curvature -> Yang-Mills-like action candidate",
        },
        "guardrails": {
            "PDG_or_mass_reference_input": False,
            "observed_masses_input": False,
            "flavour_mixing_matrix_input": False,
            "NoParamSM_input": False,
            "mass_prediction_claimed": False,
            "full_QCD_claimed": False,
            "confinement_claimed": False,
            "running_coupling_claimed": False,
            "hadron_spectrum_claimed": False,
            "Debt_9_status": "OPEN_NOT_CLOSED",
            "canon_allowed": False,
            "current_promotion": "DENY_CURRENT",
        },
        "connection_layer": {
            "interpretation": "W_mu(x) is local SU(3) parallel transport inherited from W_ij holonomic quark couplings.",
            "alpha_structure_angle_scale": alpha,
            "beta_structure_angle_scale": beta,
            "a_lattice_test_scale": a,
            "local_links_su3_status": link_status,
            "all_local_links_are_su3": all(link_status.values()),
        },
        "curvature_layer": {
            "plaquette_is_su3": is_su3(U),
            "wilson_trace": {"re": float(trace(U).real), "im": float(trace(U).imag)},
            "wilson_defect_3_minus_ReTrU": wilson_defect,
            "curvature_frobenius_norm": frob_norm(F),
            "su3_projection_residual": projection_residual,
            "active_gell_mann_modes_1_indexed": active_modes,
            "gell_mann_coefficients": coeffs,
            "F_matrix": matrix_payload(F),
        },
        "gauge_covariance_validation": {
            "gauge_covariance_residual": gauge_covariance_residual,
            "trace_invariance_residual": float(abs(trace_invariance_residual)),
            "curvature_norm_invariance_residual": curvature_norm_invariance_residual,
            "gauge_covariance_pass": gauge_covariance_residual < 1e-10,
            "trace_invariance_pass": trace_invariance_residual < 1e-10,
            "curvature_norm_invariance_pass": curvature_norm_invariance_residual < 1e-8,
        },
        "yang_mills_candidate": {
            "action_density_proxy_half_Tr_F2": action_density,
            "information_operator_g_info_ln2_over_24pi": g_info,
            "info_scaled_action_density_proxy": ym_candidate_info_scaled,
            "ramanujan_scaling_status": "LOCKED_FOR_FUTURE_COUPLING_NORMALIZATION_NOT_USED_AS_FIT_FACTOR_HERE",
            "status": "CANDIDATE_LOCAL_ACTION_DENSITY_NOT_FULL_QCD",
        },
        "small_loop_scaling": scaling,
        "checks": checks,
    }
    (RESULTS / "holonomic_yang_mills_local_connection_v4_1.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
