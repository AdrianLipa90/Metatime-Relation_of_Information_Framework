# Validation Status v2.2

- Module: Debt 7 weak-axis first-principles selection
- Gate type: structural-enumeration PASS
- Script: `scripts/weak_axis_selection_gate_v2_2.py`
- Return code: 0

## stdout

```json
{
  "gate_id": "DEBT7_WEAK_AXIS_STRUCTURAL_ENUMERATION_v2_2",
  "gate_type": "structural_enumeration_pass",
  "premises_used": [
    "two_pole",
    "killing_flow",
    "chirality",
    "charge_splitting",
    "mass_gate",
    "non_arithmetic_selector",
    "non_connection_only"
  ],
  "independent_computation": false,
  "uses_observed_masses_as_input": false,
  "status": "PASS",
  "selected_candidates": [
    "weak isospin / Bloch quantization axis"
  ],
  "note": "Finite structural candidate enumeration; not empirical mass prediction."
}
```

## stderr

```text

```

## Epistemic note

This PASS is not an empirical/numerical mass prediction. It is a finite structural enumeration under declared primitive-axis requirements. It is therefore stronger than a purely hard-coded symbolic check but weaker than a computational prediction over physical observables.
