#!/usr/bin/env python3
"""
Metatime Standard Model mass vectorization check v0.1.
This script verifies the one-generation representation vectors and anomaly cancellation,
and keeps observed masses only as validation targets. It does not derive the mass spectrum.
"""
from fractions import Fraction
import math

KAPPA = math.log(2)/(24*math.pi)
FIELDS = [
    ('Q_L', 2, 3, 6, 6, Fraction(1,6)),
    ('u_R^c', 1, 0, 3, 3, Fraction(-2,3)),
    ('d_R^c', 1, 0, 3, 3, Fraction(1,3)),
    ('L_L', 0, 1, 2, 2, Fraction(-1,2)),
    ('e_R^c', 0, 0, 1, 1, Fraction(1)),
]

def anomalies():
    return {
        'SU3^2_U1': sum(su3*Y for _, su3, _, _, _, Y in FIELDS),
        'SU2^2_U1': sum(su2*Y for _, _, su2, _, _, Y in FIELDS),
        'grav^2_U1': sum(grav*Y for _, _, _, grav, _, Y in FIELDS),
        'U1^3': sum(u1*Y**3 for _, _, _, _, u1, Y in FIELDS),
    }

if __name__ == '__main__':
    print('kappa =', KAPPA)
    for k, v in anomalies().items():
        print(k, v)
    assert all(v == 0 for v in anomalies().values())
    print('PASS: exact anomaly cancellation on rational hypercharge assignments.')
