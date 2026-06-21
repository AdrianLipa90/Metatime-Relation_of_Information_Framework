#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIGS = ROOT / "figures"
RESULTS = ROOT / "results"

commands = [
    [sys.executable, str(SCRIPTS / "collatz_phase_sim.py"), "--out-dir", str(RESULTS), "--fig-dir", str(FIGS)],
    [sys.executable, str(SCRIPTS / "euler_berry_constraint_scan.py"), "--out-dir", str(RESULTS), "--fig-dir", str(FIGS)],
    [sys.executable, str(SCRIPTS / "hamiltonian_matrix_demo.py"), "--out-dir", str(RESULTS), "--fig-dir", str(FIGS)],
]

for cmd in commands:
    print("RUN", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(ROOT))
