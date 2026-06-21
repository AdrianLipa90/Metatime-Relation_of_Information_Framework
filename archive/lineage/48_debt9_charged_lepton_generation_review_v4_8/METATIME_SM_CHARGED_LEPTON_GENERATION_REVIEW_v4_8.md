# v4.8 Charged-Lepton Generation Operator Review

Status: **PASS as diagnostic review; FAIL as numeric Debt 9 closure**.

v4.8 tests whether the already existing charged-lepton holonomy coefficients and frozen tau_v2 action repair the v4.7 mu/tau inversion. It does not add a new ontology and does not claim a mass prediction.

Review fingerprint: `a1bc731d189abc8afe147acc9eb23a91120f6cd55a56477154a27e2e71af306c`

## Ranked candidates, excluding the electron unit anchor

| rank | candidate | mean abs rel error | median abs rel error | max abs rel error |
|---:|---|---:|---:|---:|
| 1 | `doc_F_plus_tau_v2_amplitude_gate` | 0.789429 | 0.789429 | 0.966753 |
| 2 | `doc_F_plus_tau_v2_full_action` | 0.824479 | 0.824479 | 1.11778 |
| 3 | `doc_F_mass_screen_release` | 0.876703 | 0.876703 | 1.52623 |
| 4 | `tau_v2_action_gate` | 4.96015 | 4.96015 | 9.55987 |
| 5 | `v47_baseline` | 8.52584 | 8.52584 | 16.4223 |

## Interpretation

- The document F_ij layer has the right qualitative direction: it screens the muon channel and releases the tau channel.
- The review still cannot close Debt 9: the electron unit anchor remains inherited, F_ij is not rederived here, and the best diagnostic candidate is ranked after benchmark comparison.
- The next valid step is v4.9: freeze one predeclared charged-lepton operator, then run a sealed benchmark without changing it.

## Guard status

- archived mass solvers: not used
- reference replay: not used
- post-residual tuning: denied
- canon/current promotion: denied
