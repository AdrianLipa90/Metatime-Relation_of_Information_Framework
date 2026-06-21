# METATIME Standard Model Derivation — Euler--Berry Coherence Gate v1.3

## Status

This stage is a direct continuation of the merged repository line. It is not a standalone package and must not be treated as a separate canonical repository. It adds the missing Euler--Berry coherence arbitration layer after the zeta--tetrahedral anchor stage.

## Purpose

Stage v1.1 established a technical map from zeta zeros to tetrahedral weights, but it also showed that the zeta layer must not be inserted as a naive additive mass damping term. A direct additive insertion can disturb the generation ordering already obtained by the tetrahedral/Poincare/Collatz/Fibonacci/Kepler kernel.

The present stage therefore reclassifies the zeta--tetrahedral layer as a bounded Euler--Berry coherence gate:

\[
Z_{\rm tet}\neq {\rm additive\ mass\ cost}.
\]

Instead, it acts as a phase-coherence certification/credit layer:

\[
Z_{\rm tet}\rightarrow C^{\rm EB}_{\zeta}.
\]

The gate is mass-blind: no observed fermion mass is used to construct the coherence score or to select the generation ordering.

## Inputs

The stage uses only internal outputs already present in the merged repository:

- `seed_arbitration_v1_0.csv`
- `charged_fermion_action_assembly_v1_0.csv`
- `seed_zeta_tetrahedral_table_v1_1.csv`

No PDG/observed mass values are used as inputs.

## Coherence features

For every seed \(s=(p,p+2)\), the gate builds the following zeta--tetrahedral coherence features:

\[
E_s={\rm zeta\ entropy},
\]

\[
V_s=1-{\rm vertex\ asymmetry},
\]

\[
B_s={\rm normalized\ base\ balance},
\]

\[
P_s={\rm phase\ winding\ alignment},
\]

\[
A_s={\rm apex\ alignment}.
\]

The composite coherence score is:

\[
C^{\rm EB}_{\zeta}(s)
=\frac{1}{5}\left(E_s+V_s+B_s+P_s+A_s\right).
\]

This is not interpreted as a new damping action by itself. It is a bounded coherence modifier.

## Bounded credit rule

Let \(S_s^{(1.0)}\) be the structural generation action obtained in v1.0. Define the smallest action margin between adjacent generation seeds:

\[
\Delta_{\min}=
\min_i |S_{s_i}^{(1.0)}-S_{s_{i+1}}^{(1.0)}|.
\]

The zeta coherence modifier is capped by:

\[
|\delta S^{\rm EB}_{\zeta}(s)|\leq \frac{1}{4}\Delta_{\min}.
\]

This rule is deliberately conservative. It allows zeta to improve or degrade phase coherence, but forbids it from overturning the previously derived structural generation order.

The coherence-corrected action is:

\[
S_{f}^{(1.3)}=S_f^{(1.0)}+\delta S^{\rm EB}_{\zeta}(s_f).
\]

The physical meaning is:

\[
S_{\rm mass}=S_{\rm generation}+S_{\rm chiral}+S_{\rm representation}+\delta S_{\rm coherence}+\cdots
\]

where the ellipsis still contains not-yet-closed layers: full Euler--Berry constructive interference, mixing, neutrino sector, and final numeric mass law.

## Validation result

The coherence gate preserves the generation ordering across the charged fermion classes:

- charged leptons: pass;
- down-type quarks: pass;
- up-type quarks: pass.

The resulting seed order remains:

1. first generation: seed `3--5`;
2. second generation: seed `5--7`;
3. third generation: seed `11--13`.

This is an ordinal structural validation only. It is not a numerical mass prediction.

## Generated outputs

- `results/seed_coherence_gate_v1_3.csv`
- `results/charged_fermion_action_with_coherence_v1_3.csv`
- `results/coherence_validation_summary_v1_3.json`
- `results/eulerberry_coherence_gate_run_v1_3.json`

## Validation gates

| Gate | Status | Meaning |
|---|---:|---|
| no observed masses as inputs | PASS | mass data remain validation targets only |
| zeta not used as naive additive cost | PASS | zeta is treated as a coherence gate |
| bounded coherence correction | PASS | correction cannot overturn generation order |
| charged lepton ordinal hierarchy | PASS | first > second > third action |
| down-type quark ordinal hierarchy | PASS | first > second > third action |
| up-type quark ordinal hierarchy | PASS | first > second > third action |
| numeric mass prediction | NOT CLAIMED | requires final mass law |

## Canonical decision

Stage v1.3 freezes the following rule:

> The zeta--tetrahedral layer is an Euler--Berry coherence gate, not a primitive additive mass cost.

This corrects the v1.1 warning and allows the zeta layer to remain part of the derivation without corrupting the generation hierarchy.
