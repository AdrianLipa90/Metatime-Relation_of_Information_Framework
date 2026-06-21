# METATIME SM — Debt 9 One-Anchor Mass Scaling Pilot v2.6

## Status

- **Module type:** computational stress test / one-anchor scaling pilot.
- **Debt:** Debt 9 — exact mass-ratio layer.
- **Canonical status:** **not closed**; this is a controlled first attempt.
- **Gate type:** `COMPUTATIONAL_STRESS_TEST_PASS`, not `NUMERIC_MASS_DERIVATION_PASS`.
- **Observed masses used as model inputs:** exactly one, the electron mass.
- **Observed masses used as validation targets only:** muon, tau, up, down, strange, charm, bottom, top.
- **Ramanujan layer:** mandatory.
- **Zeta-Heisenberg layer:** uncertainty/coherence width, not a fitted knob.

## Executive result

This module converts Debt 9 from an open idea into a reproducible one-anchor test.

The result is useful but not yet a mass derivation:

1. The pipeline accepts exactly one dimensional mass anchor.
2. The anchor is excluded from prediction scoring.
3. Ramanujan scaling improves the stress-test residuals compared with the Euler-Berry-only variant.
4. The three generation orders are preserved inside charged leptons, down-type quarks, and up-type quarks.
5. The actual numerical ratios are still far from the observed charged-fermion spectrum.

Therefore Debt 9 is **partially advanced, not closed**.

## Source dependencies

- v1.6 charged-fermion Euler-Berry action table.
- v2.1 Ramanujan seed suppression table.
- v2.0 preference / zeta-Heisenberg fluctuation table.
- v0.1 validation target table for charged fermions.
- v2.5 old-document audit, which identified one-anchor scaling as the cleanest Debt 9 route.

## [DEFINITION] One-anchor mass-scale calibration

A one-anchor mass calibration is a map in which exactly one observed Standard Model mass is allowed to set the dimensional unit of the model. In this first pass the anchor is the electron mass.

The electron is not counted as a prediction. Every other charged fermion is scored as a ratio to the electron anchor.

## [ANSATZ] Electron as first dimensional anchor

The electron is chosen for the first pass because it is stable, precise, charged, light, and not dominated by QCD binding. This is an ansatz, not a proof that the electron is the unique correct anchor.

Later passes may test a different single anchor, but choosing an anchor by minimizing global error would be a fit and must be marked as such.

## [DEFINITION] Structural suppression score

The v2.x action produces a structural suppression score. In this pilot the score is built from:

1. the Euler-Berry action inherited from v1.6;
2. a Ramanujan release term inherited from v2.1;
3. a zeta-Heisenberg central fluctuation inherited from v2.0.

The preference constant is

\[
\kappa_I = \frac{\ln 2}{24\pi}.
\]

The mass is converted through the usual effective Yukawa-style suppression form

\[
y_f = \exp(-S_f/\kappa_I), \qquad m_f = \frac{v}{\sqrt{2}}y_f.
\]

This is a test harness. It does not claim that the final mass operator must have exactly this suppression form.

## [LEMMA] One-anchor scoring separates scale from ratios

If one mass is used only to set the absolute scale, then all non-anchor masses are ratio tests.

### Proof

Let the anchor be `a`. The observed value of `m_a` fixes the dimensional unit or equivalently fixes `S_a`. For any other fermion `f`, the prediction depends only on the structural difference between `S_f` and `S_a`. Therefore the non-anchor masses are not independent input constants; they are validation targets.

This is a formal accounting lemma, not a numerical success claim.

## [ANSATZ] Ramanujan release term

The Ramanujan term is introduced as a non-fit structural release term. Higher-generation seed structure may reduce the effective suppression relative to the first-generation anchor. In the pilot this enters through the already computed Ramanujan seed table:

\[
S_f^{(R)} = S_f^{(EB)} - (R_f - R_e).
\]

This is an ansatz. Its value is not selected from masses.

## [ANSATZ] Zeta-Heisenberg central correction and width

The zeta-Heisenberg layer is not used as a fitted correction. It supplies:

1. a small central phase correction inherited from zeta-zero spacing diagnostics;
2. an uncertainty/coherence width around the mass estimate.

If future work tunes this width to cover observed masses, that would become a fit and must be marked as such. This module does not tune it.

## [COMPUTATIONAL RESULT] Variants tested

Three variants were tested:

1. `EB_ONLY` — electron-anchored Euler-Berry action only.
2. `EB_MINUS_RAMANUJAN` — Euler-Berry plus Ramanujan release.
3. `EB_MINUS_RAMANUJAN_ZH_CENTER` — previous variant plus central zeta-Heisenberg correction.

The best current variant is the third one by median log-error, but it is only marginally better than the Ramanujan variant.

| Variant | Median absolute log-error excluding anchor | Max absolute log-error excluding anchor | Generation-order gates |
|---|---:|---:|---|
| EB_ONLY | 3.761700 | 7.337475 | pass in three charged sectors |
| EB_MINUS_RAMANUJAN | 2.629441 | 5.370477 | pass in three charged sectors |
| EB_MINUS_RAMANUJAN_ZH_CENTER | 2.628912 | 5.370477 | pass in three charged sectors |

## [INTERPRETATION]

The one-anchor strategy is valuable because it cleanly separates the absolute scale problem from the ratio problem. The current v2.x structural action already preserves the ordinal hierarchy inside the three charged sectors. Ramanujan improves the residuals substantially relative to the Euler-Berry-only stress test.

However, the action does not yet have enough dynamic range to reproduce the charged-fermion ratios. Heavy fermions remain too light in the pilot, and first-generation quark ordering still needs a more precise representation/QCD projection layer.

## [HIPOTEZA]

The missing dynamic range is likely not solved by adding another free coefficient. It likely belongs to one or more of these structural debts:

1. a refined representation table from the CP1/chiral axis;
2. a QCD/color projection for quark masses;
3. a stronger old-source eigenvalue layer from Collatz orbit lengths;
4. CKM/white-thread holonomic corrections for off-diagonal mixing;
5. a Ramanujan modular scaling layer that is not merely the seed suppression layer.

## [VALIDATION GATE]

The module passes as a computational stress test because:

- the script runs reproducibly;
- the anchor policy is enforced;
- observed masses other than the electron are not used as inputs;
- Ramanujan and zeta-Heisenberg inputs are read from previous non-mass-fitted v2.x modules;
- all output tables are generated from code.

It does not pass as a numerical mass derivation.

## [DO NOT CLAIM]

Do not claim:

- that Debt 9 is closed;
- that charged-fermion masses are numerically derived;
- that Yukawa couplings have been derived;
- that CKM or PMNS mixing has been derived here;
- that quark running/scheme dependence is solved.

## Files

- `scripts/debt9_one_anchor_scaling_v2_6.py`
- `results/one_anchor_mass_scaling_predictions_v2_6.csv`
- `results/one_anchor_mass_scaling_summary_v2_6.csv`
- `results/debt9_status_update_v2_6.json`
- `results/debt9_one_anchor_scaling_run_v2_6.json`
- `schemas/DEBT9_ONE_ANCHOR_SCHEMA_v2_6.json`
