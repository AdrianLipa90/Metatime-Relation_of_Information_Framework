# Metatime hard-math substitution audit
Generated locally from supplied Metatime-main.zip and external constants.
## Constants
- kappa = ln(2)/(24*pi) = 0.009193150006360
- repo O_I_REF = 0.00917000; relative offset vs kappa = -0.251818%
- gamma_1 = 14.134725141734695; sigma = O_I_REF/gamma_1 = 6.487568670807988e-04
- H0 = 67.4 km/s/Mpc; Omega_Lambda = 0.685; Lambda = 1.090911e-52 m^-2; R_H = 1.372497e+26 m

## Lambda sector
| area_choice   |        A_m2 |   D_Lambda |
|:--------------|------------:|-----------:|
| R_H^2         | 1.88375e+52 |   0.327063 |
| pi R_H^2      | 5.91797e+52 |   1.0275   |
| 4 pi R_H^2    | 2.36719e+53 |   4.11     |

## Neutrino epsilon sector
| case                  |   Delta_m2_eV2 |           L_km |   E_GeV |   theta_rad |   epsilon_nu |   epsilon_mod1 |
|:----------------------|---------------:|---------------:|--------:|------------:|-------------:|---------------:|
| DUNE-like atmospheric |       0.002513 | 1300           |   2.5   | 1.65566     |  0.527015    |       0.527015 |
| T2K-like atmospheric  |       0.002513 |  295           |   0.6   | 1.56545     |  0.498299    |       0.498299 |
| NOvA-like atmospheric |       0.002513 |  810           |   2     | 1.28951     |  0.410463    |       0.410463 |
| Daya Bay reactor atm  |       0.002513 |    1.6         |   0.004 | 1.27359     |  0.405396    |       0.405396 |
| KamLAND solar         |       7.49e-05 |  180           |   0.003 | 5.6939      |  1.81242     |       0.812424 |
| JUNO solar            |       7.49e-05 |   53           |   0.003 | 1.67654     |  0.533658    |       0.533658 |
| Solar 1 AU, 1 MeV     |       7.49e-05 |    1.49598e+08 |   0.001 | 1.41966e+07 |  4.51891e+06 |       0.914069 |

## Closure RHS with A=pi R_H^2
| case                  |   D_disk_plus_epsilon |   nearest_integer |   residual_to_int |   abs_residual |
|:----------------------|----------------------:|------------------:|------------------:|---------------:|
| DUNE-like atmospheric |           1.55451     |                 2 |        -0.445485  |      0.445485  |
| T2K-like atmospheric  |           1.5258      |                 2 |        -0.474201  |      0.474201  |
| NOvA-like atmospheric |           1.43796     |                 1 |         0.437963  |      0.437963  |
| Daya Bay reactor atm  |           1.4329      |                 1 |         0.432896  |      0.432896  |
| KamLAND solar         |           2.83992     |                 3 |        -0.160076  |      0.160076  |
| JUNO solar            |           1.56116     |                 2 |        -0.438842  |      0.438842  |
| Solar 1 AU, 1 MeV     |           4.51891e+06 |           4518914 |        -0.0584314 |      0.0584314 |

## Yukawa-as-holonomy action requirements
| fermion   |      mass_GeV |   y_eff_sqrt2m_over_v |   minus_ln_y |   S_required_if_y_exp_minus_S_over_kappa |   nearest_integer_minus_ln_y |   residual_to_integer |   nearest_gamma1_fraction |
|:----------|--------------:|----------------------:|-------------:|-----------------------------------------:|-----------------------------:|----------------------:|--------------------------:|
| e         |   0.000510999 |           2.93503e-06 |  12.7388     |                              0.11711     |                           13 |           -0.261207   |               0.901241    |
| mu        |   0.105658    |           0.000606871 |   7.40719    |                              0.0680955   |                            7 |            0.407195   |               0.524042    |
| tau       |   1.77686     |           0.0102058   |   4.5848     |                              0.0421488   |                            5 |           -0.415197   |               0.324364    |
| u         |   0.00216     |           1.24064e-05 |  11.2973     |                              0.103858    |                           11 |            0.297297   |               0.799258    |
| d         |   0.00467     |           2.68231e-05 |  10.5262     |                              0.0967694   |                           11 |           -0.473753   |               0.744708    |
| s         |   0.0934      |           0.000536462 |   7.53051    |                              0.0692291   |                            8 |           -0.469486   |               0.532767    |
| c         |   1.27        |           0.00729451  |   4.92063    |                              0.0452361   |                            5 |           -0.0793665  |               0.348124    |
| b         |   4.18        |           0.0240087   |   3.72934    |                              0.0342844   |                            4 |           -0.270661   |               0.263842    |
| t         | 172.69        |           0.991881    |   0.00815235 |                              7.49458e-05 |                            0 |            0.00815235 |               0.000576761 |

## SM anomaly cancellation
```json
{
  "SU3^2_U1": 0.0,
  "SU2^2_U1": 0.0,
  "grav^2_U1": 0.0,
  "U1^3": 2.220446049250313e-16
}
```

## NoParamSM audit
```json
{
  "uses_PDG_dict": true,
  "mass_ref_from_PDG": true,
  "fermion_mass_ref_multiplied": true,
  "C_constants_present": true,
  "heavy_C_zero": true
}
```

Conclusion: numeric scales are coherent in several places, but the present solver uses PDG masses as inputs for much of its output; the theory is not yet a no-parameter derivation until W_s, rho_s(k), A_Sigma, and M_hol are frozen independently.
