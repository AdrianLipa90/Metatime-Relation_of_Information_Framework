# METATIME / Standard Model v4.5
## Document-derived Collatz / twin-prime tau operator trace

Status: **PASS as operator-trace reconstruction; NOT a numeric Debt 9 closure**.

### What changed

v4.4 failed because it benchmarked a generic frozen amplitude operator that did not actually use the documented Collatz/twin-prime tau calculations. v4.5 therefore returns to the document calculations and extracts the clean arithmetic layer:

- twin-prime seed pairs;
- center seed `p+1`;
- base clock `L3 = 7` from the ordinary Collatz path `3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1`;
- terminal fragment `4 -> 2 -> 1 -> 1/2`;
- document tau/eigenvalue table;
- information quantum `ln(2)/(24*pi)`;
- Ramanujan-theta residue diagnostic over valuation words.

### Source classification

The module intentionally separates document calculations into two classes.

Allowed as active operator input:

- twin-prime centers and family metadata;
- `tau_i` document eigenvalue trace;
- `L3 = 7` Collatz base clock;
- `ln(2)/(24*pi)` preference/information quantum;
- Ramanujan theta residue as a diagnostic coordinate.

Not allowed as Debt 9 numeric closure:

- charged-lepton quadratic Vandermonde fit, because it uses the three lepton masses as anchors;
- heavy-quark log-OLS power law, because it uses c, b, t masses;
- light-quark required correction factors, because they are computed as benchmark/model ratios;
- neutrino global scale `s`, because it is calibrated to observed mass splitting.

### Important inconsistency exposed

The document table assigns the charged tau lepton `tau_doc = 10.0` and labels it around a seed `10` / `(11,13)`. But the center of `(11,13)` is `12`, not `10`. v4.5 does not hide this. It records the tau row as `document_inconsistency_review`.

This does not kill the direction; it means the symbols must stay separated:

- `pair_seed = (p, p+2)`;
- `center_seed = p+1`;
- `tau_doc/eigenvalue`;
- `mode/eigenvalue`;
- `mass operator trace`.

### Result

v4.5 creates a frozen, benchmark-free document trace. It does **not** claim a mass prediction. It prepares the correct next step: v4.6 may select one predeclared coordinate or formula from this trace and run a sealed benchmark without changing it after seeing residuals.

Debt 9 numeric spectrum remains **OPEN_NOT_CLOSED**.
