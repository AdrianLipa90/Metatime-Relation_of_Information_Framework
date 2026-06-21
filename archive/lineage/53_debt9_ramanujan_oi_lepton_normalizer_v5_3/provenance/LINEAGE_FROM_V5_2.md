# Lineage from v5.2 to v5.3

v5.2 used the White-Thread root gate but did not explicitly apply the separated Ramanujan/OI path normalizer even though Ramanujan and the information operator exist in the source docs and v2.x modules.

v5.3 adds a root-relative Ramanujan-OI amplitude normalizer:

- `OIB = ln2/(24*pi)` as information preference quantum.
- `A_R` from `ramanujan_scaled_action`.
- `V = exp(-A_R/OIB)` from the Ramanujan seed suppression layer.
- `R_ei = exp(-(A_R_i-A_R_e)/(2*OIB*DeltaGeneration))` as spinor half-action along the root-relative generation path.

No observed masses are used in this normalizer. Benchmark targets are used only after formula fingerprinting.
