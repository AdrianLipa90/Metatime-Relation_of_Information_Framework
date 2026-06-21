#!/usr/bin/env python3
"""Run all reference simulations for the phase Hamiltonian package."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    run([sys.executable, "scripts/collatz_phase_sim.py", "--p", "11", "--steps", "80"])
    run([sys.executable, "scripts/hamiltonian_matrix_demo.py", "--dim", "8", "--steps", "60"])


if __name__ == "__main__":
    main()
