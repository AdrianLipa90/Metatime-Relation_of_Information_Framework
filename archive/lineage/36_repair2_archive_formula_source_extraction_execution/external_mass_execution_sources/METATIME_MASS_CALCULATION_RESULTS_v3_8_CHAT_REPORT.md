# METATIME — wynik wyliczenia mas z dokumentów v3.8

Proweniencja: REPO_INTERNAL, moduł `36_debt9_fermion_mass_calculation_from_archive_v3_8`.
Repo zmienione przez ten raport: nie. To jest wyciąg z istniejących wyników v3.8.

## Status

- technical: PASS — skrypt policzył tabele.
- formal: PASS — wyniki rozdzielone według trybu/proweniencji.
- substantive: MIXED — archiwalne wzory liczą masy, ale różne tryby mają różny status epistemiczny.
- numeric: TABLES_GENERATED.
- red_alert: raw document power-law nie wystarcza dla wszystkich sektorów; tryb legacy_fit_reconstruction używa danych obserwowanych wewnętrznie; archive_canonical_table jest odtworzeniem tabeli, nie niezależną predykcją.

## Podsumowanie trybów

| mode                          |   n |   median_abs_log_error |   max_abs_log_error |   median_factor_error |   max_factor_error | status                 |
|:------------------------------|----:|-----------------------:|--------------------:|----------------------:|-------------------:|:-----------------------|
| archive_canonical_table_MeV   |  12 |             0          |            0        |               1       |            1       | TAUTOLOGICAL_REFERENCE |
| legacy_fit_reconstruction_MeV |  12 |             0.00470711 |            0.224364 |               1.00472 |            1.25153 | FIT_RECONSTRUCTION     |
| one_anchor_per_sector_MeV     |  12 |             0.0563324  |            9.44928  |               1.05795 |        12699.1     | CALCULATION_TEST       |
| raw_document_power_law_MeV    |  12 |             2.01933    |           13.8155   |               7.53325 |            1e+06   | CALCULATION_TEST       |

## Tabela mas — wyciąg

Wartości w MeV. `doc_reference_mass_MeV` to masa z dokumentu/archiwalnej tabeli referencyjnej.

| particle   | sector         |   lambda_GeV2 |   doc_reference_mass_MeV |   archive_canonical_table_MeV |   legacy_fit_reconstruction_MeV |   one_anchor_per_sector_MeV |   raw_document_power_law_MeV |
|:-----------|:---------------|--------------:|-------------------------:|------------------------------:|--------------------------------:|----------------------------:|-----------------------------:|
| e          | charged_lepton |         4     |                    0.511 |                         0.511 |                        0.510999 |                  0.511      |                     0.511403 |
| mu         | charged_lepton |         1     |                  105.7   |                       105.7   |                      105.658    |                  0.00832344 |                     0.00833  |
| tau        | charged_lepton |        10     |                 1776.9   |                      1776.9   |                     1776.86     |                  7.76788    |                     7.77401  |
| nu1        | neutrino       |         0.002 |                    0.001 |                         0.001 |                        0.001    |                  0.001      |                     1e-09    |
| nu2        | neutrino       |         0.016 |                    0.008 |                         0.008 |                        0.008    |                  0.008      |                     8e-09    |
| nu3        | neutrino       |         0.1   |                    0.05  |                         0.05  |                        0.05     |                  0.05       |                     5e-08    |
| u          | light_quark    |         0.05  |                    2.2   |                         2.2   |                        1.75785  |                  2.2        |                     0.276042 |
| d          | light_quark    |         0.1   |                    4.4   |                         4.4   |                        4.99636  |                  8.04172    |                     1.00902  |
| s          | light_quark    |         0.4   |                   96     |                        96     |                       80.5642   |                107.449      |                    13.482    |
| c          | heavy_quark    |         5     |                 1270     |                      1270     |                     1302.61     |               1270          |                  1269.6      |
| b          | heavy_quark    |        10     |                 4180     |                      4180     |                     4044.37     |               3355.73       |                  3354.68     |
| t          | heavy_quark    |       100     |               172760     |                    172760     |                   174325        |              84642.3        |                 84615.8      |

## Najkrótszy wniosek

Jeżeli użyć pełnych archiwalnych mechanizmów, masy da się odtworzyć. Jeżeli użyć tylko surowego prawa potęgowego z dokumentu, wynik rozjeżdża się w części sektorów. To oznacza, że same dokumenty zawierają zarówno liczby/tabele, jak i dodatkową warstwę solvera, której nie wolno spłaszczać do jednego wzoru.