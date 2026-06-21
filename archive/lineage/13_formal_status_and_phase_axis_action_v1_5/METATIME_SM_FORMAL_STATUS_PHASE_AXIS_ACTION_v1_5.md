# METATIME SM FORMAL STATUS AND PHASE-AXIS ACTION v1.5

**Layer status:** canonical working module, appended to the merged repository.

**Repository rule:** this module is not an isolated package. It is a normal directory inside the merged repository. No nested archive is permitted.

## 0. Purpose

This module repairs the derivation discipline after the v1.4 axis update. Every major object must now be assigned an explicit formal status:

- **Definition**: a fixed symbolic or mathematical convention.
- **Ansatz**: a chosen structural form that is not yet proven from earlier layers.
- **Lemma**: a conditional statement derived from previous definitions or ansätze.
- **Proof**: a formal derivation of a lemma or proposition.
- **Interpretation**: physical, geometric, or conceptual reading of a formal result.
- **Hypothesis**: a stronger claim not yet validated or not yet derived.
- **Validation gate**: executable or algebraic check that must pass before promotion.
- **Formal debt**: required missing derivation, missing proof, or missing validation.

The immediate physics target is to keep the v1.4 correction intact:

1. tetrahedral depth precedes the Poincaré disk;
2. the Poincaré disk carries the subsequent arithmetic/orbital dynamics;
3. the Collatz terminal axis is not merely `4 -> 2 -> 1`; it is the transition axis `4 -> 2 -> 1 -> 1/2`;
4. `1/2` is the spin/projection bridge;
5. the zeta structure sits on the imaginary zero axis at the transition place rather than entering as a raw mass cost.

## 1. Definitions

### Definition 1.1 — projective spin transition point

Let the terminal Collatz cycle be the ordinary discrete cycle

```text
4 -> 2 -> 1 -> 4
```

The Metatime transition axis introduces the projective terminal point

```text
4 -> 2 -> 1 -> 1/2
```

where `1/2` is not an integer Collatz iterate. It is the spin-projection bridge where the discrete arithmetic terminal cycle is mapped into the spinorial phase sector.

### Definition 1.2 — zeta imaginary zero axis

The zeta axis is placed at the critical real coordinate `1/2` and carries imaginary zero data:

```text
s_zeta = 1/2 + i gamma_n,  zeta(s_zeta) = 0.
```

This axis is not a raw additive mass cost. It is a spectral phase-coherence axis.

### Definition 1.3 — tetrahedral depth before Poincaré disk

A regular tetrahedral frame inside the Bloch ball is the internal depth frame. The Poincaré disk used by the subsequent Collatz/Kepler dynamics is derived from this tetrahedral depth, not postulated as an independent background.

### Definition 1.4 — status-tagged derivation object

Every derivation object in this repo should be represented as a record:

```json
{
  "id": "...",
  "status": "definition | ansatz | lemma | proof | interpretation | hypothesis | validation_gate | formal_debt",
  "statement": "...",
  "dependencies": ["..."],
  "promotion_rule": "..."
}
```

## 2. Ansatz layer

### Ansatz 2.1 — phase-axis action decomposition

The full charged-fermion mass-action layer is treated as a structured action with distinct kinds of terms:

1. generational arithmetic-orbital action;
2. tetrahedral/Poincaré depth action;
3. chiral transition admissibility;
4. representation-sector cost;
5. zeta-axis coherence;
6. Euler--Berry constructive coherence.

The zeta-axis term is not allowed to enter as an unrestricted positive damping term unless a later proof shows that this preserves the validated generational ordering.

### Ansatz 2.2 — Collatz terminal projection

The terminal arithmetic structure `4 -> 2 -> 1` is projected to spin/projection coordinate `1/2`. This projection is a formal bridge from integer iteration to spinorial phase closure.

### Ansatz 2.3 — zeta axis as coherence rather than damping

The zeta contribution is modeled as a coherence gate or alignment factor acting at the imaginary zero axis. It may enhance or suppress admissibility through phase alignment, but it is not assumed to increase mass-action monotonically.

## 3. Lemmas and proofs

### Lemma 3.1 — representation data alone cannot distinguish generations

**Statement.** Standard Model representation data distinguish sector type but do not distinguish generation index.

**Proof.** Within one charged fermion class, the three generations share the same gauge representation. The charged lepton class has identical color, weak-isospin structure, and hypercharge across electron, muon, and tau. The same holds for up-type quarks across up, charm, top and for down-type quarks across down, strange, bottom. Therefore a function depending only on gauge representation must assign the same value to all three generations within a class. Such a function cannot produce a strict three-generation hierarchy. QED.

### Lemma 3.2 — zeta as raw damping is not validated

**Statement.** The zeta-tetrahedral layer cannot be promoted as a raw additive damping cost at v1.5.

