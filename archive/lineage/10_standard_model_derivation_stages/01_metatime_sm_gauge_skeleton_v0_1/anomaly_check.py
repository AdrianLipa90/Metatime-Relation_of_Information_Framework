from fractions import Fraction

Nc = 3
YH = Fraction(1, 2)
YQ = YH / Nc
YL = -Nc * YQ
Yu = -YQ - YH      # left-handed conjugate u^c
Yd = -YQ + YH      # left-handed conjugate d^c
Ye = -YL + YH      # left-handed conjugate e^c

checks = {
    "SU3^2_U1": 2*YQ + Yu + Yd,
    "SU2^2_U1": Nc*YQ + YL,
    "grav^2_U1": 2*Nc*YQ + Nc*Yu + Nc*Yd + 2*YL + Ye,
    "U1^3": 2*Nc*YQ**3 + Nc*Yu**3 + Nc*Yd**3 + 2*YL**3 + Ye**3,
}

charges = {
    "Q_L": YQ,
    "u_c_L": Yu,
    "d_c_L": Yd,
    "L_L": YL,
    "e_c_L": Ye,
}

electric = {
    "u_L": Fraction(1,2)+YQ,
    "d_L": Fraction(-1,2)+YQ,
    "nu_L": Fraction(1,2)+YL,
    "e_L": Fraction(-1,2)+YL,
}

print("hypercharge")
for k,v in charges.items():
    print(k, str(v))
print("anomaly_checks")
for k,v in checks.items():
    print(k, str(v))
print("electric_charges")
for k,v in electric.items():
    print(k, str(v))
