# Phase-Intention Hamiltonian - formal English derivation package

This package contains a formal English LaTeX note and reference simulations for the phase-intention Hamiltonian scaffold.

## Contents

- `main.tex` - LaTeX source.
- `main.pdf` - compiled PDF.
- `scripts/collatz_phase_sim.py` - twin-prime seed -> Collatz rhythm -> intention phase simulation.
- `scripts/euler_berry_constraint_scan.py` - Euler-Berry closure defect scan binding epsilon, D, and total phase.
- `scripts/hamiltonian_matrix_demo.py` - finite Hermitian Hamiltonian and unitary evolution check.
- `scripts/run_all.py` - runs all simulations.
- `figures/` - generated figures included in the PDF.
- `results/` - JSON outputs.

## Rebuild

```bash
python scripts/run_all.py
pdflatex main.tex
pdflatex main.tex
```

## Epistemic status

Formal ansatz and numerical consistency scaffold only. No external NOEMA CURRENT/ACK or experimental proof is claimed.
