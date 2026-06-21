# Lineage from v4.5

v4.6 continues v4.5 by selecting and benchmarking document-derived Collatz/twin-prime/tau formula candidates.

Input basis:
- v4.5 document-derived trace: `45_debt9_document_collatz_twinprime_tau_v4_5/results/document_collatz_twinprime_tau_trace_v4_5.json`.
- v4.4 benchmark snapshot used only after formula selection: `44_debt9_mmt_sealed_benchmark_v4_4/data/benchmark_reference_snapshot_v4_4.json`.
- document formulas from README/Formal_SM are classified by provenance before benchmarking.

Boundary:
- v4.6 does not promote old fitted formulas.
- v4.6 records one selected clean diagnostic formula and several comparison formulas.
- Benchmark values are never operator inputs; they are post-selection validation targets.
