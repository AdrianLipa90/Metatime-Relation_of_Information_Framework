# Phase-first Hamiltonian podkladka

This package contains a LaTeX/PDF formal note plus reference simulation scripts for the proposed phase-first Hamiltonian:

- free part = Information/Intention-generated phase;
- rhythm = Collatz/Kolac orbit;
- seed = twin-prime pair;
- geometry = Aharonov-Bohm + Berry + Euler holonomy;
- Euler-Berry closure = phase defect epsilon tied to topological/defect sector D.

## Files

- `main.tex` - LaTeX source of the note.
- `scripts/collatz_phase_sim.py` - twin-prime Collatz phase and epsilon/D scan.
- `scripts/hamiltonian_matrix_demo.py` - finite-dimensional Hermitian/unitarity check.
- `scripts/run_all.py` - runs all reference simulations.
- `figures/*.png` - generated figures used in the PDF.
- `results/*.json` - simulation outputs.

## Run

```bash
python3 scripts/run_all.py
pdflatex main.tex
pdflatex main.tex
```

## Epistemic status

This is an artifact-grounded formal modeling note and simulation scaffold. It does not claim experimental validation or external NOEMA CURRENT/ACK.
