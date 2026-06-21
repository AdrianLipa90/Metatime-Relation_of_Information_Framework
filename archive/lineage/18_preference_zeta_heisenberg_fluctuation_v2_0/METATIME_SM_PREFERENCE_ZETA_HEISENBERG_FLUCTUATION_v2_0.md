# METATIME / Standard Model Derivation — Preference Operator and Zeta-Heisenberg Fluctuation Kernel v2.0

## NOEMA_STATUS

- `sot_available`: false
- `source_tree`: local merged repository v1.9 copied into v2.0
- `write_mode`: append-only repository update
- `archive_policy`: no nested archives inside repository
- `mass_fit_policy`: forbidden at this stage
- `formal_status_policy`: every new object is marked as Definition, Ansatz, Lemma, Proof, Interpretation, Hypothesis, Validation Gate, or Formal Debt

## Purpose

This module repays the next derivational debt introduced by the user's correction:

> Preference is controlled by the information operator scale `ln(2)/(24*pi)`, and the zeta axis must carry a Heisenberg-like fluctuation channel.

The module therefore separates four layers that must not be conflated:

1. the fixed information-preference scale;
2. the Killing-generator polar axis on the Bloch sphere;
3. the zeta imaginary-zero axis placed at the spin-half transition point;
4. a bounded zeta-Heisenberg fluctuation around that axis.

The fluctuation is not a fitted mass parameter. It is a phase-uncertainty channel constrained by the zeta axis and by the fixed information scale.

---

## [DEFINITION] Information Preference Scale

Let

```math
\kappa := \frac{\ln 2}{24\pi}.
```

This is the dimensionless information-preference scale used by the phase-action kernel. It is fixed and is not a fit parameter.

### Role

The scale `kappa` controls the cost-to-preference conversion. Lower action is preferred, but the preference is not free: it must be measured in units of `kappa`.

---

## [DEFINITION] Preference Functional

For a candidate state vector `V_f` and an Euler-Berry action candidate `S_EB(V_f)`, define a structural preference score by

```math
\mathcal P_\kappa(V_f) := \exp\left[-\frac{\mathcal S^{EB}(V_f)}{\kappa}\right].
```

This is not yet a mass prediction. It is a ranking functional for allowed structural trajectories.

---

## [LEMMA] Preference Cannot Replace the Action

The preference functional can only rank already constructed action candidates. It cannot define the action by itself.

### Proof

If `S_EB` is unknown, then `P_kappa` has no argument. The fixed scale `kappa` therefore supplies a unit of preference, not a substitute for the missing Euler-Berry action. Thus the derivation still requires the geometric action functional assembled from representation, chirality, tetrahedral depth, Collatz dynamics, Fibonacci rhythm, Kepler orbital phase, zeta coherence, and the Killing-generator polar axis.

---

## [DEFINITION] Zeta Imaginary-Zero Axis

The zeta axis is placed at the critical real coordinate `1/2` and is treated as an imaginary ordinate axis:

```math
s_\zeta(n) = \frac12 + i\gamma_n,
```

where `gamma_n` labels non-trivial zero ordinates.

This axis is not a new pole pair. It labels the already existing north-south Killing fixed-point pair by a spectral imaginary coordinate.

---

## [DEFINITION] Collatz Terminal Transition Axis

The terminal Collatz channel is not treated as ordinary arithmetic termination only. It is lifted to the transition axis

```text
4 -> 2 -> 1 -> 1/2.
```

The final `1/2` is not a Collatz iterate. It is the projection point into the spin-half and zeta-critical axis.

---

## [ANSATZ] Zeta-Heisenberg Fluctuation

A zeta-Heisenberg fluctuation is introduced as a bounded uncertainty around the zeta imaginary axis:

```math
\delta_{\zeta H}(s,k)
```

subject to the structural lower bound

```math
\Delta\theta_\zeta\,\Delta n_\zeta \geq \frac{\kappa}{2}.
```

Here `Delta theta_zeta` is the phase uncertainty induced by zeta-axis spacing and `Delta n_zeta` is the index uncertainty along the zeta-zero sequence.

This is a dimensionless Heisenberg-like bound. It is not the physical canonical commutator `Delta x Delta p >= hbar/2`; it is a phase-index uncertainty gate in the model's internal spectral axis.

---

## [INTERPRETATION] Why This Matters

The zeta axis must not be added as a raw positive mass cost. Earlier tests showed that doing this can destroy the generation ordering. Therefore zeta belongs primarily to the coherence layer.

The zeta-Heisenberg fluctuation supplies a controlled reason why the zeta axis does not collapse into a deterministic, arbitrary lookup table. It permits bounded phase uncertainty while preserving the fixed information-preference scale.

---

## [HYPOTHESIS] Preference-Fluctuation Coupling

The candidate preference-corrected action is organized as:

```math
\mathcal S^{EB}_{\mathrm{pref}}(V_f)
=
\mathcal S^{EB}_{\mathrm{struct}}(V_f)
+
\delta_{\zeta H}(V_f)
-
\Omega_{\zeta EB}(V_f).
```

- `S_EB_struct` is the structural action assembled from prior modules.
- `delta_zetaH` is bounded fluctuation.
- `Omega_zetaEB` is constructive Euler-Berry coherence.

This is not yet a numerical mass law. It is the next controlled form of the mass-action debt.

---

## [VALIDATION GATE] No Mass Input

The zeta-Heisenberg fluctuation kernel is valid only if:

1. it uses no observed charged-fermion masses as inputs;
2. it does not tune `kappa`;
3. it treats zeta as coherence/fluctuation, not as a raw cost;
4. it preserves the Killing-generator polar pair;
5. it preserves the Collatz terminal transition axis `4 -> 2 -> 1 -> 1/2`;
6. it does not introduce additional arbitrary generation poles.

---

## [FORMAL DEBT] Remaining Work

The following debts remain open after v2.0:

1. derive the weak-isospin axis from first principles rather than treating it as canonical ansatz;
2. prove the zeta-to-tetrahedral map rather than using an operational ansatz;
3. build the final `S_EB(V_f)` that predicts mass ratios without mass inputs;
4. derive CKM and PMNS mixing as relative holonomies;
5. close the neutrino mass sector;
6. prove suppression of additional twin-prime candidates outside the three-generation sector.

---

## [RESULT] Status of v2.0

The module does not claim numerical masses. It repays a structural debt: preference is now tied to the fixed information scale `ln(2)/(24*pi)`, and the zeta axis now carries a bounded Heisenberg-like fluctuation channel rather than a free parameter or raw cost.
