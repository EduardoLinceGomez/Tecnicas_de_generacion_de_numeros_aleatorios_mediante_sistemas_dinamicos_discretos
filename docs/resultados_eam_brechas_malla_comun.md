# AUT-093: EAM de brechas sobre una malla común

## Estado y trazabilidad

- **Repositorio:** `EduardoLinceGomez/Tecnicas_de_generacion_de_numeros_aleatorios_mediante_sistemas_dinamicos_discretos`.
- **Rama:** `feat/eam-brechas-malla-comun`.
- **Rama base:** `reestructuracion/repositorio`.
- **SHA base aprobado:** `1fe481ddb577e8d6d1e145ec3569bb8428e8ca1c`.
- **SHA final científico (implementación, pruebas, baselines y CSV):**
  `f6ef83a7a1ea66e981355c7ae5f814200088ff3d`.
- **HEAD final del PR:** posterior por el commit exclusivamente documental; se
  informa en el PR y en el cierre de AUT-093 para evitar que este archivo se
  autorreferencie a su propio commit.
- **Fecha:** 2026-09-22.
- **Repositorio de la tesis:** consultado sólo para identificar el handoff; no
  fue modificado.

Este documento supersede únicamente los EAM de brechas calculados con soportes
propios en `resultados_brechas_comparables.md`. AUT-065 permanece como registro
histórico de la homogeneización de intervalos.

## Entorno

- macOS 26.6.2, arm64;
- Python 3.14.5;
- NumPy 2.4.6;
- SciPy 1.18.0;
- Matplotlib 3.10.9;
- Pillow 12.2.0;
- backend gráfico de validación: `Agg`.

El paquete editable se reinstaló desde este checkout porque el entorno apuntaba
inicialmente a un worktree anterior.

## Metodología y arquitectura

Para cada intervalo \(I_j\), AUT-093 define

\[
W_j^*=\max_S W_{\max}(S,I_j),
\]

con nueve participantes: logístico, tienda, R30 columnas y R30 filas, cada uno
en versión original y reordenada, más Park--Miller MINSTD original. MINSTD no
se reordena. Los máximos se derivan de las muestras, no son constantes del
algoritmo:

| Intervalo | \(W_j^*\) | Participante que alcanza el máximo |
|---|---:|---|
| \(I_1=(0.1,0.3)\) | 43 | Park--Miller MINSTD original |
| \(I_2=(0.4,0.6)\) | 26 | R30 filas original y reordenada |
| \(I_3=(0.7,0.9)\) | 35 | Park--Miller MINSTD original |

La fuente única es `experimentos/soportes_brechas.py`. Los bloques de
reordenamiento y comparación consumen el mismo diccionario. El resumen de bajo
nivel conserva el comportamiento histórico si no recibe soporte externo y,
cuando lo recibe, exige que sea entero y al menos el máximo observado. Para
\(w>W_{\max}\), `searchsorted(..., side="right")` produce
\(\widehat F(w)=1\), de modo que

\[
\operatorname{EAM}_{F,j}(S)=\frac{1}{W_j^*}
\sum_{w=1}^{W_j^*}\left|\widehat F_{S,j}(w)-(1-0.8^w)\right|.
\]

No se cambió `tiempos_espera_brechas` ni la convención \(W=G+1\).

## Tabla A — original frente a reordenada

`Δ O` y `Δ R` son EAM nuevo menos EAM anterior para cada estado. Las columnas
de \(D_{\max}\) muestran `anterior / nuevo`; la igualdad exacta es deliberada.

