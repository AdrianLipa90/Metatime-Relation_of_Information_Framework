# Selected Archive Formula / Mass Source Excerpts

Created UTC: 2026-06-20T09:50:27Z

Provenance: scanned local v3.6 Repair1 repo text sources.


## 00_original_metatime/Metatime-main/NoParamSM/gluons.py


### Line 35 — tau_eigenvalue

```text
33: 
34: # =============================================================================
35: # 2. Generate τ eigenvalues for 8 gluons from twin primes
36: # =============================================================================
37: 
```


### Line 47 — tau_eigenvalue

```text
45:     return twins
46: 
47: def collatz_tau(seed: int, s: float = 0.5) -> float:
48:     # Uproszczenie: τ = seed (w pełnej teorii z orbit Collatza)
49:     return float(seed)
```


### Line 56 — tau_eigenvalue

```text
54: for i, (p1, p2) in enumerate(twin_pairs):
55:     seed = p1 + 1
56:     τ = collatz_tau(seed)
57:     τ_gluons.append(τ)
58:     print(f"  Gluon g{i+1}: ({p1}, {p2}) -> seed = {seed} -> τ = {τ:.1f}")
```


### Line 223 — mass_or_fermion

```text
221: print(f"\nτ range: min = {τ_min:.1f}, max = {τ_max:.1f}")
222: 
223: # Zakładamy, że skala jest proporcjonalna do τ (jak w masach fermionów)
224: mu_min = mu_star * (τ_min / τ_max)
225: mu_max = mu_star
```


## 00_original_metatime/Metatime-main/NoParamSM/gluonsfull.py


### Line 36 — tau_eigenvalue

```text
34:     return twins
35: 
36: def tau_from_twins(twin_pairs: List[Tuple[int, int]]) -> np.ndarray:
37:     """
38:     Dla każdej pary (p, p+2) zwraca τ = p+1.
```


### Line 49 — mass_or_fermion

```text
47: ALPHA_C = 0.474812      # współczynnik kinetyczny pola informacji (1/g^2)
48: I0 = 0.009               # operator intencji
49: BETA_FERMION = 0.414     # wykładnik dla fermionów (z mas)
50: M_E = 0.511              # masa elektronu w MeV
51: TAU_E = 4.0              # τ elektronu (z generatora)
```


### Line 51 — tau_eigenvalue

```text
49: BETA_FERMION = 0.414     # wykładnik dla fermionów (z mas)
50: M_E = 0.511              # masa elektronu w MeV
51: TAU_E = 4.0              # τ elektronu (z generatora)
52: 
53: # Stałe QCD
```


### Line 73 — tau_eigenvalue

```text
71:             twin_pairs = generate_twin_primes(8)
72:         self.twin_pairs = twin_pairs
73:         self.tau = tau_from_twins(twin_pairs)
74:         self._compute_all()
75: 
```


### Line 85 — mass_or_fermion

```text
83: 
84:         # Skala masy M0 z elektronu
85:         self.M0 = M_E / (TAU_E ** BETA_FERMION)   # MeV
86: 
87:         # Masa glueballa
```


### Line 88 — tau_eigenvalue

```text
86: 
87:         # Masa glueballa
88:         self.sum_tau2 = np.sum(self.tau ** 2)
89:         self.m_glueball_MeV = self.M0 * self.alpha_c * self.sum_tau2
90:         self.m_glueball_GeV = self.m_glueball_MeV / 1000.0
```


### Line 89 — tau_eigenvalue

```text
87:         # Masa glueballa
88:         self.sum_tau2 = np.sum(self.tau ** 2)
89:         self.m_glueball_MeV = self.M0 * self.alpha_c * self.sum_tau2
90:         self.m_glueball_GeV = self.m_glueball_MeV / 1000.0
91: 
```


### Line 179 — tau_eigenvalue

```text
177:         print("🌌 METATIME GLUON SOLVER – WYNIKI")
178:         print("=" * 70)
179:         print(f"Liczba gluonów: {len(self.tau)}")
180:         print(f"Pary bliźniacze: {self.twin_pairs}")
181:         print(f"τ gluonów: {self.tau.tolist()}")
```


### Line 181 — tau_eigenvalue

```text
179:         print(f"Liczba gluonów: {len(self.tau)}")
180:         print(f"Pary bliźniacze: {self.twin_pairs}")
181:         print(f"τ gluonów: {self.tau.tolist()}")
182:         print(f"Suma kwadratów τ: {self.sum_tau2:.1f}")
183:         print("-" * 70)
```


### Line 182 — tau_eigenvalue

