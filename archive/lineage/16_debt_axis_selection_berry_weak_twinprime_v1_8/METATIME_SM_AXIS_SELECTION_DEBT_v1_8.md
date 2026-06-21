# METATIME Standard Model Derivation — Physical Axis Selection Debt v1.8

## Status classification

- **Debt addressed:** physical axis selection after Debt 1.
- **Debt relation:** Debt 1 fixed the primitive generator as a Killing-flow generator on the Bloch/Fubini--Study sphere. This module addresses the remaining question: which physical axis selects that generator.
- **Status:** conditionally closed as a canonical working ansatz plus validation gates.
- **Closure class:** definition + lemma + proof for role separation; ansatz for canonical physical selection; interpretation for Berry/twin-prime/zeta use; validation gate for future modules.
- **Non-claim:** this module does not prove numerical masses or mixing matrices.

---

## 1. [DEFINITION] Three axis-like structures are distinct

Debt 1 left three candidates:

1. Berry phase axis.
2. Weak-isospin axis.
3. Twin-prime-selected axis.

This module defines them as different logical objects:

- the **weak-isospin axis** selects the physical quantization doublet and therefore selects which two polar states carry the Standard Model weak doublet structure;
- the **Berry axis/connection** transports phase around the selected Bloch/Fubini--Study geometry and measures geometric phase;
- the **twin-prime sector** indexes a generation/sector and modulates downstream dynamics, but must not arbitrarily choose two unrelated poles.

Thus the three structures are not interchangeable.

---

## 2. [LEMMA] The weak-isospin axis is the only candidate compatible with the gauge skeleton

For the Standard Model derivation, the pole pair must remain universal for all members of a weak doublet.  If the pole pair were chosen independently by a twin-prime sector for each fermion, the weak doublet structure would become generation-dependent at the primitive axis level.

### [PROOF]

The previously frozen gauge skeleton requires a universal left weak-doublet action.  A left doublet must share one weak quantization structure before mass splitting and generation-specific action are applied.

If the primitive Killing axis were chosen independently by the twin-prime seed, then the weak doublet would not be selected by a single gauge-axis structure.  That would turn the generation index into a primitive weak-axis selector and would blur the distinction between weak representation and generation vector.

The mass-vectorization layer already separates:

- representation vector,
- chiral bridge,
- generation vector,
- zeta/tetrahedral layer,
- Euler--Berry coherence.

Therefore the primitive Standard Model axis must be the weak-isospin quantization axis, while the twin-prime seed enters downstream as a sector/generation index.

This preserves the gauge skeleton and avoids collapsing the generation layer into the gauge layer.

---

## 3. [LEMMA] Berry supplies transport, not independent pole selection

The Berry connection on the projective state space measures phase transport along paths.  It can be locked to the chosen axis, but it should not be treated as a second independent selector of the two polar states.

### [PROOF]

The polar states were already fixed by the zero set of a Killing field.  Berry phase arises from parallel transport around loops in projective state space.  If Berry were used as an independent pole selector, the model would contain two independent mechanisms selecting the same north/south pair.

Instead, Berry should be treated as the geometric phase connection associated with transport around the weak-isospin-selected polar axis.

Thus Berry is a phase-transport layer over the axis, not an independent source of pole count.

---

## 4. [ANSATZ] Canonical axis-selection rule

The canonical working ansatz is:


a. the primitive Killing generator is selected by the weak-isospin quantization axis;

b. the Berry connection supplies geometric phase transport around that axis;

c. the twin-prime sector selects the generational/arithmetical sector and downstream Collatz/Fibonacci/Kepler dynamics;

d. the zeta-polar map is constrained to the north/south fixed pair of the same weak-isospin Killing field.

Equivalently:

- **axis:** weak-isospin/Bloch quantization axis;
- **connection:** Berry/Fubini--Study phase transport;
- **sector index:** twin-prime seed;
- **spectral anchor:** zeta imaginary-zero axis constrained by the polar pair.

This is the canonical working ansatz for subsequent Standard Model derivation modules.

---

## 5. [INTERPRETATION] Consequence for `zeta_index_for_seed`

The function `zeta_index_for_seed` must not be interpreted as selecting arbitrary poles.  It assigns a spectral index to the already-selected north/south fixed pair.

Therefore the zeta index may depend on the twin-prime seed, but the geometry it labels is the fixed polar pair of one Killing field.

The seed can choose which spectral zero index is read along the axis; it cannot create a new axis per particle in the primitive gauge layer.

---

## 6. [HYPOTHESIS] Twin-prime sectors enter through generation action, not primitive gauge axis

The model now records the following hypothesis:

Twin-prime sectors select generation-dependent action kernels through Collatz, Fibonacci, Kepler and Poincare-disk dynamics. They do not define the primitive weak-isospin axis itself.

This preserves the Standard Model gauge skeleton while allowing generational structure to remain arithmetically indexed.

---

## 7. [VALIDATION GATE] Axis-selection consistency

Future modules must satisfy:

1. The weak doublet uses one universal weak-isospin axis.
2. Berry phase is used as phase transport over this axis.
3. Twin-prime seeds modulate generation/action, not primitive pole existence.
4. The zeta-polar map labels the fixed north/south pair of one Killing field.
5. No module may use unrelated zeta zeros as independently chosen poles.
6. No mass calculation may use observed masses to choose the physical axis.

---

## 8. [DEBT STATUS]

The physical axis-selection debt is **conditionally closed as a canonical working ansatz**:

- mathematically closed: the primitive generator is a Killing-flow generator with two polar fixed points;
- physically selected: the canonical axis is the weak-isospin/Bloch quantization axis;
- Berry role: phase connection over the selected axis;
- twin-prime role: generation/sector index downstream;
- zeta role: imaginary-zero spectral anchor constrained by the same polar pair.

Remaining open part: a deeper derivation of why weak-isospin, rather than another internal axis, is forced from first principles. This remains a formal proof debt, not an operational blocker for the next mass-action modules.

---

## 9. [DO NOT CLAIM]

Do not claim from this module alone:

- numerical fermion masses,
- CKM matrix,
- PMNS matrix,
- final neutrino mass mechanism,
- proof that twin-prime sectors force the weak-isospin axis,
- proof that zeta zeros alone generate the Standard Model gauge group.

This module only fixes the role hierarchy of weak axis, Berry transport, twin-prime sector and zeta anchor.
