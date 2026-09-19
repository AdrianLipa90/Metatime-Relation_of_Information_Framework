# Metatime W_sem Semantic U(1) Holonomy Type Firewall v0.1

Status: `APPEND_ONLY_CROSSWALK / CHYBA / LEGACY_PRESERVED`

Date: 2026-09-19

## Why this file exists

Metatime already contains several historically valid uses of `W_ij`, including White-Thread/Berry holonomies and later SU(3)-valued holonomic gluon links. Those records are not rewritten.

The 2026-09-19 semantic clarification introduces a separately typed object:

\[
\boxed{W^{\rm sem}_{ij}[\gamma]=\exp\!\left(i\int_{\gamma_{ij}}A_{\rm sem}\right)\in U(1).}
\]

`A_sem` is a local semantic phase connection/potential. `W_sem` is its nonlocal path transporter / phase holonomy.

## Type table

| Symbol | Type | Meaning |
|---|---|---|
| `W_ij^sem` | `U(1)` | nonlocal semantic phase transporter from `A_sem` |
| `W_ij^WT` | source-typed, typically Abelian in White-Thread use | White-Thread/Berry transport |
| `W_ij^c` | `SU(3)` | colour/gluon holonomic link |
| `W_mu(x)` / local colour link | non-Abelian | local lattice/continuum gauge transport |

Unsuperscripted `W_ij` is therefore ambiguous whenever more than one sector is in scope.

## Compatibility rule

`W_ij^sem` may be bound to a historical Abelian White-Thread transporter only after endpoint, path, normalization, fibre and source provenance are shown to be identical. No such equality is promoted by this crosswalk alone.

`W_ij^sem` must never be silently substituted for the SU(3) gluon `W_ij` used in the v4.x holonomic Yang-Mills lineage.

## Semantic coupling

Given relation overlap `z_ij`,

\[\mathcal C_{ij}=W_{ij}^{\rm sem}z_{ij}.\]

This is a model-level semantic phase coupling. Physical gauge-field and nonlocal-signalling claims remain separate gates.