**Proof.** In v1.1/v1.3 checks, direct addition of the raw zeta-tetrahedral contribution disrupted the generational ordering preserved by the structural action layers. A term that destroys the previously validated ordering cannot be promoted as a canonical additive cost. The weaker role as a coherence gate remains admissible because it does not assume monotonic damping. QED.

### Lemma 3.3 — the `1/2` transition point is not a Collatz integer iterate

**Statement.** The terminal point `1/2` in the sequence `4 -> 2 -> 1 -> 1/2` is a projection bridge, not an ordinary Collatz step.

**Proof.** The ordinary Collatz map sends odd `1` to `4`, not to `1/2`. Therefore `1 -> 1/2` is not a step of the standard Collatz map. In this model it is a separate projection from the arithmetic terminal node to the spinorial half-axis. QED.

### Lemma 3.4 — the zeta axis and spin axis share the critical half-coordinate

**Statement.** The spin-projection bridge and the zeta critical line share the real coordinate `1/2`.

**Proof.** The spin transition bridge is explicitly defined at the coordinate `1/2`. The non-trivial zeta zero axis used in the model is placed at critical real coordinate `1/2` with imaginary coordinate `gamma_n`. Hence both axes share the same real coordinate while differing in the additional structure: spin projection versus imaginary spectral zero data. QED.

## 4. Interpretation layer

### Interpretation 4.1 — why the half-axis matters

The half-axis is the place where integer arithmetic dynamics stops being treated as a closed integer orbit and becomes a phase/spin transition. This allows the terminal Collatz attractor to be connected to spin one-half and to the critical zeta line without pretending that `1/2` is a standard Collatz iterate.

### Interpretation 4.2 — why zeta is placed, not added

The zeta structure should be understood as a spectral axis placed at the transition site. It supplies imaginary zero data and phase-coherence structure. It should not be treated as another arbitrary scalar cost appended to the mass formula.

### Interpretation 4.3 — why tetrahedra precede the disk

The disk is not the first geometric object. Tetrahedral depth supplies internal geometry inside the Bloch ball. The disk is then extracted as a working surface for hyperbolic/orbital dynamics. This order prevents the Poincaré disk from being an unsupported assumption.

## 5. Hypotheses not yet promoted

### Hypothesis 5.1 — exact mass prediction from the full action

The full action may predict charged fermion mass ratios once the zeta-axis coherence and Euler--Berry constructive coherence are canonically fixed. This is not yet proven.

### Hypothesis 5.2 — three generations from minimal admissible seed triplet

The three Standard Model generations may correspond to the minimal admissible twin-prime seed triplet after full phase-axis arbitration. This is not yet proven.

### Hypothesis 5.3 — zeta imaginary zero ordering as spectral generation selector

The imaginary zero data may select or stabilize generational sectors through phase coherence. This is not yet proven.

## 6. Validation gates

### Gate 6.1 — no nested archive invariant

The repository must contain no `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.rar`, `.7z`, `.gz`, `.bz2`, or `.xz` archive files inside the merged repository tree.

### Gate 6.2 — no mass-as-input gate

Scripts that claim structural mass-action validation must not use observed fermion masses as predictors or fitted inputs. Observed masses may appear only as validation targets.

### Gate 6.3 — status ledger gate

Every promoted statement in new modules must be classed as definition, ansatz, lemma, proof, interpretation, hypothesis, validation gate, or formal debt.

### Gate 6.4 — Collatz-axis gate

Any module that uses the terminal Collatz axis must distinguish the ordinary integer cycle from the projective spin transition to `1/2`.

### Gate 6.5 — zeta-axis gate

Any module that uses zeta data must state whether zeta is being used as coherence, damping, spectral labeling, or validation target. Raw additive damping is blocked unless proven safe.

## 7. Formal debts

1. Define the exact map from zeta imaginary zero data to tetrahedral vertex weights.
2. Define the Euler--Berry constructive coherence functional.
3. Determine whether the full phase-axis action predicts mass ratios without fitted mass inputs.
4. Derive the final seed-to-generation assignment after zeta coherence is promoted.
5. Extend the formalism to neutrino masses and mixing without confusing oscillation phase with charged-fermion mass hierarchy.
6. Derive or reject additional generation suppression for twin-prime candidates beyond the minimal triplet.

## 8. Repository promotion rule

This v1.5 module does not claim final Standard Model mass prediction. It promotes only the formal-status discipline and the corrected axis ordering:

```text
zeta imaginary axis / critical half coordinate
        -> tetrahedral depth
        -> Poincaré disk
        -> Collatz / Fibonacci / Kepler dynamics
        -> terminal Collatz cycle
        -> projective half-axis
        -> spin and Euler--Berry phase closure
```

The next module should build the Euler--Berry coherence functional as a status-tagged object with explicit distinction between definitions, ansätze, lemmas, proofs, interpretations, hypotheses, validation gates, and formal debts.
