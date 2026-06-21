# Metatime — warstwa mas i wektoryzacji Modelu Standardowego v0.1

Status: kandydat kanonicznej warstwy mas; **nie** pełny dowód widma mas.

Cel: przejść od zamkniętego szkieletu cechowania do sektora mas bez traktowania standardowych sprzężeń Yukawy jako parametrów pierwotnych. W tej wersji zamrażamy schemat wektoryzacji i bramki walidacyjne, a nie jeszcze pełne przewidywanie mas.

## 1. Punkt wejścia

Z poprzedniego etapu mamy:

\[
G_{SM}^{global}=rac{SU(3)_c	imes SU(2)_L	imes U(1)_Y}{\mathbb Z_6},
\]

jedną generację z dokładnymi wartościami \(Y\), warunek anulowania anomalii oraz główne połączenie

\[
\mathcal A_{EBI}
=\mathcal A_{AB}+\mathcal A_{Berry}+\mathcal A_{Euler}+\mathcal A_{\mathcal I}.
\]

Warunek domknięcia:

\[
rac1{2\pi}\oint_{\gamma_f}\mathcal A_{EBI}
=D_\Lambda+\epsilon_
u+N_f,\qquad N_f\in\mathbb Z.
\]

Skala informacji:

\[
\kappa=rac{\ln2}{24\pi}=0.009193150006360484.
\]

## 2. Decyzja terminologiczna

Standardowe sprzężenia Yukawy nie są w tej warstwie parametrami fundamentalnymi. Są nazwą efektywną niskoenergetycznej projekcji operatora holonomicznego:

\[
y_f^{eff}
=rac{\sqrt2}{v}
\left|\lambda_f\left(\hat{\mathcal M}_{hol}^{(f)}ight)ight|.
\]

Operator przejścia chiralnego ma postać:

\[
\hat{\mathcal M}_{hol}^{(f)}
=
M_0\,\Pi_{R,f}\,
\mathcal P\exp\left(i\oint_{\gamma_f}\mathcal A_{EBI}ight)\,
\Pi_{L,f}
\exp\left(-rac{\mathcal S_f^{EB}}{\kappa}ight).
\]

Czysta holonomia fazowa ma moduł \(1\). Hierarchia mas nie może więc pochodzić z samej fazy. Musi pochodzić z dodatniego działania geometrycznego:

\[
\mathcal S_f^{EB}\ge 0.
\]

## 3. Wektoryzacja

Dla każdego pola lub seeda definiujemy wektor:

\[
\mathcal V_f
=
\mathbf r_f\oplus\mathbf h_f\oplus\mathbf c_s\oplus\mathbf g_f\oplus\mathbf z_s.
\]

Składniki:

1. \(\mathbf r_f\) — wektor reprezentacji: wymiar koloru, wymiar słaby, chiralność, \(Y\), \(T_3\), \(Q\).
2. \(\mathbf h_f\) — wektor holonomii: \(\Phi_{AB},\Phi_{Berry},\Phi_{Euler},\Theta_{\mathcal I},D_\Lambda,\epsilon_
u,N_f\).
3. \(\mathbf c_s\) — wektor orbity Collatza: twin-prime seed, długość orbity, słowo parzystości, liczba zmian znaku, znormalizowany koszt Collatza.
4. \(\mathbf g_f\) — wektor geometrii: odległość Fubiniego--Study'ego, pole Berry'ego, domknięcie spinorowe Euler, geodezyjna głębia na dysku Poincarégo.
5. \(\mathbf z_s\) — wektor spektralny: etykiety zeta-polarne i etykiety głębi tetraedrycznej, kiedy mapa jest jawna.

Obserwowane masy mogą być dołączone tylko jako **cele walidacyjne**, nie jako wejście do wyprowadzenia.

## 4. Funkcja działania Euler--Berry

Następna właściwa funkcja do wyprowadzenia to:

\[
\mathcal S_f^{EB}=\mathcal S^{EB}(\mathcal V_f).
\]

W tej wersji nie wolno jeszcze wprowadzić swobodnych wag dopasowujących masy. Dopuszczalne są tylko współczynniki pochodzące z wcześniej zamrożonych stałych lub z jawnie wyprowadzonych operatorów geometrii.

Docelowy test masowy ma kolejność:

\[
\mathcal V_f
\longrightarrow
\mathcal S_f^{EB, predicted}
\longrightarrow
y_f^{predicted}=\exp(-\mathcal S_f^{EB}/\kappa)
\longrightarrow
m_f^{predicted}
\]

oraz dopiero potem porównanie z masą obserwowaną.

## 5. Związek ze starym operatorem masy w `MetaTheory`

`MetaTheory_260218_073120.txt` zawiera operator kosztu informacyjnego orbity Collatza:

\[
\hat M\Psi=\deltalpha\sum_{i=0}^{\hat L-1}\log_2(\hat n_i)\Psi.
\]

Ten operator należy zachować jako składnik wektora \(\mathbf c_s\), ale nie traktować go samodzielnie jako pełnego dowodu mas. W nowej warstwie mas koszt Collatza jest jednym z kanałów wejściowych do \(\mathcal S_f^{EB}\), obok domknięcia Euler--Berry, geometrii Fubiniego--Study'ego, głębi Poincarégo i danych reprezentacji.

## 6. Bramka walidacyjna

Twierdzenie o wyprowadzeniu mas jest dopuszczalne tylko wtedy, gdy:

1. \(\mathcal S_f^{EB}\) jest wyliczone z \(\mathcal V_f\), nie z obserwowanej masy.
2. Standardowe sprzężenia Yukawy pojawiają się wyłącznie jako efektywne wartości po projekcji niskoenergetycznej.
3. Anulowanie anomalii pozostaje dokładne na ułamkach wymiernych.
4. Ta sama funkcja \(\mathcal S^{EB}\) działa dla leptonów i kwarków, ewentualnie z jawnie wyprowadzonymi sektorami reprezentacji.
5. Dane obserwacyjne występują dopiero w tabeli walidacyjnej.

## 7. Wynik kontroli anomalii

Skrypt `sm_mass_vectorization_check.py` zwraca:

```text
kappa = 0.009193150006360484
SU3^2_U1 0
SU2^2_U1 0
grav^2_U1 0
U1^3 0
PASS: exact anomaly cancellation on rational hypercharge assignments.
```

## 8. Status końcowy

Mamy teraz zamknięty szkielet cechowania oraz schemat wektoryzacji sektora mas. Nie mamy jeszcze kanonicznej funkcji \(\mathcal S^{EB}\), która z tych wektorów przewiduje widmo mas. To jest następny właściwy obiekt do wyprowadzenia.