| Muestra | I | Wmax O | Wmax R | W* | Dmax O ant./nuevo | Dmax R ant./nuevo | EAM O ant. | EAM O nuevo | Δ O | EAM R ant. | EAM R nuevo | Δ R | O→R nuevo | EAM nuevo (4 dec.) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Logístico transformado | I1 | 23 | 26 | 43 | 0.12020408163265295 / 0.12020408163265295 | 0.03469387755102046 / 0.03469387755102046 | 0.02196957136796534 | 0.012293947627535213 | -0.009675623740430126 | 0.011916275753749676 | 0.0074800046953511865 | -0.0044362710583984895 | disminuye | O 0.0123; R 0.0075 |
| Logístico transformado | I2 | 15 | 24 | 26 | 0.3599999999999999 / 0.3599999999999999 | 0.04651355428571424 / 0.04651355428571424 | 0.10585635791916863 | 0.06601898457487351 | -0.039837373344295116 | 0.014581197869094509 | 0.013721113715138481 | -0.0008600841539560273 | disminuye | O 0.0660; R 0.0137 |
| Logístico transformado | I3 | 20 | 32 | 35 | 0.20000000000000007 / 0.20000000000000007 | 0.033939622335025454 / 0.033939622335025454 | 0.027265991527720322 | 0.01685183137058252 | -0.010414160157137801 | 0.007941522545735193 | 0.0073050072913087025 | -0.0006365152544264901 | disminuye | O 0.0169; R 0.0073 |
| Tienda | I1 | 26 | 21 | 43 | 0.11598086124401902 / 0.11598086124401902 | 0.0440191387559809 / 0.0440191387559809 | 0.018566758169272276 | 0.011501226621016014 | -0.0070655315482562615 | 0.014548433669899616 | 0.007956706263297074 | -0.006591727406602542 | disminuye | O 0.0115; R 0.0080 |
| Tienda | I2 | 12 | 25 | 26 | 0.3505213270142179 / 0.3505213270142179 | 0.03939518483412341 / 0.03939518483412341 | 0.12851720443713113 | 0.06942288853820876 | -0.059094315898922375 | 0.014725046349762206 | 0.014274941280503526 | -0.00045010506925867964 | disminuye | O 0.0694; R 0.0143 |
| Tienda | I3 | 29 | 22 | 35 | 0.19526066350710908 / 0.19526066350710908 | 0.029762455632366902 / 0.029762455632366902 | 0.023567333634868397 | 0.01965770808112338 | -0.0039096255537450185 | 0.013807061439189002 | 0.009475644268908606 | -0.004331417170280396 | disminuye | O 0.0197; R 0.0095 |
| R30 columnas | I1 | 20 | 30 | 43 | 0.07957671957671947 / 0.07957671957671947 | 0.04355555555555546 / 0.04355555555555546 | 0.023080020773517902 | 0.011801047668862679 | -0.011278973104655223 | 0.009709819886960186 | 0.006883119322614192 | -0.0028267005643459932 | disminuye | O 0.0118; R 0.0069 |
| R30 columnas | I2 | 20 | 25 | 26 | 0.05628140703517592 / 0.05628140703517592 | 0.04466331658291467 / 0.04466331658291467 | 0.01788008408684903 | 0.015062664758658008 | -0.002817419328191021 | 0.016317096776771272 | 0.015805758998781474 | -0.0005113377779897982 | **aumenta** | O 0.0151; R 0.0158 |
| R30 columnas | I3 | 21 | 27 | 35 | 0.106268656716418 / 0.106268656716418 | 0.03936318407960193 / 0.03936318407960193 | 0.028072458868128095 | 0.017851215188851913 | -0.010221243679276182 | 0.00877564483817035 | 0.006999749269120695 | -0.001775895569049655 | disminuye | O 0.0179; R 0.0070 |
| R30 filas | I1 | 15 | 27 | 43 | 0.11402714932126692 / 0.11402714932126692 | 0.060393933031674285 / 0.060393933031674285 | 0.05109315688490879 | 0.021089828272916823 | -0.03000332861199197 | 0.018417822944940345 | 0.011783265120389989 | -0.006634557824550356 | disminuye | O 0.0211; R 0.0118 |
| R30 filas | I2 | 26 | 26 | 26 | 0.12857142857142853 / 0.12857142857142853 | 0.09076923076923066 / 0.09076923076923066 | 0.02021243950533586 | 0.02021243950533586 | 0.0 | 0.021927560992464307 | 0.021927560992464307 | 0.0 | **aumenta** | O 0.0202; R 0.0219 |
| R30 filas | I3 | 22 | 25 | 35 | 0.10291262135922337 / 0.10291262135922337 | 0.08481553398058239 / 0.08481553398058239 | 0.021103255329502454 | 0.014061823285677061 | -0.007041432043825393 | 0.017772984182579946 | 0.013080388129753982 | -0.004692596052825964 | disminuye | O 0.0141; R 0.0131 |

## Tabla B — comparación de generadores originales

