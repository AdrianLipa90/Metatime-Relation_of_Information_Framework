# METATIME SM v3.4 — Projection Orientation for Sector-Basis / White-Thread Operator

**Status:** pre-mass module.  
**Gate:** `PRE_MASS_ORIENTATION_OPERATOR_PASS`.  
**Scope:** Debt 9 / Debt 10 / Debt 11 bridge.  
**Rule:** no observed masses, no observed CKM/PMNS entries, no old fitted White-Thread constants, no old `tau/eigenvalue` import.

## PURPOSE

v3.2 showed that the frozen representation projection from v3.1 cannot be added to the mass action as a simple scalar. v3.3 recovered the missing sector-basis / White-Thread layer from old-document structure. v3.4 defines the next missing piece: **orientation**.

The purpose is not to improve the mass error. The purpose is to define which sector basis a particle belongs to, and how up/down quark bases can differ before any CKM or mass rescore is attempted.

## DEFINITION — Sector-Basis Orientation Channel

A channel record consists of:

- particle name,
- family class,
- generation index,
- sector label,
- seed pair,
- mode,
- CP1 weak pole,
- chiral/Higgs path,
- tetrahedral/color depth,
- hypercharge path,
- information-operator role.

The information operator is not a scalar tuning knob. It is recorded as the **quantum of informational preference fluctuation**.

## ANSATZ — Old-Document Bridge Without Old Fits

Old Metatime documents suggest that the present v2.x/v3.x common generation ladder is too flat. v3.4 therefore introduces a quarantined bridge assignment:

- charged leptons: small charged-lepton seed sector,
- neutrinos: pair-coherence sector, quarantined for PMNS,
- light quarks: light-quark seed sector,
- heavy quarks: heavy-quark resonance sector.

This is not a mass result. It is a sector-basis ansatz extracted from old-document structure after removing fitted constants.

## LEMMA — A CKM-Like Object Requires Non-Identical Up and Down Bases

If up-type and down-type quarks live in the same ordered basis with only labels changed, a non-trivial mixing matrix has no source. A CKM-like object requires a relative orientation between the up basis and the down basis.

v3.4 constructs structural up/down bases and checks that they are not identical. This is a readiness condition for CKM, not a CKM prediction.

## PROOF / VALIDATION

The validation script constructs normalized feature vectors from structural coordinates only. It then Gram-Schmidt orthonormalizes up and down bases and computes their overlap matrix. The identity-distance is non-zero, which means the bases are structurally non-identical.

No observed masses or observed mixing values are read.

## INTERPRETATION

This module repairs the methodological failure mode exposed by v3.2:

- representation projection is not a scalar mass correction,
- sector-basis orientation must be fixed before mass testing,
- CKM must come from relative basis orientation, not a flat common seed ladder,
- White-Thread may later act as open holonomy between oriented sector bases.

## VALIDATION GATE

`PRE_MASS_ORIENTATION_OPERATOR_PASS` requires:

- all channel orientation vectors are finite and normalized,
- every record has `uses_observed_mass = False`,
- every record has `uses_observed_mixing = False`,
- up/down bases are non-identical,
- charged lepton, neutrino, light-quark and heavy-quark sectors are present,
- heavy-quark resonance remains explicitly quarantined as old-document bridge ansatz.

## DO NOT CLAIM

Do not claim:

- numerical mass prediction,
- CKM derivation,
- PMNS derivation,
- White-Thread coupling derivation,
- final proof of heavy-quark seed assignment.

v3.4 only freezes the next pre-mass orientation layer.

## NEXT STEP

The next allowed step is a CKM-readiness module: derive a symbolic White-Thread/open-holonomy rotation between the up and down bases without inserting observed CKM values.

Only after that should Debt 9 one-anchor mass scaling be retried.