```text
180:         print(f"Pary bliźniacze: {self.twin_pairs}")
181:         print(f"τ gluonów: {self.tau.tolist()}")
182:         print(f"Suma kwadratów τ: {self.sum_tau2:.1f}")
183:         print("-" * 70)
184:         print(f"α_c (pole informacji) = {self.alpha_c:.6f}")
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMextended.py


### Line 35 — tau_eigenvalue

```text
33:         # PDG Baselines for reference comparison
34:         self.pdg = {
35:             'e': 0.510998, 'mu': 105.658, 'tau': 1776.86,
36:             'p': 938.272, 'n': 939.565,
37:             'W': 80377, 'Z': 91187, 'Higgs': 125100 # In MeV
```


### Line 67 — mass_or_fermion

```text
65:         return m_w, m_z, m_h
66: 
67:     def calculate_fermions(self, O_I):
68:         """FERMIONIC SECTOR: Yukawa-like topological charge mapping."""
69:         d_oi = O_I - self.spec.O_I_REF
```


### Line 68 — mass_or_fermion

```text
66: 
67:     def calculate_fermions(self, O_I):
68:         """FERMIONIC SECTOR: Yukawa-like topological charge mapping."""
69:         d_oi = O_I - self.spec.O_I_REF
70:         # Mass modulation via information density gradients
```


### Line 70 — mass_or_fermion

```text
68:         """FERMIONIC SECTOR: Yukawa-like topological charge mapping."""
69:         d_oi = O_I - self.spec.O_I_REF
70:         # Mass modulation via information density gradients
71:         e = self.pdg['e'] * math.exp(0.2 * d_oi)
72:         mu = self.pdg['mu'] * math.exp(0.1 * d_oi)
```


### Line 73 — tau_eigenvalue

```text
71:         e = self.pdg['e'] * math.exp(0.2 * d_oi)
72:         mu = self.pdg['mu'] * math.exp(0.1 * d_oi)
73:         tau = self.pdg['tau'] * math.exp(0.05 * d_oi)
74:         return e, mu, tau
75: 
```


### Line 74 — tau_eigenvalue

```text
72:         mu = self.pdg['mu'] * math.exp(0.1 * d_oi)
73:         tau = self.pdg['tau'] * math.exp(0.05 * d_oi)
74:         return e, mu, tau
75: 
76:     def calculate_nucleons(self, O_I, e_mass):
```


### Line 76 — mass_or_fermion

```text
74:         return e, mu, tau
75: 
76:     def calculate_nucleons(self, O_I, e_mass):
77:         """NUCLEONIC SECTOR: Baryonic mass as a spectral saturation state."""
78:         # Saturation factor based on the hyperbolic tangent of the info density
```


### Line 77 — mass_or_fermion

```text
75: 
76:     def calculate_nucleons(self, O_I, e_mass):
77:         """NUCLEONIC SECTOR: Baryonic mass as a spectral saturation state."""
78:         # Saturation factor based on the hyperbolic tangent of the info density
79:         factor = math.tanh(O_I * self.spec.IM_S1) / math.tanh(self.spec.O_I_REF * self.spec.IM_S1)
```


### Line 81 — mass_or_fermion

```text
79:         factor = math.tanh(O_I * self.spec.IM_S1) / math.tanh(self.spec.O_I_REF * self.spec.IM_S1)
80:         
81:         # Proton and Neutron masses reconstructed from internal binding topology
82:         m_p = 938.272 * factor
83:         m_n = 939.565 * factor
```


### Line 87 — mass_or_fermion

```text
85: 
86:     def calculate_nuclear_stability(self, O_I, A, Z):
87:         """NUCLEAR SECTOR: Semi-Empirical Mass Formula (Metatime variant)."""
88:         scale = (O_I / self.spec.O_I_REF) ** (1.0 / (1.0 + (self.spec.IM_S1/10.0)))
89:         
```


### Line 104 — tau_eigenvalue

```text
102:         samples = self.get_oi_samples()
103:         data = {
104:             'Leptons (MeV)': {'e': [], 'mu': [], 'tau': []},
105:             'Bosons (GeV)': {'W': [], 'Z': [], 'Higgs': []},
106:             'Nucleons (MeV)': {'Proton': [], 'Neutron': []},
```


### Line 118 — mass_or_fermion

```text
116:             
117:             # Lepton Sector
118:             e, mu, tau = self.calculate_fermions(O)
119:             data['Leptons (MeV)']['e'].append(e)
120:             data['Leptons (MeV)']['mu'].append(mu)
```


### Line 121 — tau_eigenvalue

```text
119:             data['Leptons (MeV)']['e'].append(e)
120:             data['Leptons (MeV)']['mu'].append(mu)
121:             data['Leptons (MeV)']['tau'].append(tau)
122:             
123:             # Baryon Sector
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMextendedresult.txt


### Line 10 — tau_eigenvalue

```text
8:    e        | Mean:       0.5110 | Std: 0.000066
9:    mu       | Mean:     105.6580 | Std: 0.006843
10:    tau      | Mean:    1776.8603 | Std: 0.057542
11: 
12: >> Bosons (GeV)
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMresult.json


### Line 18 — tau_eigenvalue

```text
16:         "std": 0.006871773533966165
17:       },
18:       "tau": {
19:         "mean": 1776.8580476654806,
20:         "std": 0.05778145208749473
```


### Line 23 — mass_or_fermion

```text
21:       }
22:     },
23:     "quarks": {
24:       "u": {
25:         "mean": 2.159990520473858,
```


### Line 75 — tau_eigenvalue

```text
73:     "lepton_e": true,
74:     "lepton_mu": true,
75:     "lepton_tau": true,
76:     "16O_binding": true
77:   }
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMresult.txt


### Line 7 — tau_eigenvalue

```text
5:   e: 0.510997 ± 0.000066 (PDG: 0.5109989461)
6:   mu: 105.658142 ± 0.006872 (PDG: 105.6583745)
7:   tau: 1776.858048 ± 0.057781 (PDG: 1776.86)
8: 
9: Quarks (mean ± std) [MeV] (u,d,s shown):
```


### Line 9 — mass_or_fermion

```text
7:   tau: 1776.858048 ± 0.057781 (PDG: 1776.86)
8: 
9: Quarks (mean ± std) [MeV] (u,d,s shown):
10:   u: 2.159991 ± 0.000281 (PDG: 2.16)
11:   d: 4.673514 ± 0.082454 (PDG: 4.67)
```


### Line 23 — tau_eigenvalue

```text
21:   208Pb: 7.844389 ± 0.231776 (ref: 7.867)
22: 
23: Quick checks: {'lepton_e': True, 'lepton_mu': True, 'lepton_tau': True, '16O_binding': True}
24: 
25: Saved results to newsm_results/newsm_results.json
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMsolver.py


### Line 11 — mass_or_fermion

```text
9: 
10: Outputs:
11:  - ensemble means and standard deviations for particle masses, nucleon masses,
12:    and nuclear binding energies (selected nuclei).
13:  - unit-test checks (consistency with PDG within modeled uncertainty)
```


### Line 46 — tau_eigenvalue

```text
44: # ----------------------------
45: PDG = {
46:     'leptons': {'e': 0.5109989461, 'mu': 105.6583745, 'tau': 1776.86},
47:     'quarks': {'u': 2.16, 'd': 4.67, 's': 93.5, 'c': 1270.0, 'b': 4180.0, 't': 173000.0},
48:     'nucleons': {'p': 938.27208816, 'n': 939.56542052},
```


### Line 47 — mass_or_fermion

```text
45: PDG = {
46:     'leptons': {'e': 0.5109989461, 'mu': 105.6583745, 'tau': 1776.86},
47:     'quarks': {'u': 2.16, 'd': 4.67, 's': 93.5, 'c': 1270.0, 'b': 4180.0, 't': 173000.0},
48:     'nucleons': {'p': 938.27208816, 'n': 939.56542052},
49:     'binding_ref_per_nucleon': {'16O': 7.976, '56Fe': 8.79, '208Pb': 7.867}
```


### Line 111 — mass_or_fermion

```text
109:         }
110: 
111:     def yukawa_factor(self, C: float, O_I: float) -> float:
112:         """ekspresja sprzężenia: exp(C * (O_I - O_I_ref)) — prosta, deterministyczna"""
113:         return math.exp(C * (O_I - self.O_I_ref))
```


### Line 147 — mass_or_fermion

```text
145:         factor = math.tanh(O_I * im) / math.tanh(self.O_I_ref * im)
146:         # przy O_I = O_I_ref => factor = 1
147:         # E_bind_ref zostanie określone później z mas referencyjnych (mass_ref)
148:         return float(factor)
149: 
```


### Line 152 — mass_or_fermion

```text
150: 
151: # ----------------------------
152: # Mass spectrum + nucleon construction
153: # ----------------------------
154: class MassEngine:
```


### Line 154 — mass_or_fermion

```text
152: # Mass spectrum + nucleon construction
153: # ----------------------------
154: class MassEngine:
155:     """
156:     Oblicza masy fermionów i nukleonów deterministycznie dla danej wartości O_I.
```


### Line 156 — mass_or_fermion

```text
154: class MassEngine:
155:     """
156:     Oblicza masy fermionów i nukleonów deterministycznie dla danej wartości O_I.
157:     Masy referencyjne pochodzą z PDG; modulujemy je przez topologiczne czynniki exp(C*ΔO_I).
158:     """
```


### Line 163 — tau_eigenvalue

```text
161:         # topologiczne C dla cząstek (przykład, zgodne z Twoim formalizmem)
162:         self.C = {
163:             'e': 0.2, 'mu': 0.1, 'tau': 0.05,
164:             'u': 0.2, 'd': -27.13, 's': -5.0,
165:             'c': 0.0, 'b': 0.0, 't': 0.0
```


### Line 167 — mass_or_fermion

```text
165:             'c': 0.0, 'b': 0.0, 't': 0.0
166:         }
167:         self.mass_ref = {**PDG['leptons'], **PDG['quarks']}  # referencje
168: 
169:     def fermion_mass(self, particle: str, O_I: float) -> float:
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/Fij_toy_S2_delta_theta.csv


### Line 1 — tau_eigenvalue

```text
1: ,e,mu,tau,u,d,s,c,b,t,nu1,nu2,nu3
2: e,1.0,1.002358972497844,1.0047235097469331,0.9988225964390275,0.9981168198209383,1.000942922067836,1.0094693310381957,1.0142375692625847,1.0190283303067023,0.9976465791572003,1.0,1.002358972497844
3: mu,0.9976465791572003,1.0,1.002358972497844,0.9964719465223085,0.9957678308936226,0.9985872821325888,1.0070936248743632,1.0118506414275314,1.0166301277947551,0.9952986969040639,0.9976465791572003,1.0
```


### Line 4 — tau_eigenvalue

```text
2: e,1.0,1.002358972497844,1.0047235097469331,0.9988225964390275,0.9981168198209383,1.000942922067836,1.0094693310381957,1.0142375692625847,1.0190283303067023,0.9976465791572003,1.0,1.002358972497844
3: mu,0.9976465791572003,1.0,1.002358972497844,0.9964719465223085,0.9957678308936226,0.9985872821325888,1.0070936248743632,1.0118506414275314,1.0166301277947551,0.9952986969040639,0.9976465791572003,1.0
4: tau,0.9952986969040639,0.9976465791572003,1.0,0.9941268286740976,0.9934243701258081,0.9962371860094632,1.0047235097469331,1.0094693310381957,1.0142375692625847,0.9929563402059584,0.9952986969040639,0.9976465791572003
5: u,1.001178791474252,1.0035405447087642,1.0059078692542034,1.0,0.9992933914184507,1.0021228250505825,1.0106592848791425,1.0154331438620976,1.020229552214489,0.9988225964390275,1.001178791474252,1.0035405447087642
6: d,1.0018867332376982,1.0042501564873605,1.0066191549874695,1.000707108230293,1.0,1.0028314343479403,1.0113739303775025,1.0161511649954347,1.020950964927648,0.9995288721175721,1.0018867332376982,1.0042501564873605
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/Fij_toy_S2_directional.csv


### Line 1 — tau_eigenvalue

```text
1: ,e,mu,tau,u,d,s,c,b,t,nu1,nu2,nu3
2: e,1.0,1.00235897,1.00472351,0.9988226,0.99811682,1.00094292,1.00946933,1.01423757,1.01902833,0.99764658,1.0,1.00235897
3: mu,0.99764658,1.0,1.00235897,0.99647195,0.99576783,0.99858728,1.00709362,1.01185064,1.01663013,0.9952987,0.99764658,1.0
```


### Line 4 — tau_eigenvalue

```text
2: e,1.0,1.00235897,1.00472351,0.9988226,0.99811682,1.00094292,1.00946933,1.01423757,1.01902833,0.99764658,1.0,1.00235897
3: mu,0.99764658,1.0,1.00235897,0.99647195,0.99576783,0.99858728,1.00709362,1.01185064,1.01663013,0.9952987,0.99764658,1.0
4: tau,0.9952987,0.99764658,1.0,0.99412683,0.99342437,0.99623719,1.00472351,1.00946933,1.01423757,0.99295634,0.9952987,0.99764658
5: u,1.00117879,1.00354054,1.00590787,1.0,0.99929339,1.00212283,1.01065928,1.01543314,1.02022955,0.9988226,1.00117879,1.00354054
6: d,1.00188673,1.00425016,1.00661915,1.00070711,1.0,1.00283143,1.01137393,1.01615116,1.02095096,0.99952887,1.00188673,1.00425016
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/Fij_toy_S2_sym_abs.csv


### Line 1 — tau_eigenvalue

```text
1: ,e,mu,tau,u,d,s,c,b,t,nu1,nu2,nu3
2: e,1.0,1.00235897,1.00472351,1.00117879,1.00188673,1.00094292,1.00946933,1.01423757,1.01902833,1.00235897,1.0,1.00235897
3: mu,1.00235897,1.0,1.00235897,1.00354054,1.00425016,1.00141472,1.00709362,1.01185064,1.01663013,1.00472351,1.00235897,1.0
```


### Line 4 — tau_eigenvalue

```text
2: e,1.0,1.00235897,1.00472351,1.00117879,1.00188673,1.00094292,1.00946933,1.01423757,1.01902833,1.00235897,1.0,1.00235897
3: mu,1.00235897,1.0,1.00235897,1.00354054,1.00425016,1.00141472,1.00709362,1.01185064,1.01663013,1.00472351,1.00235897,1.0
4: tau,1.00472351,1.00235897,1.0,1.00590787,1.00661915,1.00377703,1.00472351,1.00946933,1.01423757,1.00709362,1.00472351,1.00235897
5: u,1.00117879,1.00354054,1.00590787,1.0,1.00070711,1.00212283,1.01065928,1.01543314,1.02022955,1.00117879,1.00117879,1.00354054
6: d,1.00188673,1.00425016,1.00661915,1.00070711,1.0,1.00283143,1.01137393,1.01615116,1.02095096,1.00047135,1.00188673,1.00425016
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/Fij_toy_S2_sym_cos.csv


### Line 1 — tau_eigenvalue

```text
1: ,e,mu,tau,u,d,s,c,b,t,nu1,nu2,nu3
2: e,1.00904062,1.00873123,1.00782468,1.00896293,1.00884219,1.00899087,1.00451014,1.0,0.99551011,1.00873123,1.00904062,1.00873123
3: mu,1.00873123,1.00904062,1.00873123,1.00834958,1.0080513,1.00892882,1.00638425,1.00233209,0.99767334,1.00782468,1.00873123,1.00904062
```


### Line 4 — tau_eigenvalue

```text
2: e,1.00904062,1.00873123,1.00782468,1.00896293,1.00884219,1.00899087,1.00451014,1.0,0.99551011,1.00873123,1.00904062,1.00873123
3: mu,1.00873123,1.00904062,1.00873123,1.00834958,1.0080513,1.00892882,1.00638425,1.00233209,0.99767334,1.00782468,1.00873123,1.00904062
4: tau,1.00782468,1.00873123,1.00904062,1.00716573,1.00671072,1.0082558,1.00782468,1.00451014,1.0,1.00638425,1.00782468,1.00873123
5: u,1.00896293,1.00834958,1.00716573,1.00904062,1.00901263,1.00878973,1.00345009,0.99882595,0.99453613,1.00896293,1.00896293,1.00834958
6: d,1.00884219,1.0080513,1.00671072,1.00901263,1.00904062,1.00859625,1.00278502,0.99813054,0.99399592,1.00902818,1.00884219,1.0080513
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/analysis_F_directional_full.csv


### Line 1 — tau_eigenvalue

```text
1: ,e,mu,tau,u,d,s,c,b,t,nu1,nu2,nu3
2: e,1.000000000000,1.002358972498,1.004723509747,0.998822596439,0.998116819821,1.000942922068,1.009469331038,1.014237569263,1.019028330307,0.997646579157,1.000000000000,1.002358972498
3: mu,0.997646579157,1.000000000000,1.002358972498,0.996471946522,0.995767830894,0.998587282133,1.007093624874,1.011850641428,1.016630127795,0.995298696904,0.997646579157,1.000000000000
```


### Line 4 — tau_eigenvalue

```text
2: e,1.000000000000,1.002358972498,1.004723509747,0.998822596439,0.998116819821,1.000942922068,1.009469331038,1.014237569263,1.019028330307,0.997646579157,1.000000000000,1.002358972498
3: mu,0.997646579157,1.000000000000,1.002358972498,0.996471946522,0.995767830894,0.998587282133,1.007093624874,1.011850641428,1.016630127795,0.995298696904,0.997646579157,1.000000000000
4: tau,0.995298696904,0.997646579157,1.000000000000,0.994126828674,0.993424370126,0.996237186009,1.004723509747,1.009469331038,1.014237569263,0.992956340206,0.995298696904,0.997646579157
5: u,1.001178791474,1.003540544709,1.005907869254,1.000000000000,0.999293391418,1.002122825051,1.010659284879,1.015433143862,1.020229552214,0.998822596439,1.001178791474,1.003540544709
6: d,1.001886733238,1.004250156487,1.006619154987,1.000707108230,1.000000000000,1.002831434348,1.011373930378,1.016151164995,1.020950964928,0.999528872118,1.001886733238,1.004250156487
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/analysis_F_sym_abs_full.csv


### Line 1 — tau_eigenvalue

```text
1: ,e,mu,tau,u,d,s,c,b,t,nu1,nu2,nu3
2: e,1.000000000000,1.002358972498,1.004723509747,1.001178791474,1.001886733238,1.000942922068,1.009469331038,1.014237569263,1.019028330307,1.002358972498,1.000000000000,1.002358972498
3: mu,1.002358972498,1.000000000000,1.002358972498,1.003540544709,1.004250156487,1.001414716463,1.007093624874,1.011850641428,1.016630127795,1.004723509747,1.002358972498,1.000000000000
```


### Line 4 — tau_eigenvalue

```text
2: e,1.000000000000,1.002358972498,1.004723509747,1.001178791474,1.001886733238,1.000942922068,1.009469331038,1.014237569263,1.019028330307,1.002358972498,1.000000000000,1.002358972498
3: mu,1.002358972498,1.000000000000,1.002358972498,1.003540544709,1.004250156487,1.001414716463,1.007093624874,1.011850641428,1.016630127795,1.004723509747,1.002358972498,1.000000000000
4: tau,1.004723509747,1.002358972498,1.000000000000,1.005907869254,1.006619154987,1.003777026238,1.004723509747,1.009469331038,1.014237569263,1.007093624874,1.004723509747,1.002358972498
5: u,1.001178791474,1.003540544709,1.005907869254,1.000000000000,1.000707108230,1.002122825051,1.010659284879,1.015433143862,1.020229552214,1.001178791474,1.001178791474,1.003540544709
6: d,1.001886733238,1.004250156487,1.006619154987,1.000707108230,1.000000000000,1.002831434348,1.011373930378,1.016151164995,1.020950964928,1.000471349949,1.001886733238,1.004250156487
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/analysis_F_sym_cos_full.csv


### Line 1 — tau_eigenvalue

```text
1: ,e,mu,tau,u,d,s,c,b,t,nu1,nu2,nu3
2: e,1.009040621774,1.008731229188,1.007824682705,1.008962932423,1.008842191660,1.008990874329,1.004510140205,1.000000000000,0.995510109830,1.008731229188,1.009040621774,1.008731229188
3: mu,1.008731229188,1.009040621774,1.008731229188,1.008349580717,1.008051297486,1.008928821288,1.006384254056,1.002332086499,0.997673339474,1.007824682705,1.008731229188,1.009040621774
```


### Line 4 — tau_eigenvalue

```text
2: e,1.009040621774,1.008731229188,1.007824682705,1.008962932423,1.008842191660,1.008990874329,1.004510140205,1.000000000000,0.995510109830,1.008731229188,1.009040621774,1.008731229188
3: mu,1.008731229188,1.009040621774,1.008731229188,1.008349580717,1.008051297486,1.008928821288,1.006384254056,1.002332086499,0.997673339474,1.007824682705,1.008731229188,1.009040621774
4: tau,1.007824682705,1.008731229188,1.009040621774,1.007165731927,1.006710720079,1.008255801838,1.007824682705,1.004510140205,1.000000000000,1.006384254056,1.007824682705,1.008731229188
5: u,1.008962932423,1.008349580717,1.007165731927,1.009040621774,1.009012627343,1.008789734115,1.003450088794,0.998825954002,0.994536128680,1.008962932423,1.008962932423,1.008349580717
6: d,1.008842191660,1.008051297486,1.006710720079,1.009012627343,1.009040621774,1.008596245984,1.002785023943,0.998130544396,0.993995921495,1.009028176155,1.008842191660,1.008051297486
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/analysis_sample_pairs.csv


### Line 4 — tau_eigenvalue

```text
2: e,mu,1.002358972498,1.002358972498,1.008731229188
3: mu,e,0.997646579157,1.002358972498,1.008731229188
4: e,tau,1.004723509747,1.004723509747,1.007824682705
5: tau,e,0.995298696904,1.004723509747,1.007824682705
6: nu1,nu3,1.004723509747,1.004723509747,1.007824682705
```


### Line 5 — tau_eigenvalue

```text
3: mu,e,0.997646579157,1.002358972498,1.008731229188
4: e,tau,1.004723509747,1.004723509747,1.007824682705
5: tau,e,0.995298696904,1.004723509747,1.007824682705
6: nu1,nu3,1.004723509747,1.004723509747,1.007824682705
7: nu3,nu1,0.995298696904,1.004723509747,1.007824682705
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/interpretation.md


### Line 1 — white_thread

```text
1: # Toy-Model White-Thread Matrix F_ij on S²
2: 
3: **Toy-Model Construction**: 12 SM fermions assigned to cycles on Kähler sphere S² via polar angles θ_i.  
```


### Line 3 — mass_or_fermion

```text
1: # Toy-Model White-Thread Matrix F_ij on S²
2: 
3: **Toy-Model Construction**: 12 SM fermions assigned to cycles on Kähler sphere S² via polar angles θ_i.  
4: **Intention Operator**: I₀ = 0.009 (subtle topological corrections). [Geometria.txt]  
5: **Generated**: 3 matrices (directional + 2 symmetric), block stats, top deviations, full analysis. [code_file:77..87]
```


### Line 9 — mass_or_fermion

```text
7: ## Model Specification
8: 
9: | Fermion | Generation | Cycle θ_i (rad) |
10: |---------|------------|-----------------|
11: | e       | 1          | π/6 ≈ 0.5236   |
```


### Line 83 — mass_or_fermion

```text
81: 
82: **Toy-Model Strength**: Captures generational hierarchy via θ_i geometry.  
83: **Limitation**: Effects too small (~2%) vs real F_i (e.g. d-quark F_d=0.783). Scale I₀ or add β factor for calibration. [Formal_SM.pdf]
84: 
85: ## Files Generated
```


### Line 100 — mass_or_fermion

```text
98: - Calibrate β to match PDG F_i (u/d/s/neutrinos).  
99: - Add monopole Berry A on S² for true holonomy.  
100: - Extend to full SM (baryons/mesons via quark F_ij).
```


## 00_original_metatime/Metatime-main/simulations/Standard Model/README.md


### Line 1 — mass_or_fermion

```text
1: # Simulation 1 - Toy Model F_ij Generator for 12 Fermions (S²)
2: 
3: This repository contains a Python implementation to compute and analyze **pairwise topological factors F_ij** for the 12 Standard Model fermions in a simple toy model based on a Kähler sphere (S²). It includes directional and symmetric variants of the F matrix and provides basic statistical and visualization outputs.
```


### Line 3 — mass_or_fermion

```text
1: # Simulation 1 - Toy Model F_ij Generator for 12 Fermions (S²)
2: 
3: This repository contains a Python implementation to compute and analyze **pairwise topological factors F_ij** for the 12 Standard Model fermions in a simple toy model based on a Kähler sphere (S²). It includes directional and symmetric variants of the F matrix and provides basic statistical and visualization outputs.
4: 
5: ---
```


### Line 9 — mass_or_fermion

```text
7: ## Overview
8: 
9: We assign each fermion a “cycle angle” θ_i on S²:
10: 
11: | Fermion | Generation | θ_i (rad) |
```


### Line 11 — mass_or_fermion

```text
9: We assign each fermion a “cycle angle” θ_i on S²:
10: 
11: | Fermion | Generation | θ_i (rad) |
12: |---------|------------|-----------|
13: | e       | 1          | π/6       |
```


## 00_original_metatime/Metatime-main/simulations/Standard Model/full solver.py


### Line 9 — mass_or_fermion

```text
7: ║                                                                            ║
8: ║          METATIME: A GEOMETRIC EFFECTIVE FIELD THEORY                      ║
9: ║         OF FERMION MASSES, DARK ENERGY, AND INFORMATION                    ║
10: ║                                                                            ║
11: ║              Complete Monolithic Solver Implementation                      ║
```


### Line 25 — mass_or_fermion

```text
23:   - Kähler geometry (S² manifold) with Berry phase quantization
24:   - Linking number topology (corrected v2.0)
25:   - Fermion mass spectrum fitting (leptons, quarks, neutrinos)
26:   - Information Operator (O_I) as fundamental quantum information
27:   - Cosmological constraints via Euler-Berry linking
```


### Line 74 — mass_or_fermion

```text
72:     
73:     # Neutrino physics
74:     ALPHA_NU = 2.97     # Power-law exponent for neutrino masses
75:     
76:     # Cosmological
```


### Line 88 — mass_or_fermion

```text
86:     
87:     LEPTONS = {
88:         'e': {'mass': 0.5109989461, 'tau': 4.0},
89:         'mu': {'mass': 105.6583745, 'tau': 1.0},
90:         'tau': {'mass': 1776.86, 'tau': 10.0},
```


### Line 89 — mass_or_fermion

```text
87:     LEPTONS = {
88:         'e': {'mass': 0.5109989461, 'tau': 4.0},
89:         'mu': {'mass': 105.6583745, 'tau': 1.0},
90:         'tau': {'mass': 1776.86, 'tau': 10.0},
91:     }
```


### Line 90 — mass_or_fermion

```text
88:         'e': {'mass': 0.5109989461, 'tau': 4.0},
89:         'mu': {'mass': 105.6583745, 'tau': 1.0},
90:         'tau': {'mass': 1776.86, 'tau': 10.0},
91:     }
92:     
```


### Line 93 — mass_or_fermion

```text
91:     }
92:     
93:     QUARKS = {
94:         'u': {'mass': 2.16, 'tau': 0.05},
95:         'd': {'mass': 4.67, 'tau': 0.10},
```


### Line 94 — mass_or_fermion

```text
92:     
93:     QUARKS = {
94:         'u': {'mass': 2.16, 'tau': 0.05},
95:         'd': {'mass': 4.67, 'tau': 0.10},
96:         's': {'mass': 93.5, 'tau': 0.40},
```


### Line 113 — tau_eigenvalue

```text
111: 
112: class CollatzDynamics:
113:     """Collatz iteration for eigenvalue extraction from twin primes"""
114:     
115:     def __init__(self):
```


### Line 123 — tau_eigenvalue

```text
121:         ]
122:     
123:     def iterate(self, tau: float, max_iter: int = 10000) -> List[float]:
124:         """Iterate Collatz-like map"""
125:         orbit = [tau]
```


### Line 125 — tau_eigenvalue

```text
123:     def iterate(self, tau: float, max_iter: int = 10000) -> List[float]:
124:         """Iterate Collatz-like map"""
125:         orbit = [tau]
126:         current = float(tau)
127:         
```


### Line 126 — tau_eigenvalue

```text
124:         """Iterate Collatz-like map"""
125:         orbit = [tau]
126:         current = float(tau)
127:         
128:         for _ in range(max_iter):
```


### Line 144 — tau_eigenvalue

```text
142:         return orbit
143:     
144:     def extract_eigenvalues(self, family: str, p_bar: float) -> List[Dict]:
145:         """Extract eigenvalues using ζ-weighting"""
146:         
```


### Line 145 — tau_eigenvalue

```text
143:     
144:     def extract_eigenvalues(self, family: str, p_bar: float) -> List[Dict]:
145:         """Extract eigenvalues using ζ-weighting"""
146:         
147:         seeds = [p_bar, p_bar/2, p_bar/4, p_bar*2, p_bar/3]
```


### Line 148 — tau_eigenvalue

```text
146:         
147:         seeds = [p_bar, p_bar/2, p_bar/4, p_bar*2, p_bar/3]
148:         eigenvalues = []
149:         
150:         for seed in seeds:
```


### Line 156 — tau_eigenvalue

```text
154:             orbit = self.iterate(seed)
155:             
156:             for n, tau in enumerate(orbit):
157:                 if tau > 0:
158:                     criterion = tau / (seed ** 0.5)
```


### Line 183 — white_thread

```text
181:     - Related to Shannon entropy: S = -Σ p_i log(p_i)
182:     - Quantifies information capacity of topological sectors
183:     - Controls strength of white-thread network couplings
184:     - Dimensionless parameter ∈ [10⁻⁴, 10⁻²]
185:     
```


### Line 214 — white_thread

```text
212:         """
213:         
214:         # Topological quantum numbers (from white-thread network)
215:         C_values = {
216:             'e': 0.2,
```


### Line 257 — white_thread

```text
255:             f"  Physical scale: Fundamental quantum information\n"
256:             f"  Related to: Shannon entropy, topological coupling\n"
257:             f"  Role: Controls strength of white-thread corrections\n"
258:             f"  Value derived from: ln(2)/ln(10000) ≈ 0.00917"
259:         )
```


### Line 887 — white_thread

```text
885: 
886: Related to Shannon entropy and topological correction strengths.
887: Controls white-thread network couplings.
888: 
889: Physical interpretation: O_I ≈ ln(2)/ln(10000) ≈ 0.00917
```


## 00_original_metatime/Metatime-main/simulations/Standard Model/oneparamSM.py


### Line 11 — mass_or_fermion

```text
9: 
10: Outputs:
11:  - ensemble means and standard deviations for particle masses, nucleon masses,
12:    and nuclear binding energies (selected nuclei).
13:  - unit-test checks (consistency with PDG within modeled uncertainty)
```


### Line 46 — tau_eigenvalue

```text
44: # ----------------------------
45: PDG = {
46:     'leptons': {'e': 0.5109989461, 'mu': 105.6583745, 'tau': 1776.86},
47:     'quarks': {'u': 2.16, 'd': 4.67, 's': 93.5, 'c': 1270.0, 'b': 4180.0, 't': 173000.0},
48:     'nucleons': {'p': 938.27208816, 'n': 939.56542052},
```


### Line 47 — mass_or_fermion

```text
45: PDG = {
46:     'leptons': {'e': 0.5109989461, 'mu': 105.6583745, 'tau': 1776.86},
47:     'quarks': {'u': 2.16, 'd': 4.67, 's': 93.5, 'c': 1270.0, 'b': 4180.0, 't': 173000.0},
48:     'nucleons': {'p': 938.27208816, 'n': 939.56542052},
49:     'binding_ref_per_nucleon': {'16O': 7.976, '56Fe': 8.79, '208Pb': 7.867}
```


### Line 111 — mass_or_fermion

```text
109:         }
110: 
111:     def yukawa_factor(self, C: float, O_I: float) -> float:
112:         """ekspresja sprzężenia: exp(C * (O_I - O_I_ref)) — prosta, deterministyczna"""
113:         return math.exp(C * (O_I - self.O_I_ref))
```


### Line 147 — mass_or_fermion

```text
145:         factor = math.tanh(O_I * im) / math.tanh(self.O_I_ref * im)
146:         # przy O_I = O_I_ref => factor = 1
147:         # E_bind_ref zostanie określone później z mas referencyjnych (mass_ref)
148:         return float(factor)
149: 
```


### Line 152 — mass_or_fermion

```text
150: 
151: # ----------------------------
152: # Mass spectrum + nucleon construction
153: # ----------------------------
154: class MassEngine:
```


### Line 154 — mass_or_fermion

```text
152: # Mass spectrum + nucleon construction
153: # ----------------------------
154: class MassEngine:
155:     """
156:     Oblicza masy fermionów i nukleonów deterministycznie dla danej wartości O_I.
```


### Line 156 — mass_or_fermion

```text
154: class MassEngine:
155:     """
156:     Oblicza masy fermionów i nukleonów deterministycznie dla danej wartości O_I.
157:     Masy referencyjne pochodzą z PDG; modulujemy je przez topologiczne czynniki exp(C*ΔO_I).
158:     """
```


### Line 163 — tau_eigenvalue

```text
161:         # topologiczne C dla cząstek (przykład, zgodne z Twoim formalizmem)
162:         self.C = {
163:             'e': 0.2, 'mu': 0.1, 'tau': 0.05,
164:             'u': 0.2, 'd': -27.13, 's': -5.0,
165:             'c': 0.0, 'b': 0.0, 't': 0.0
```


### Line 167 — mass_or_fermion

```text
165:             'c': 0.0, 'b': 0.0, 't': 0.0
166:         }
167:         self.mass_ref = {**PDG['leptons'], **PDG['quarks']}  # referencje
168: 
169:     def fermion_mass(self, particle: str, O_I: float) -> float:
```


## 00_original_metatime/Metatime-main/simulations/Standard Model/plots.py


### Line 19 — mass_or_fermion

```text
17: ║    1. S² Manifold with Berry Phases                                        ║
18: ║    2. Collatz Orbits (Twin Prime Families)                                 ║
19: ║    3. Fermion Mass Spectrum (Observation vs Prediction)                    ║
20: ║    4. Neutrino Mass-Squared Splittings with Corrections                    ║
21: ║    5. DUNE CP Resonance Prediction                                         ║
```


### Line 20 — mass_or_fermion

```text
18: ║    2. Collatz Orbits (Twin Prime Families)                                 ║
19: ║    3. Fermion Mass Spectrum (Observation vs Prediction)                    ║
20: ║    4. Neutrino Mass-Squared Splittings with Corrections                    ║
21: ║    5. DUNE CP Resonance Prediction                                         ║
22: ║    6. CMB Power Spectrum Enhancement                                       ║
```


### Line 103 — mass_or_fermion

```text
101:     
102:     # Berry phase as function of path
103:     gamma_fermionic = np.pi * np.ones_like(theta)
104:     
105:     ax2.fill_between(theta, gamma_fermionic, alpha=0.3, color='red', label='Fermionic ($\\gamma = \\pi$)')
```


### Line 105 — mass_or_fermion

```text
103:     gamma_fermionic = np.pi * np.ones_like(theta)
104:     
105:     ax2.fill_between(theta, gamma_fermionic, alpha=0.3, color='red', label='Fermionic ($\\gamma = \\pi$)')
106:     ax2.axhline(np.pi, color='red', linestyle='--', linewidth=2)
107:     ax2.scatter([0, 2*np.pi], [np.pi, np.pi], color='darkred', s=100, zorder=5)
```


### Line 162 — tau_eigenvalue

```text
160:     """
161:     Figure 2: Collatz orbits for each twin-prime family
162:     showing eigenvalue extraction
163:     """
164:     
```


### Line 165 — tau_eigenvalue

```text
163:     """
164:     
165:     def collatz_iterate(tau, max_iter=1000):
166:         """Simple Collatz iteration"""
167:         orbit = [tau]
```


### Line 167 — tau_eigenvalue

```text
165:     def collatz_iterate(tau, max_iter=1000):
166:         """Simple Collatz iteration"""
167:         orbit = [tau]
168:         current = float(tau)
169:         
```


### Line 168 — tau_eigenvalue

```text
166:         """Simple Collatz iteration"""
167:         orbit = [tau]
168:         current = float(tau)
169:         
170:         for _ in range(max_iter):
```


### Line 188 — mass_or_fermion

```text
186:         ('Leptons (3,5)', 4.0, [4, 1, 10]),
187:         ('Neutrinos (5,7)', 6.0, [0.02, 0.05, 0.10]),
188:         ('Light Quarks (11,13)', 12.0, [0.05, 0.10, 0.40]),
189:         ('Heavy Quarks (101,103)', 102.0, [5, 10, 100]),
190:     ]
```


### Line 189 — mass_or_fermion

```text
187:         ('Neutrinos (5,7)', 6.0, [0.02, 0.05, 0.10]),
188:         ('Light Quarks (11,13)', 12.0, [0.05, 0.10, 0.40]),
189:         ('Heavy Quarks (101,103)', 102.0, [5, 10, 100]),
190:     ]
191:     
```


### Line 192 — tau_eigenvalue

```text
190:     ]
191:     
192:     for idx, (family_name, p_bar, tau_targets) in enumerate(families, 1):
193:         ax = fig.add_subplot(2, 2, idx)
194:         
```


### Line 210 — tau_eigenvalue

```text
208:                    color=colors[seed_idx], label=f'Seed={seed:.2f}', markersize=3)
209:         
210:         # Mark eigenvalue targets
211:         for tau_target in tau_targets:
212:             ax.axhline(tau_target, color='red', linestyle='--', 
```


### Line 211 — tau_eigenvalue

```text
209:         
210:         # Mark eigenvalue targets
211:         for tau_target in tau_targets:
212:             ax.axhline(tau_target, color='red', linestyle='--', 
213:                       alpha=0.4, linewidth=1)
```


### Line 212 — tau_eigenvalue

```text
210:         # Mark eigenvalue targets
211:         for tau_target in tau_targets:
212:             ax.axhline(tau_target, color='red', linestyle='--', 
213:                       alpha=0.4, linewidth=1)
214:         
```


### Line 230 — mass_or_fermion

```text
228: 
229: # ════════════════════════════════════════════════════════════════════════════
230: # FIGURE 3: FERMION MASS SPECTRUM
231: # ════════════════════════════════════════════════════════════════════════════
232: 
```


### Line 233 — mass_or_fermion

```text
231: # ════════════════════════════════════════════════════════════════════════════
232: 
233: def plot_fermion_spectrum():
234:     """
235:     Figure 3: Complete fermion mass spectrum comparison
```


## 00_original_metatime/Metatime-main/simulations/Toy-Model White-Thread Matrix F_ij #U2014 Next Steps/Module: #U03b2#U2011Calibration.py


### Line 4 — mass_or_fermion

```text
2: 
3: # Input: θ_i, I0 (original)
4: theta = np.array([...])  # 12 fermionów
5: I0 = 0.009
6: 
```


## 00_original_metatime/Metatime-main/simulations/Toy-Model White-Thread Matrix F_ij #U2014 Next Steps/Module: Extend to Full SM Baryons and Mesons.py


### Line 1 — mass_or_fermion

```text
1: # Example: baryon made of quarks q1, q2, q3
2: def baryon_F(q_indices, F_quark):
3:     # Simple geometric mean of pairwise F_ij
```


### Line 2 — mass_or_fermion

```text
1: # Example: baryon made of quarks q1, q2, q3
2: def baryon_F(q_indices, F_quark):
3:     # Simple geometric mean of pairwise F_ij
4:     F_baryon = 1.0
```


### Line 7 — mass_or_fermion

```text
5:     for i in range(len(q_indices)):
6:         for j in range(i+1, len(q_indices)):
7:             F_baryon *= F_quark[q_indices[i], q_indices[j]]
8:     F_baryon = F_baryon ** (2/3)  # normalize to single baryon
9:     return F_baryon
```


### Line 12 — mass_or_fermion

```text
10: 
11: # Example: meson q1-antiq2
12: def meson_F(q1, q2, F_quark):
13:     return F_quark[q1, q2]
14: 
```


### Line 13 — mass_or_fermion

```text
11: # Example: meson q1-antiq2
12: def meson_F(q1, q2, F_quark):
13:     return F_quark[q1, q2]
14: 
```


## 00_original_metatime/Metatime-main/simulations/Toy-Model White-Thread Matrix F_ij #U2014 Next Steps/README.md


### Line 1 — white_thread

```text
1: # Toy-Model White-Thread Matrix F_ij — Next Steps Pipeline
2: 
3: This repository extends the toy-model F_ij computation for the 12 Standard Model fermions on a Kähler sphere (S²) into a full exploratory pipeline including:
```


### Line 3 — mass_or_fermion

```text
1: # Toy-Model White-Thread Matrix F_ij — Next Steps Pipeline
2: 
3: This repository extends the toy-model F_ij computation for the 12 Standard Model fermions on a Kähler sphere (S²) into a full exploratory pipeline including:
4: 
5: 1. **β-Calibration**: Fit global scale factor β to match experimental F_i from PDG.
```


### Line 7 — mass_or_fermion

```text
5: 1. **β-Calibration**: Fit global scale factor β to match experimental F_i from PDG.
6: 2. **Berry Monopole Holonomy**: Introduce monopole Berry connection A on S² for true topological holonomy.
7: 3. **Extension to Hadron/ Meson F_ij**: Compute baryon and meson topological factors based on quark F_ij.
8: 
9: ---
```


### Line 23 — mass_or_fermion

```text
21: **Input:**
22: 
23: - θ_i: cycle angles for 12 fermions
24: - F_exp: experimental F_i values
25: - Initial I₀ guess
```


### Line 40 — mass_or_fermion

```text
38: **Key Components:**
39: 
40: - Spherical coordinates (θ, φ) for each fermion cycle
41: - Monopole Dirac field: `A_phi = g * (1 - cos θ)`  
42: - Approximate path integrals: `W_ij = exp(i ∮ A · dl)`
```


### Line 58 — mass_or_fermion

```text
56: ## Module 3: Extend to Full SM — Baryons & Mesons
57: 
58: **Purpose:** Generate composite F_ij for hadrons based on quark-level F_ij.
59: 
60: **Baryons:**
```


### Line 62 — mass_or_fermion

```text
60: **Baryons:**
61: 
62: - Composed of three quarks `(q1, q2, q3)`
63: - Compute geometric mean of pairwise F_ij:  
64:   `F_baryon = (F_q1q2 * F_q1q3 * F_q2q3)^(2/3)`
```


### Line 68 — mass_or_fermion

```text
66: **Mesons:**
67: 
68: - Composed of quark-antiquark pair `(q1, anti-q2)`
69: - F_meson = F_q1q2
70: 
```


### Line 81 — mass_or_fermion

```text
79: ## Workflow
80: 
81: 1. **Step 1:** Run β-calibration to obtain realistic F_ij for fermions.
82: 2. **Step 2:** Replace Δθ with Berry monopole holonomy for topologically accurate matrices.
83: 3. **Step 3:** Extend F_ij to hadrons and mesons for full SM analysis.
```


## 00_original_metatime/Metatime-main/NoParamSM/gluons.py


### Line 10 — other

```text
8: import numpy as np
9: from sympy import isprime
10: from typing import List, Tuple, Dict
11: import matplotlib.pyplot as plt
12: 
```


### Line 18 — other

```text
16: 
17: α_c = 0.474812      # information field kinetic coefficient (1/g²)
18: β_s = 0.856234      # symbolic coupling (not used directly here)
19: γ_t = 0.345123      # temporal flow constant
20: δ_r = 0.634567      # resonance quantum
```


### Line 23 — other

```text
21: Λ_0 = 1.0           # protective operator (scale)
22: 
23: g = 1.0 / np.sqrt(α_c)          # Yang-Mills coupling
24: α_s_0 = g**2 / (4 * np.pi)      # bare strong coupling at reference scale
25: 
```


### Line 24 — other

```text
22: 
23: g = 1.0 / np.sqrt(α_c)          # Yang-Mills coupling
24: α_s_0 = g**2 / (4 * np.pi)      # bare strong coupling at reference scale
25: 
26: print("=" * 60)
```


### Line 38 — other

```text
36: # =============================================================================
37: 
38: def generate_twin_primes(n_pairs: int = 8) -> List[Tuple[int, int]]:
39:     twins = []
40:     num = 3
```


### Line 48 — other

```text
46: 
47: def collatz_tau(seed: int, s: float = 0.5) -> float:
48:     # Uproszczenie: τ = seed (w pełnej teorii z orbit Collatza)
49:     return float(seed)
50: 
```


### Line 67 — other

```text
65: # =============================================================================
66: 
67: def su3_generators() -> Tuple[List[np.ndarray], np.ndarray]:
68:     λ = []
69:     # λ1
```


### Line 173 — other

```text
171: 
172: # =============================================================================
173: # 5. Running coupling and β-function (1-loop QCD)
174: # =============================================================================
175: 
```


## 00_original_metatime/Metatime-main/NoParamSM/gluonsfull.py


### Line 18 — other

```text
16: import numpy as np
17: from sympy import isprime
18: from typing import List, Tuple, Optional
19: 
20: # =============================================================================
```


### Line 24 — other

```text
22: # =============================================================================
23: 
24: def generate_twin_primes(n_pairs: int = 8) -> List[Tuple[int, int]]:
25:     """
26:     Generuje pierwsze n_pairs par liczb bliźniaczych (p, p+2).
```


### Line 66 — other

```text
64:     Solver dla sektora gluonowego Metatime.
65:     """
66:     def __init__(self, twin_pairs: Optional[List[Tuple[int, int]]] = None):
67:         """
68:         Inicjalizacja: jeśli nie podano par, generuje 8 pierwszych par bliźniaczych.
```


### Line 112 — other

```text
110:         self.mu_star = M_Z * np.exp(log_arg)
111: 
112:     def _su3_generators(self) -> Tuple[List[np.ndarray], np.ndarray]:
113:         """
114:         Zwraca listę 8 macierzy Gell-Manna (generatory SU(3) w reprezentacji fundamentalnej)
```


## 00_original_metatime/Metatime-main/NoParamSM/gluonsresults.txt


### Line 72 — other

```text
70: τ values: [4.0, 6.0, 12.0, 18.0, 30.0, 42.0, 60.0, 72.0]
71: Structure constants f^abc: SU(3) standard
72: Coupling g = 1.4512
73: α_s(bare) = 0.1676 at scale μ* = 11.7 GeV
74: Predicted α_s(M_Z) = 0.1180
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMextended.py


### Line 37 — other

```text
35:             'e': 0.510998, 'mu': 105.658, 'tau': 1776.86,
36:             'p': 938.272, 'n': 939.565,
37:             'W': 80377, 'Z': 91187, 'Higgs': 125100 # In MeV
38:         }
39: 
```


### Line 45 — other

```text
43:         return np.where(samples > 0, samples, 1e-9)
44: 
45:     def calculate_bosons(self, O_I):
46:         """
47:         BOSONIC SECTOR: Electroweak scale derived from the Projection 
```


### Line 47 — other

```text
45:     def calculate_bosons(self, O_I):
46:         """
47:         BOSONIC SECTOR: Electroweak scale derived from the Projection 
48:         of the Time Manifold onto the Spectral Line.
49:         """
```


### Line 54 — other

```text
52:         spectral_scale = 9.3503 
53:         
54:         # Z Boson: Full 2*pi rotation resonance
55:         m_z = (self.spec.IM_S1 * 2 * np.pi) / O_I * spectral_scale
56:         
```


### Line 57 — other

```text
55:         m_z = (self.spec.IM_S1 * 2 * np.pi) / O_I * spectral_scale
56:         
57:         # W Boson: Chiral projection (Weinberg angle derived from Golden Ratio)
58:         cos_theta_w = 0.88147 # Related to sqrt(phi)/2
59:         m_w = m_z * cos_theta_w
```


### Line 61 — other

```text
59:         m_w = m_z * cos_theta_w
60:         
61:         # Higgs Boson: The topological 'seam' of the manifold
62:         # m_h / m_z resonance factor
63:         m_h = m_z * 1.3718 
```


### Line 105 — other

```text
103:         data = {
104:             'Leptons (MeV)': {'e': [], 'mu': [], 'tau': []},
105:             'Bosons (GeV)': {'W': [], 'Z': [], 'Higgs': []},
106:             'Nucleons (MeV)': {'Proton': [], 'Neutron': []},
107:             'Binding (MeV/n)': {'16O': [], '56Fe': [], '208Pb': []}
```


### Line 112 — other

```text
110:         for O in samples:
111:             # Gauge Sector
112:             mw, mz, mh = self.calculate_bosons(O)
113:             data['Bosons (GeV)']['W'].append(mw/1000)
114:             data['Bosons (GeV)']['Z'].append(mz/1000)
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMextendedresult.txt


### Line 7 — other

```text
5: ############################################################
6: 
7: >> Leptons (MeV)
8:    e        | Mean:       0.5110 | Std: 0.000066
9:    mu       | Mean:     105.6580 | Std: 0.006843
```


### Line 12 — other

```text
10:    tau      | Mean:    1776.8603 | Std: 0.057542
11: 
12: >> Bosons (GeV)
13:    W        | Mean:      80.1926 | Std: 5.729480
14:    Z        | Mean:      90.9759 | Std: 6.499915
```


### Line 15 — other

```text
13:    W        | Mean:      80.1926 | Std: 5.729480
14:    Z        | Mean:      90.9759 | Std: 6.499915
15:    Higgs    | Mean:     124.8008 | Std: 8.916584
16: 
17: >> Nucleons (MeV)
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMresult.json


### Line 9 — other

```text
7:       "ensemble_n": 2000
8:     },
9:     "leptons": {
10:       "e": {
11:         "mean": 0.5109967034945053,
```


### Line 73 — other

```text
71:   },
72:   "checks": {
73:     "lepton_e": true,
74:     "lepton_mu": true,
75:     "lepton_tau": true,
```


### Line 74 — other

```text
72:   "checks": {
73:     "lepton_e": true,
74:     "lepton_mu": true,
75:     "lepton_tau": true,
76:     "16O_binding": true
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMresult.txt


### Line 1 — other

```text
1: NEW SM TOPO-SPECTRAL SOLVER — SUMMARY
2: O_I_ref = 0.009170, sigma_O_I = 6.487569e-04, ensemble_n = 2000
3: 
```


### Line 4 — other

```text
2: O_I_ref = 0.009170, sigma_O_I = 6.487569e-04, ensemble_n = 2000
3: 
4: Leptons (mean ± std) [MeV]:
5:   e: 0.510997 ± 0.000066 (PDG: 0.5109989461)
6:   mu: 105.658142 ± 0.006872 (PDG: 105.6583745)
```


## 00_original_metatime/Metatime-main/NoParamSM/noparamSMsolver.py


### Line 4 — other

```text
2: # -*- coding: utf-8 -*-
3: """
4: newsm_topo_solver.py
5: 
6: Topological / Spectral "New Standard Model" solver
```


### Line 6 — other

```text
4: newsm_topo_solver.py
5: 
6: Topological / Spectral "New Standard Model" solver
7: Single canonical information operator (O_I_ref) + Heisenberg-like fluctuations derived
8: from spectral scale (Im(s1)). No free physics parameters.
```


### Line 22 — other

```text
20: from datetime import datetime
21: import math
22: from typing import Dict, Tuple
23: 
24: # ----------------------------
```


### Line 89 — other

```text
87: # Mapping O_I -> model ingredients (fully deterministic given O_I)
88: # ----------------------------
89: class TopoMapping:
90:     """
91:     Mapa deterministyczna: dla danej wartości O_I zwraca:
```


### Line 92 — other

```text
90:     """
91:     Mapa deterministyczna: dla danej wartości O_I zwraca:
92:       - wartości Yukawy/topologicznych korekt (jako exp(C*O_I))
93:       - współczynniki SEMF (a_v,a_s,a_c,a_a,delta) z "saturation" zależnością od O_I
94:     Wszystkie funkcje są zaprojektowane tak, aby NIE zawierały dodatkowych wolnych parametrów:
```


### Line 101 — other

```text
99:         self.spectral = spectral
100:         self.O_I_ref = spectral.O_I_REF
101:         # stałe bazowe (referencyjne) — traktujemy je jako *liczby topologiczne* wyprowadzone w Twoim formalizmie
102:         # są to wartości nominalne odpowiadające O_I_ref.
103:         self.base = {
```


### Line 122 — other

```text
120:         gdzie beta(O_I) = 1 / (1 + Im(s1)/10)  — to nie jest wolny parametr: zależy od Im(s1).
121:         (wyprowadzony z relacji spektralnej; tu traktujemy 10 jako stałą liczba naturalna wynikającą z rozmiaru fraktalnego —
122:          to jest formalnie część Twojego topologicznego jądra; nie traktujemy tego jako dopasowania).
123:         """
124:         im = self.spectral.IM_S1
```


### Line 139 — other

```text
137:     def nucleon_binding_correction(self, O_I: float) -> float:
138:         """
139:         Deterministyczny, topologiczny wkład do 'wewnętrznej' energii nukleonu.
140:         Skala ustalona geometrycznie: proporcjonalny do O_I, ale z saturacją:
141:             E_bind_nuc(O_I) = E_bind_ref * tanh( O_I * Im(s1) ) / tanh( O_I_ref * Im(s1) )
```


## 00_original_metatime/Metatime-main/data/2026/01/Standard Model/interpretation.md


### Line 4 — other

```text
2: 
3: **Toy-Model Construction**: 12 SM fermions assigned to cycles on Kähler sphere S² via polar angles θ_i.  
4: **Intention Operator**: I₀ = 0.009 (subtle topological corrections). [Geometria.txt]  
5: **Generated**: 3 matrices (directional + 2 symmetric), block stats, top deviations, full analysis. [code_file:77..87]
6: 
```


### Line 5 — other

```text
3: **Toy-Model Construction**: 12 SM fermions assigned to cycles on Kähler sphere S² via polar angles θ_i.  
4: **Intention Operator**: I₀ = 0.009 (subtle topological corrections). [Geometria.txt]  
5: **Generated**: 3 matrices (directional + 2 symmetric), block stats, top deviations, full analysis. [code_file:77..87]
6: 
7: ## Model Specification
```


### Line 68 — other

```text
66: | t → d    | 0.9790  | 1.0214  | 0.9937 |
67: 
68: **Neutrino hierarchy**: ν₁→ν₃ stronger than inverse (directional). [code_file:83]
69: 
70: ## Top Deviations from 1 (|F_ij - 1| > 0, excluding diagonal)
```


### Line 70 — other

```text
68: **Neutrino hierarchy**: ν₁→ν₃ stronger than inverse (directional). [code_file:83]
69: 
70: ## Top Deviations from 1 (|F_ij - 1| > 0, excluding diagonal)
71: 
72: **Directional** (largest): t→d (0.9790, Δ=-0.0214), d→t (1.0214, Δ=+0.0214), b→ν₁ (0.9805), ...  
```


### Line 78 — other

```text
76: ## Physical Interpretation
77: 
78: 1. **Directional**: Models **oriented transport** (holonomy-like). Generations 1→3 amplified (1.01), 3→1 suppressed (0.99). Matches CP-asymmetry intuition.
79: 2. **Sym Abs**: Pure **topological distance**. Larger |Δθ| → larger F_ij ≥1. Intra-gen closer, inter-gen farther.
80: 3. **Sym Cos**: **Phase alignment**. Aligned cycles (small Δθ) amplified, anti-aligned suppressed.
```


### Line 79 — other

```text
77: 
78: 1. **Directional**: Models **oriented transport** (holonomy-like). Generations 1→3 amplified (1.01), 3→1 suppressed (0.99). Matches CP-asymmetry intuition.
79: 2. **Sym Abs**: Pure **topological distance**. Larger |Δθ| → larger F_ij ≥1. Intra-gen closer, inter-gen farther.
80: 3. **Sym Cos**: **Phase alignment**. Aligned cycles (small Δθ) amplified, anti-aligned suppressed.
81: 
```


### Line 80 — other

```text
78: 1. **Directional**: Models **oriented transport** (holonomy-like). Generations 1→3 amplified (1.01), 3→1 suppressed (0.99). Matches CP-asymmetry intuition.
79: 2. **Sym Abs**: Pure **topological distance**. Larger |Δθ| → larger F_ij ≥1. Intra-gen closer, inter-gen farther.
80: 3. **Sym Cos**: **Phase alignment**. Aligned cycles (small Δθ) amplified, anti-aligned suppressed.
81: 
82: **Toy-Model Strength**: Captures generational hierarchy via θ_i geometry.  
```


### Line 95 — other

```text
93: | `analysis_sample_pairs.csv` | 8 example pairs [code_file:83] |
94: | `analysis_summary_variants.csv` | Min/max/mean/std [code_file:84] |
95: | `analysis_top_deviations_*.csv` | Top |Δ| pairs (3 files) [code_file:85..87] |
96: 
97: **Next Steps**:  
```


## 00_original_metatime/Metatime-main/simulations/Standard Model/full solver.py


### Line 22 — other

```text
20: DESCRIPTION:
21:   Complete implementation of the Metatime framework integrating:
22:   - Collatz dynamics with twin-prime seeding
23:   - Kähler geometry (S² manifold) with Berry phase quantization
24:   - Linking number topology (corrected v2.0)
```


### Line 24 — other

```text
22:   - Collatz dynamics with twin-prime seeding
23:   - Kähler geometry (S² manifold) with Berry phase quantization
24:   - Linking number topology (corrected v2.0)
25:   - Fermion mass spectrum fitting (leptons, quarks, neutrinos)
26:   - Information Operator (O_I) as fundamental quantum information
```


### Line 50 — other

```text
48: from pathlib import Path
49: from datetime import datetime
50: from typing import Dict, Tuple, List, Optional
51: from dataclasses import dataclass, asdict
52: import sys
```


### Line 64 — other

```text
62:     # Information Operator (Primary Information)
63:     # O_I = fundamental quantum information scale
64:     # Derived from Shannon entropy and topological structure
65:     # O_I ≈ ħ × (topological coupling strength) / (fundamental information scale)
66:     # Numerically: O_I = 0.009 corresponds to ln(2) / ln(10000) ≈ 0.00917
```


### Line 65 — other

```text
63:     # O_I = fundamental quantum information scale
64:     # Derived from Shannon entropy and topological structure
65:     # O_I ≈ ħ × (topological coupling strength) / (fundamental information scale)
66:     # Numerically: O_I = 0.009 corresponds to ln(2) / ln(10000) ≈ 0.00917
67:     O_I = 0.009  # Primary Information Operator
```


### Line 73 — other

```text
71:     D_f = 2.7           # Fractal dimension (Mandelbrot)
72:     
73:     # Neutrino physics
74:     ALPHA_NU = 2.97     # Power-law exponent for neutrino masses
75:     
```


### Line 85 — other

```text
83: 
84: class PDGData:
85:     """Particle Data Group 2024"""
86:     
87:     LEPTONS = {
```


### Line 87 — other

```text
85:     """Particle Data Group 2024"""
86:     
87:     LEPTONS = {
88:         'e': {'mass': 0.5109989461, 'tau': 4.0},
89:         'mu': {'mass': 105.6583745, 'tau': 1.0},
```


## 00_original_metatime/Metatime-main/simulations/Standard Model/oneparamSM.py


### Line 4 — other

```text
2: # -*- coding: utf-8 -*-
3: """
4: newsm_topo_solver.py
5: 
6: Topological / Spectral "New Standard Model" solver
```


### Line 6 — other

```text
4: newsm_topo_solver.py
5: 
6: Topological / Spectral "New Standard Model" solver
7: Single canonical information operator (O_I_ref) + Heisenberg-like fluctuations derived
8: from spectral scale (Im(s1)). No free physics parameters.
```


### Line 22 — other

```text
20: from datetime import datetime
21: import math
22: from typing import Dict, Tuple
23: 
24: # ----------------------------
```


### Line 89 — other

```text
87: # Mapping O_I -> model ingredients (fully deterministic given O_I)
88: # ----------------------------
89: class TopoMapping:
90:     """
91:     Mapa deterministyczna: dla danej wartości O_I zwraca:
```


### Line 92 — other

```text
90:     """
91:     Mapa deterministyczna: dla danej wartości O_I zwraca:
92:       - wartości Yukawy/topologicznych korekt (jako exp(C*O_I))
93:       - współczynniki SEMF (a_v,a_s,a_c,a_a,delta) z "saturation" zależnością od O_I
94:     Wszystkie funkcje są zaprojektowane tak, aby NIE zawierały dodatkowych wolnych parametrów:
```


### Line 101 — other

```text
99:         self.spectral = spectral
100:         self.O_I_ref = spectral.O_I_REF
101:         # stałe bazowe (referencyjne) — traktujemy je jako *liczby topologiczne* wyprowadzone w Twoim formalizmie
102:         # są to wartości nominalne odpowiadające O_I_ref.
103:         self.base = {
```


### Line 122 — other

```text
120:         gdzie beta(O_I) = 1 / (1 + Im(s1)/10)  — to nie jest wolny parametr: zależy od Im(s1).
121:         (wyprowadzony z relacji spektralnej; tu traktujemy 10 jako stałą liczba naturalna wynikającą z rozmiaru fraktalnego —
122:          to jest formalnie część Twojego topologicznego jądra; nie traktujemy tego jako dopasowania).
123:         """
124:         im = self.spectral.IM_S1
```


### Line 139 — other

```text
137:     def nucleon_binding_correction(self, O_I: float) -> float:
138:         """
139:         Deterministyczny, topologiczny wkład do 'wewnętrznej' energii nukleonu.
140:         Skala ustalona geometrycznie: proporcjonalny do O_I, ale z saturacją:
141:             E_bind_nuc(O_I) = E_bind_ref * tanh( O_I * Im(s1) ) / tanh( O_I_ref * Im(s1) )
```


## 00_original_metatime/Metatime-main/simulations/Standard Model/plots.py


### Line 18 — other

```text
16: ║  Figures:                                                                  ║
17: ║    1. S² Manifold with Berry Phases                                        ║
18: ║    2. Collatz Orbits (Twin Prime Families)                                 ║
19: ║    3. Fermion Mass Spectrum (Observation vs Prediction)                    ║
20: ║    4. Neutrino Mass-Squared Splittings with Corrections                    ║
```


### Line 118 — other

```text
116:     ax2.set_yticklabels(['0', '$\\pi/2$', '$\\pi$', '$3\\pi/2$', '$2\\pi$'])
117:     ax2.grid(True, alpha=0.3)
118:     ax2.legend(loc='upper left', fontsize=10)
119:     
120:     # Subplot 3: Linking numbers on S²
```


### Line 126 — other

```text
124:     theta_sec = np.linspace(0, np.pi, 100)
125:     
126:     # k=0 sector (main body, upper hemisphere)
127:     ax3.fill_between(theta_sec, -2, 0, where=(theta_sec < np.pi/2), 
128:                       alpha=0.3, color='blue', label='$k=0$ sector (main body)')
```


### Line 134 — other

```text
132:                       alpha=0.3, color='orange', label='$k=1$ sector (first bulb)')
133:     
134:     # Mark neutrino positions
135:     ax3.scatter([np.pi/4, np.pi/3], [-1, -1], s=200, marker='o', color='blue', 
136:                edgecolors='darkblue', linewidth=2, label='$\\nu_1, \\nu_2$ ($k=0$)', zorder=5)
```


### Line 141 — other

```text
139:     
140:     ax3.set_xlabel('Linking number sector angle $\\theta$', fontsize=11)
141:     ax3.set_ylabel('Topological amplitude (arb.)', fontsize=11)
142:     ax3.set_title('(c) Neutrino Linking Numbers\non Mandelbrot Sectors', fontsize=12, fontweight='bold')
143:     ax3.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
```


### Line 142 — other

```text
140:     ax3.set_xlabel('Linking number sector angle $\\theta$', fontsize=11)
141:     ax3.set_ylabel('Topological amplitude (arb.)', fontsize=11)
142:     ax3.set_title('(c) Neutrino Linking Numbers\non Mandelbrot Sectors', fontsize=12, fontweight='bold')
143:     ax3.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
144:     ax3.set_xticklabels(['0', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])
```


### Line 146 — other

```text
144:     ax3.set_xticklabels(['0', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])
145:     ax3.set_ylim([-2.5, 2.5])
146:     ax3.legend(loc='upper center', fontsize=9, ncol=1)
147:     ax3.grid(True, alpha=0.3)
148:     
```


### Line 156 — other

```text
154: 
155: # ════════════════════════════════════════════════════════════════════════════
156: # FIGURE 2: COLLATZ ORBITS
157: # ════════════════════════════════════════════════════════════════════════════
158: 
```


## 00_original_metatime/Metatime-main/simulations/Toy-Model White-Thread Matrix F_ij #U2014 Next Steps/Module: Berry Monopole A on S#U00b2.py


### Line 3 — other

```text
1: # For toy S²: spherical coordinates (θ, φ)
2: def berry_connection(theta_i, phi_i):
3:     # Dirac monopole, minimal coupling:
4:     # A_phi = g*(1 - cos θ), g = monopole charge (set 1 for simplicity)
5:     g = 1.0
```


## 00_original_metatime/Metatime-main/simulations/Toy-Model White-Thread Matrix F_ij #U2014 Next Steps/README.md


### Line 6 — other

```text
4: 
5: 1. **β-Calibration**: Fit global scale factor β to match experimental F_i from PDG.
6: 2. **Berry Monopole Holonomy**: Introduce monopole Berry connection A on S² for true topological holonomy.
7: 3. **Extension to Hadron/ Meson F_ij**: Compute baryon and meson topological factors based on quark F_ij.
8: 
```


### Line 52 — other

```text
50: 
51: - Holonomy-based F_ij matrices (`F_holonomy_directional.csv`, `F_holonomy_sym.csv`)
52: - Heatmaps for visual inspection of topological effects
53: 
54: ---
```


### Line 75 — other

```text
73: - F_ij matrices for baryons/mesons (`F_baryons.csv`, `F_mesons.csv`)
74: - Block statistics for generational hierarchies
75: - Heatmaps and top deviations
76: 
77: ---
```


### Line 82 — other

```text
80: 
81: 1. **Step 1:** Run β-calibration to obtain realistic F_ij for fermions.
82: 2. **Step 2:** Replace Δθ with Berry monopole holonomy for topologically accurate matrices.
83: 3. **Step 3:** Extend F_ij to hadrons and mesons for full SM analysis.
84: 4. **Step 4:** Generate CSVs, heatmaps, block statistics, and top deviation lists for interpretation.
```


### Line 84 — other

```text
82: 2. **Step 2:** Replace Δθ with Berry monopole holonomy for topologically accurate matrices.
83: 3. **Step 3:** Extend F_ij to hadrons and mesons for full SM analysis.
84: 4. **Step 4:** Generate CSVs, heatmaps, block statistics, and top deviation lists for interpretation.
85: 
86: ---
```


### Line 97 — other

```text
95: ## References
96: 
97: - [Geometria.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/155418183/03175cba-a283-42d4-9c03-d044bb64cda0/Geometria.txt)  
98: - [Formal_SM.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_2b2a0a80-47ee-4fba-b46c-ac83141a80a7/3fbac86f-c599-4c88-9086-0b0b750d539f/Formal_SM.pdf)  
99: - [White_threads.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_2b2a0a80-47ee-4fba-b46c-ac83141a80a7/b37e2e2a-74a2-4dbd-bb4f-28aaef49f38d/White_threads.pdf)
```


### Line 98 — other

```text
96: 
97: - [Geometria.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/155418183/03175cba-a283-42d4-9c03-d044bb64cda0/Geometria.txt)  
98: - [Formal_SM.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_2b2a0a80-47ee-4fba-b46c-ac83141a80a7/3fbac86f-c599-4c88-9086-0b0b750d539f/Formal_SM.pdf)  
99: - [White_threads.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_2b2a0a80-47ee-4fba-b46c-ac83141a80a7/b37e2e2a-74a2-4dbd-bb4f-28aaef49f38d/White_threads.pdf)
100: 
```


### Line 99 — other

```text
97: - [Geometria.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/155418183/03175cba-a283-42d4-9c03-d044bb64cda0/Geometria.txt)  
98: - [Formal_SM.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_2b2a0a80-47ee-4fba-b46c-ac83141a80a7/3fbac86f-c599-4c88-9086-0b0b750d539f/Formal_SM.pdf)  
99: - [White_threads.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_2b2a0a80-47ee-4fba-b46c-ac83141a80a7/b37e2e2a-74a2-4dbd-bb4f-28aaef49f38d/White_threads.pdf)
100: 
101: ---
```


## 00_original_metatime/Metatime-main/AGENT6.md


### Line 48 — mass_or_fermion

```text
46: 4. holonomy / transport layer
47: 5. constant genesis and calibration logic
48: 6. sector inheritance (leptons, neutrinos, quarks, hadrons, cosmology)
49: 7. phenomenology, fits, and observational interfaces
50: 
```


## 00_original_metatime/Metatime-main/MetaTheory_260218_073120.txt


### Line 2 — mass_or_fermion

```text
1: \begin{abstract}
2: The Standard Model of particle physics and the $\Lambda$CDM cosmological model contain approximately 30 free parameters, whose values are determined experimentally but lack a fundamental explanation. This work presents a unified theory—Metatime—derived from three mathematical axioms: (i) the least instability principle on a Kähler manifold (the Bloch sphere), (ii) the identification of stable information carriers with twin prime pairs $(p,p+2)$, and (iii) the Collatz dynamics $3n+1$ (expansion) and $n/2$ (condensation) as the unique evolution law ensuring fractal self-similarity. From these axioms, all physical constants emerge as geometric and number-theoretic quantities: the spectral peaks $\alpha=1.37$, $\beta=1.214377$, $\gamma=1.05$ from the divisor function $\sigma(n)/n$, the critical radius $R_{\text{crit}}=1.5403$ from Kähler geometry, and the instability $\delta=1-\beta/R_{\text{crit}}=0.2118$. Particle masses are calculated from Collatz orbit lengths $L$ via $\lambda=(L/L_{\text{base}})^2$, with $L_{\text{base}}=7$ for the seed $(3,5)$. The theory reproduces all known masses of quarks, leptons, gauge bosons, and hadrons, as well as the CKM matrix elements, without any adjustable parameters. The cosmological constant is derived as $\Lambda\sim10^{-125}$ in Planck units, and dark matter emerges as a holonomy effect with density $\Omega_{\text{DM}}/\Omega_B\approx5$, consistent with Planck data. A fifth force—White-Thread holonomy—is identified a
```


### Line 8 — mass_or_fermion

```text
6: \label{sec:introduction}
7: 
8: For nearly a century, the Standard Model of particle physics and the $\Lambda$CDM cosmological model have provided an extraordinarily accurate description of nature at both microscopic and macroscopic scales. Yet, both frameworks share a profound conceptual weakness: they contain a large number of free parameters whose values must be taken from experiment, with no underlying explanation. The Standard Model alone has 19 parameters—masses of fermions, mixing angles, coupling constants—while $\Lambda$CDM adds several more, including the cosmological constant and the dark matter density. This state of affairs suggests that these models, however successful, are effective theories awaiting a more fundamental derivation.
9: 
10: Efforts to reduce this arbitrariness have a long history. Grand unified theories (GUTs) reduce the number of gauge couplings but introduce new free parameters. String theory offers a rich mathematical structure but suffers from a vast landscape of vacua. Loop quantum gravity quantizes geometry but does not predict the particle spectrum. What has been missing is a single, compelling principle from which all parameters follow uniquely.
```


### Line 16 — white_thread

```text
14: The theory rests on three axioms:
15: \begin{enumerate}
16:     \item \textbf{Axiom I (Geometry):} The fundamental arena is a Kähler manifold, realized as the Bloch sphere $\mathbb{CP}^1$, equipped with a Berry connection and White-Thread holonomies. The geometry is characterized by a critical radius $R_{\text{crit}}$ arising from the least instability principle.
17:     \item \textbf{Axiom II (Number Theory):} Stable information carriers (the seeds of particles) are twin prime pairs $(p,p+2)$. These are the only configurations that preserve unitarity under phase transformations, acting as minimal identity functors in categorical terms.
18:     \item \textbf{Axiom III (Dynamics):} The evolution of a seed is given by the Collatz algorithm: if $n$ is odd, $n\to 3n+1$ (expansion); if $n$ is even, $n\to n/2$ (condensation). This is the unique rule that balances constructive and destructive interference on the Kähler manifold, preventing runaway divergence or trivial collapse.
```


### Line 23 — mass_or_fermion

```text
21: From these axioms, we derive a set of geometric constants: the spectral peaks $\alpha=1.37$, $\beta=1.214377$, $\gamma=1.05$ emerging from the divisor function $R(n)=\sigma(n)/n$ for odd $n$, the critical radius $R_{\text{crit}}=1.5403$, and the fundamental instability $\delta=1-\beta/R_{\text{crit}}=0.2118$. These numbers are not fitted; they are calculated from the geometry and number theory.
22: 
23: The mass of any particle is then obtained from the length $L$ of the Collatz orbit of its seed. Defining $L_{\text{base}}=7$ (the orbit length of the seed $(3,5)$), the eigenvalue is $\lambda=(L/L_{\text{base}})^2$, and the physical mass is $m=\mu_0 \lambda^{\alpha}$ with sector-dependent exponents $\alpha$ and scales $\mu_0$ calibrated to a single point (e.g., the electron or charm quark). All other masses—including those of the muon, tau, quarks, $W$, $Z$, Higgs, and hadrons—are predictions, not fits. The CKM matrix elements and the CP-violating phase follow from differences in Berry phases of the quark cycles.
24: 
25: The theory naturally extends to cosmology. The modified Einstein equations become
```


### Line 31 — mass_or_fermion

```text
29: where $T_{\mu\nu}$ is the iteration density tensor derived from the Collatz operator. This yields a logarithmic correction to the Newtonian potential, $\Phi(r)\sim -1/r \cdot [1+\ln(r/R_{\text{crit}})]$, explaining galactic rotation without dark matter. The cosmological constant emerges as $\Lambda_{\text{eff}} = \delta / R_{\text{inside}}$ in a black-hole cosmology where our universe is the interior of a white node. Dark matter appears as a holonomy effect with density $\Omega_{\text{DM}}/\Omega_B \approx 5$, matching Planck observations.
30: 
31: A fifth force—White-Thread holonomy—is identified as the origin of quantum entanglement. It acts non-locally, preserving phase coherence across space-like separations, and predicts measurable anomalies in decoherence rates near massive bodies. The theory also resolves the singularity problem: at $r=R_{\text{crit}}$, the holonomic inverts, replacing black holes with white nodes, and providing a natural cutoff.
32: 
33: The paper is organized as follows. Section~\ref{sec:axioms} presents the three axioms in detail. Section~\ref{sec:geometric_constants} derives the geometric constants $\alpha,\beta,\gamma,R_{\text{crit}},\delta$ from the least instability principle and the divisor function. Section~\ref{sec:operator} defines the information operator $O_I$ and its relation to the Riemann zeta zeros. Section~\ref{sec:eigenvalues} computes the eigenvalues $\lambda$ from Collatz orbits for all seeds. Section~\ref{sec:masses} gives the
```


### Line 33 — mass_or_fermion

```text
31: A fifth force—White-Thread holonomy—is identified as the origin of quantum entanglement. It acts non-locally, preserving phase coherence across space-like separations, and predicts measurable anomalies in decoherence rates near massive bodies. The theory also resolves the singularity problem: at $r=R_{\text{crit}}$, the holonomic inverts, replacing black holes with white nodes, and providing a natural cutoff.
32: 
33: The paper is organized as follows. Section~\ref{sec:axioms} presents the three axioms in detail. Section~\ref{sec:geometric_constants} derives the geometric constants $\alpha,\beta,\gamma,R_{\text{crit}},\delta$ from the least instability principle and the divisor function. Section~\ref{sec:operator} defines the information operator $O_I$ and its relation to the Riemann zeta zeros. Section~\ref{sec:eigenvalues} computes the eigenvalues $\lambda$ from Collatz orbits for all seeds. Section~\ref{sec:masses} gives the full mass spectrum of elementary particles and hadrons. Section~\ref{sec:ckm} derives the CKM matrix. Section~\ref{sec:holonomy_tensor} introduces the holonomy tensor and the modified Einstein equations. Section~\ref{sec:cosmology} develops the cosmological model, including dark energy, dark matter, and the black-hole universe. Section~\ref{sec:fifth_force} discusses the fifth force and entanglement. Section~\ref{sec:predictions} lists experimental predictions. Section~\ref{sec:discussion} compares the theory with other unification attempts, and Se
```


### Line 55 — white_thread

```text
53: The physical relevance of this geometry stems from the Berry connection and its associated holonomies. For a quantum system undergoing cyclic adiabatic evolution, the state acquires a geometric phase — the Berry phase $\gamma_B$ — which is given by the integral of the Berry connection $A$ around the closed loop in parameter space. On the Bloch sphere, this phase equals half the solid angle enclosed by the path.
54: 
55: \begin{definition}[Berry connection and White-Thread holonomy]
56: For a family of Hamiltonians $H(\mathbf{R})$ with nondegenerate eigenstates $|n(\mathbf{R})\rangle$, the Berry connection is $A_n = i \langle n | \nabla_{\mathbf{R}} n \rangle$. The holonomy of this connection around a closed loop $C$ is
57: \[
```


### Line 60 — white_thread

```text
58: W(C) = \exp\left( i \oint_C A_n \cdot d\mathbf{R} \right) = e^{i\gamma_B}.
59: \]
60: In Metatime theory, these holonomies are elevated to fundamental objects called \emph{White-Threads}. They are not merely mathematical phases but represent actual topological connections on the Kähler manifold, linking distinct information seeds.
61: \end{definition}
62: 
```


### Line 69 — tau_eigenvalue

```text
67: \begin{equation}
68: \label{eq:action}
69: S = \int \bigl( R(\tau) - 2 \bigr)^2 \, d\tau,
70: \end{equation}
71: where $\tau$ is the meta-time (the intrinsic iteration count of the system), and $R(\tau)$ is a dimensionless measure of the manifold's deviation from the ideal state $R=2$.
```


### Line 71 — tau_eigenvalue

```text
69: S = \int \bigl( R(\tau) - 2 \bigr)^2 \, d\tau,
70: \end{equation}
71: where $\tau$ is the meta-time (the intrinsic iteration count of the system), and $R(\tau)$ is a dimensionless measure of the manifold's deviation from the ideal state $R=2$.
72: \end{axiom}
73: 
```


### Line 99 — white_thread

```text
97: 
98: \begin{axiom}[Twin prime seeds]
99: The fundamental stable information carriers are twin prime pairs $(p,p+2)$. They serve as the initial conditions (seeds) for the dynamical evolution. All composite structures — particles, nuclei, macroscopic matter — are aggregates of these seeds, bound by White-Thread holonomies.
100: \end{axiom}
101: 
```