| Generador | I | Wmax | W* | Dmax ant. | Dmax nuevo | EAM ant. | EAM nuevo | Δ | EAM nuevo (4 dec.) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Logístico transformado | I1 | 23 | 43 | 0.12020408163265295 | 0.12020408163265295 | 0.02196957136796534 | 0.012293947627535213 | -0.009675623740430126 | 0.0123 |
| Logístico transformado | I2 | 15 | 26 | 0.3599999999999999 | 0.3599999999999999 | 0.10585635791916863 | 0.06601898457487351 | -0.039837373344295116 | 0.0660 |
| Logístico transformado | I3 | 20 | 35 | 0.20000000000000007 | 0.20000000000000007 | 0.027265991527720322 | 0.01685183137058252 | -0.010414160157137801 | 0.0169 |
| Tienda | I1 | 26 | 43 | 0.11598086124401902 | 0.11598086124401902 | 0.018566758169272276 | 0.011501226621016014 | -0.0070655315482562615 | 0.0115 |
| Tienda | I2 | 12 | 26 | 0.3505213270142179 | 0.3505213270142179 | 0.12851720443713113 | 0.06942288853820876 | -0.059094315898922375 | 0.0694 |
| Tienda | I3 | 29 | 35 | 0.19526066350710908 | 0.19526066350710908 | 0.023567333634868397 | 0.01965770808112338 | -0.0039096255537450185 | 0.0197 |
| R30 columnas | I1 | 20 | 43 | 0.07957671957671947 | 0.07957671957671947 | 0.023080020773517902 | 0.011801047668862679 | -0.011278973104655223 | 0.0118 |
| R30 columnas | I2 | 20 | 26 | 0.05628140703517592 | 0.05628140703517592 | 0.01788008408684903 | 0.015062664758658008 | -0.002817419328191021 | 0.0151 |
| R30 columnas | I3 | 21 | 35 | 0.106268656716418 | 0.106268656716418 | 0.028072458868128095 | 0.017851215188851913 | -0.010221243679276182 | 0.0179 |
| R30 filas | I1 | 15 | 43 | 0.11402714932126692 | 0.11402714932126692 | 0.05109315688490879 | 0.021089828272916823 | -0.03000332861199197 | 0.0211 |
| R30 filas | I2 | 26 | 26 | 0.12857142857142853 | 0.12857142857142853 | 0.02021243950533586 | 0.02021243950533586 | 0.0 | 0.0202 |
| R30 filas | I3 | 22 | 35 | 0.10291262135922337 | 0.10291262135922337 | 0.021103255329502454 | 0.014061823285677061 | -0.007041432043825393 | 0.0141 |
| Park--Miller MINSTD | I1 | 43 | 43 | 0.056554455445544716 | 0.056554455445544716 | 0.0073920757121687585 | 0.0073920757121687585 | 0.0 | 0.0074 |
| Park--Miller MINSTD | I2 | 24 | 26 | 0.07681438202247182 | 0.07681438202247182 | 0.024044876345457402 | 0.022456816924088845 | -0.0015880594213685574 | 0.0225 |
| Park--Miller MINSTD | I3 | 35 | 35 | 0.07643351955307276 | 0.07643351955307276 | 0.017187156571563708 | 0.017187156571563708 | 0.0 | 0.0172 |

## Impacto cuantitativo

1. \(W_1^*=43\), \(W_2^*=26\) y \(W_3^*=35\).
2. \(D_{\max}\) disminuye con el reordenamiento en **12/12** casos.
3. El EAM disminuye con el reordenamiento en **10/12** casos.
4. El EAM aumenta en **2/12** casos: **R30 columnas–I2**
   (`0.015062664758658008 → 0.015805758998781474`) y **R30 filas–I2**
   (`0.02021243950533586 → 0.021927560992464307`).
5. Ningún \(D_{\max}\) cambió entre la metodología anterior y AUT-093.
6. No cambiaron muestras, fingerprints, semillas, estados iniciales, tiempos de
   espera, brechas completas, rachas finales, medias, máximos observados,
   permutaciones, ACF, CDF marginal, momentos, FGM, función característica ni
   los datos de MINSTD.
7. Ningún PNG versionado cambió: se compararon los hashes SHA-256 de los 77
   archivos antes y después y el diff fue vacío.

## Handoff exacto a la tesis

No se modificó la tesis. En una corrección posterior deben realizarse estos
reemplazos:

- En la definición metodológica, sustituir el dominio y denominador propio
  `1..W_max` del EAM por `1..W_j^*`, con los tres máximos comunes anteriores.
  \(D_{\max}\) puede declararse sobre la misma malla; sus cifras no cambian.
- En la tabla de reordenamiento y en las tablas locales, usar estos EAM
  `original / reordenada`, redondeados a cuatro decimales:

| Muestra | I1 | I2 | I3 |
|---|---|---|---|
| Logístico transformado | 0.0123 / 0.0075 | 0.0660 / 0.0137 | 0.0169 / 0.0073 |
| Tienda | 0.0115 / 0.0080 | 0.0694 / 0.0143 | 0.0197 / 0.0095 |
| R30 columnas | 0.0118 / 0.0069 | 0.0151 / 0.0158 | 0.0179 / 0.0070 |
| R30 filas | 0.0211 / 0.0118 | 0.0202 / 0.0219 | 0.0141 / 0.0131 |

- En la tabla comparativa de originales, usar:

| Muestra | I1 | I2 | I3 |
|---|---:|---:|---:|
| Logístico transformado | 0.0123 | 0.0660 | 0.0169 |
| Tienda | 0.0115 | 0.0694 | 0.0197 |
| R30 columnas | 0.0118 | 0.0151 | 0.0179 |
| R30 filas | 0.0211 | 0.0202 | 0.0141 |
| Park--Miller MINSTD | 0.0074 | 0.0225 | 0.0172 |

