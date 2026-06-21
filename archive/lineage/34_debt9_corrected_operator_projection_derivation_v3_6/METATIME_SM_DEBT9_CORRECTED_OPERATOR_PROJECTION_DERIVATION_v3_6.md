# METATIME SM — Debt 9 Corrected Operator Projection Derivation v3.6

Created UTC: 2026-06-20T08:46:18Z  
Status: correction module  
Repo relation: append-only after v3.5  
Noema SoT: unavailable  
Observed masses used: no  
CKM/PMNS used: no  
Old fitted White-Thread values used: no  
Old tau/eigenvalue table imported: no  

---

## 0. Red status

**SUBSTANTIVE STATUS: Debt 9 remains OPEN.**

This module does **not** claim a numerical mass derivation.

It corrects a structural error detected by the v3.2 failure:

> A representation/sector projection operator must not be injected as a scalar additive correction into the mass action.

The catastrophic v3.2 scatter is treated as a falsification of the scalar-projection path, not as a tuning target.

---

## 1. Failure being corrected

### [FACT]

v2.6 used a clean one-anchor mass test. It was anti-leak and methodologically useful, but numerically insufficient.

### [FACT]

v3.2 tested the frozen v3.1 sector projection as a scalar correction/orientation to the one-anchor mass action. The result was a catastrophic numerical degradation.

### [INTERPRETATION]

The failure occurred because an operator-level object was compressed into a scalar action component and then passed through the exponential mass map. Since the information quantum is small, scalarizing an order-one projection creates an enormous logarithmic shift.

### [DO NOT CLAIM]

Do not claim that v3.2 disproves the full sector-projection program.

It disproves the use of the frozen sector projection as a naive scalar mass correction.

---

## 2. Corrected derivation layer

### [DEFINITION] State before mass

A fermion is represented not only by a scalar action but by a state in a sector basis:

- CP1/Bloch pole channel,
- chirality channel,
- representation channel,
- color/tetrahedral channel,
- seed/orbit channel,
- zeta-axis coherence channel,
- Ramanujan scaling channel,
- information-preference fluctuation channel.

The pre-mass object is therefore a structured state, not a scalar.

### [DEFINITION] Projection operator

The sector-basis projection operator acts on the pre-mass state. It selects or rotates a channel. It is not itself a mass action.

### [LEMMA] Scalar injection failure

If an operator-valued projection is collapsed to a scalar and added directly to the mass action, the exponential mass map amplifies the collapse error.

### [PROOF SKETCH]

The mass map is logarithmic/exponential in the effective action. The action unit is controlled by the information quantum. A projection scalar of ordinary size, when divided by the small information quantum, creates a large logarithmic displacement. This explains why v3.2 failed by many orders of magnitude.

### [CORRECTION]

The corrected path is:

```text
structured fermion state
  -> sector-basis projection operator
  -> White-Thread open holonomy / relative basis map
  -> expectation or spectral phase in the selected channel
  -> effective action
  -> one-anchor mass map
```

Not:

```text
scalar action + scalar projection -> mass
```

---

## 3. Operator information role

### [DEFINITION]

The information operator is the quantum of informational preference fluctuation.

It must act on a channel/state, not merely multiply a scalar residual.

### [CONSTRAINT]

The information quantum may scale a fluctuation spectrum or an expectation value after projection. It must not be used as a free fitting knob.

---

## 4. White-Thread role

### [DEFINITION]

White-Thread is an open holonomy between sector bases.

For CKM it should mediate the relative orientation between up and down bases.

For masses it should provide a channel-dependent expectation/spectral phase, not a scalar offset.

### [QUARANTINE]

Old numerical White-Thread constants remain quarantined unless rederived independently of observed masses and CKM/PMNS data.

---

## 5. Corrected mass pipeline

### [ANSATZ — corrected, not yet proven]

For a fermion state and a sector projection operator, define an effective channel object by applying the projection to the state.

Then the mass action must be derived from an allowed scalarization of that channel object, such as:

- an expectation value of a Hermitian effective action operator,
- a spectral phase,
- a relative holonomy phase,
- or a norm/defect that is derived from the operator structure.

The scalarization rule must be frozen before comparison with observed masses.

### [VALIDATION REQUIREMENT]

A valid future v3.7+ mass test must satisfy:

1. no additional mass anchor beyond the declared one,
2. no CKM/PMNS values as input,
3. no old fitted tau/eigenvalue table as input,
4. no tuned Ramanujan coefficient,
5. no widened zeta-Heisenberg band fitted to targets,
6. scalarization rule frozen before residuals are computed,
7. report starts with substantive status before artifacts.

---

## 6. Immediate consequence

### [RESULT]

v3.2 failure is now classified as:

```text
TECHNICAL PASS
ANTI-FIT PASS
NUMERIC FAIL
SCALAR-PROJECTION PATH FALSIFIED
```

### [RESULT]

v3.3–v3.5 are valid as preparatory structural repairs, not as mass or CKM derivations.

### [OPEN DEBT]

Debt 9 remains open until a frozen operator-level scalarization rule is derived and passes a one-anchor stress test.

---

## 7. Next module recommendation

The next module should not rescore masses immediately.

The next module should define and freeze one candidate scalarization rule:

```text
operator-projected channel -> effective action
```

Possible candidates:

1. expectation value of an effective action operator,
2. Berry/Euler phase defect after White-Thread transport,
3. spectral gap between sector-projected eigenchannels,
4. Ramanujan-weighted information fluctuation norm.

Only after that rule is frozen should the one-anchor mass test be repeated.
