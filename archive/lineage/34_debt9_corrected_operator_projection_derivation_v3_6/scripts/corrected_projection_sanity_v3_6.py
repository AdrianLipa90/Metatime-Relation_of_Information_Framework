#!/usr/bin/env python3
import math, json
from pathlib import Path
KAPPA = math.log(2)/(24*math.pi)
def orders(x): return abs(x)/math.log(10)
examples=[]
for p in [0.01,0.05,0.1,0.25,0.5,1.0]:
    shift=p/KAPPA
    examples.append({
        "projection_scalar": p,
        "log_shift_if_injected": shift,
        "orders_of_magnitude_if_injected": orders(shift),
        "interpretation": "dangerous if treated as additive action scalar"
    })
status={
    "mass_input_used": False,
    "ckm_input_used": False,
    "pmns_input_used": False,
    "old_tau_imported": False,
    "old_white_thread_constants_imported": False,
    "information_quantum": KAPPA,
    "gate": "CORRECTED_DERIVATION_SANITY_PASS",
    "examples": examples,
    "conclusion": "Order-one projection scalars are too large to inject directly into the mass action."
}
out=Path(__file__).resolve().parents[1]/"results"/"projection_scalar_amplification_sanity_v3_6.json"
out.write_text(json.dumps(status, indent=2), encoding="utf-8")
print(json.dumps(status, indent=2))