- Cambiar “once de los doce” por **“diez de los doce”** y declarar las dos
  excepciones de I2.
- Corregir la lectura de R30 columnas: el EAM disminuye en I1 e I3, pero aumenta
  en I2. La excepción de R30 filas–I2 permanece.
- En tienda, después del reordenamiento I3 sigue minimizando \(D_{\max}\), pero
  **I1**, no I3, minimiza el EAM bajo AUT-093.
- Revisar resumen y conclusiones para que no afirmen una mejora uniforme del EAM.
- No sustituir figuras: sus PMF no dependen del EAM y los 77 PNG permanecen
  byte a byte idénticos.

## Diff científico e invariantes

Antes de actualizar baselines se conservaron fuera del repositorio los dos
JSON, los dos CSV de brechas y un manifiesto SHA-256 de los 77 PNG. La
comparación campo por campo admitió sólo `mae_cdf` y el nuevo
`maximo_soporte_evaluacion`. En particular:

- los parámetros previos son idénticos y sólo se añadió el mapa de soportes;
- el benchmark MINSTD completo es idéntico;
- en reordenamiento son idénticos fingerprints, ACF, permutaciones y los cinco
  campos previos al EAM de cada resumen, incluido \(D_{\max}\);
- en comparación son idénticos `n`, fingerprint, CDF, momentos, FGM, función
  característica, ACF y todos los campos de brechas salvo EAM;
- los casos cuyo máximo observado ya era \(W_j^*\) conservan también el EAM.

## PNG y reproducibilidad

Las funciones gráficas de brechas consumen los tiempos observados y sus PMF,
no `mae_cdf`. Por eso AUT-093 no actualiza referencias gráficas, manifiestos ni
PNG. Las regeneraciones exigidas se ejecutan sólo bajo `outputs/`, que está
ignorado; no se copian a `graficas_auxiliares`.

Comandos principales de reproducción y validación:

```bash
python3 -m pip install -e .
python3 -m unittest -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/regenerar_reordenamiento.py \
  --output-dir outputs/reordenamiento
python3 scripts/regenerar_comparacion_generadores.py \
  --output-dir outputs/comparacion_generadores
python3 scripts/verificar_figuras_tesis.py
VERIFICAR_PNG_REORDENAMIENTO=1 \
VERIFICAR_PNG_COMPARACION=1 \
MPLBACKEND=Agg \
python3 -m unittest -v \
  tests.test_visualizacion_reordenamiento \
  tests.test_visualizacion_comparacion_generadores
diff -u /tmp/aut093-before.hWItAn/png-sha256.txt \
  <(git ls-files -z '*.png' | xargs -0 shasum -a 256)
git diff --check
```

Resultados obtenidos:

- `python3 -m unittest -v`: **8 aprobadas, 0 omitidas, 0 fallidas**;
- descubrimiento completo: **129 aprobadas, 6 omitidas, 0 fallidas**
  (135 pruebas en total);
- verificación PNG opcional de los dos bloques afectados: **6 aprobadas,
  0 omitidas, 0 fallidas**;
- ambas regeneraciones reproducibles: código de salida cero;
- manifiesto de figuras: **65 entradas, 0 errores**;
- `git diff --check`: sin errores.

## Archivos de AUT-093

Implementación:

- `src/tesis_generacion/estadistica/dependencia_serial.py`;
- `src/tesis_generacion/experimentos/__init__.py`;
- `src/tesis_generacion/experimentos/parametros.py`;
- `src/tesis_generacion/experimentos/soportes_brechas.py`;
- `src/tesis_generacion/experimentos/reordenamiento.py`;
- `src/tesis_generacion/experimentos/comparacion_generadores.py`;
- `src/tesis_generacion/visualizacion/reordenamiento.py`;
- `src/tesis_generacion/visualizacion/comparacion_generadores.py`.

Pruebas y baselines:

- `tests/test_estadistica_dependencia_serial.py`;
- `tests/test_soportes_brechas.py`;
- `tests/test_experimentos_reordenamiento.py`;
- `tests/test_visualizacion_reordenamiento.py`;
- `tests/test_visualizacion_comparacion_generadores.py`;
- `tests/data/reordenamiento_baseline.json`;
- `tests/data/comparacion_generadores_baseline.json`.

Salidas numéricas:

- `graficas_auxiliares/reordenamiento/resumen_brechas_reordenamiento.csv`;
- `graficas_auxiliares/comparacion_generadores/resumen_brechas_comparacion.csv`.

Documentación:

- `docs/metodologia_brechas_comparables.md`;
- `docs/resultados_brechas_comparables.md`;
- `docs/resultados_eam_brechas_malla_comun.md`.
