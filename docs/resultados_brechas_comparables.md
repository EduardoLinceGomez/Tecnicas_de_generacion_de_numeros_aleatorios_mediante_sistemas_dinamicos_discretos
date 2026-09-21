# Resultados reproducibles de brechas comparables

## Estado y trazabilidad

- **Estado:** IMPLEMENTADO y validado en el repositorio científico.
- **Repositorio:**
  `EduardoLinceGomez/Tecnicas_de_generacion_de_numeros_aleatorios_mediante_sistemas_dinamicos_discretos`.
- **Rama base:** `reestructuracion/repositorio`.
- **Commit base actualizado:**
  `363bef1a8fc694e40ccab8e0625c166775f14c9c`.
- **Rama de implementación:** `feat/brechas-comparables`.
- **Commit científico principal:**
  `3099b0630fb3eca42a18f7c5eaabe3874c4857b6`.
- **Fecha de ejecución:** 2026-09-21.
- **Repositorio de la tesis:** no modificado en esta entrega.

Este documento es la fuente de handoff para actualizar posteriormente
`capitulos/resultados.tex`. Las tablas se extrajeron de los CSV reproducibles
versionados; los decimales se muestran con 12 cifras significativas y los CSV
conservan la representación completa.

## Motivación y metodología final

El experimento histórico asignaba un intervalo de brechas distinto a cada
generador. Además de cambiar la región de observación, dos intervalos tenían
longitud 0.3 y dos longitud 0.2. Por ello, los diagnósticos no compartían una
misma probabilidad de éxito ni una misma referencia geométrica.

La corrección aplica a todas las muestras los mismos intervalos abiertos:

\[
I_1=(0.1,0.3),\qquad I_2=(0.4,0.6),\qquad I_3=(0.7,0.9).
\]

Los tres tienen longitud `0.2`. Bajo Uniforme(0,1), `p=0.2` y, con la
convención preservada `W=G+1`, la referencia común es

\[
\mathbb P(W=w)=0.2(0.8)^{w-1},\qquad w=1,2,\ldots.
\]

No se modificaron `tiempos_espera_brechas` ni el cálculo matemático de
`resumen_brechas`. Para la serialización del protocolo común se normaliza el
valor público a la constante validada `0.2`, evitando representar
`0.3-0.1` como `0.19999999999999998`.

## Entorno utilizado

- macOS 26.6.2, build 25G83, arm64;
- Python 3.14.5;
- NumPy 2.4.6;
- SciPy 1.18.0;
- Matplotlib 3.10.9;
- Pillow 12.2.0;
- backend gráfico `Agg`.

El proyecto se instaló localmente con `python3 -m pip install -e .` para
ejecutar los comandos de prueba desde la raíz del worktree.

## Comandos exactos de regeneración

```bash
python3 scripts/regenerar_reordenamiento.py \
  --output-dir outputs/reordenamiento \
  --reference-dir graficas_auxiliares/reordenamiento

python3 scripts/regenerar_comparacion_generadores.py \
  --output-dir outputs/comparacion_generadores \
  --reference-dir graficas_auxiliares/comparacion_generadores
```

Las cuatro figuras PG aprobadas visualmente se copiaron dentro del mismo
repositorio científico a `figuras_tesis/cientificas/reordenamiento/`. No se
copiaron al repositorio de la tesis.

## Comandos exactos de validación

```bash
python3 -m unittest -v
python3 -m unittest discover -s tests -p 'test_*.py' -v

VERIFICAR_PNG_REORDENAMIENTO=1 \
VERIFICAR_PNG_COMPARACION=1 \
MPLBACKEND=Agg \
python3 -m unittest -v \
  tests.test_visualizacion_reordenamiento \
  tests.test_visualizacion_comparacion_generadores

python3 scripts/verificar_figuras_tesis.py
git diff --check
```

## Invariantes confirmados

La comparación exacta de los baselines nuevos con el estado base
`363bef1a8fc694e40ccab8e0625c166775f14c9c` confirmó:

- los fingerprints de las cuatro muestras son idénticos;
- los fingerprints de las muestras reordenadas son idénticos;
- las dos permutaciones, sus fingerprints, semillas, estados iniciales y
  primeros/últimos índices son idénticos;
- las métricas ACF originales y reordenadas son idénticas;
- CDF, momentos, FGM, función característica, ACF y fingerprints del benchmark
  de cinco generadores son idénticos;
- `n=1000`, los lags 1 a 20 y la uniformización logística no cambiaron;
- original y reordenada tienen el mismo número de tiempos completos para cada
  muestra e intervalo;
- no queda una asignación activa generador-a-intervalo;
- existen exactamente 24 resúmenes de reordenamiento y 15 resúmenes de
  comparación original;
- no se introdujo promedio, puntuación ni ranking global.

Los PNG versionados de ACF y `permutacion_indices.png` tampoco cambiaron.

## Resultados de reordenamiento: 12 casos, 24 resúmenes

`O` significa original y `R` reordenada. `Racha` es la longitud de la racha
final incompleta.

| Muestra | Intervalo | Brechas O | Racha O | Media W O | Máx W O | Dmax O | EAM O | Brechas R | Racha R | Media W R | Máx W R | Dmax R | EAM R |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Logístico uniformizado | I1 | 196 | 5 | 5.07653061224 | 23 | 0.120204081633 | 0.021969571368 | 196 | 3 | 5.08673469388 | 26 | 0.034693877551 | 0.0119162757537 |
| Logístico uniformizado | I2 | 196 | 1 | 5.09693877551 | 15 | 0.36 | 0.105856357919 | 196 | 1 | 5.09693877551 | 24 | 0.0465135542857 | 0.0145811978691 |
| Logístico uniformizado | I3 | 197 | 0 | 5.07614213198 | 20 | 0.2 | 0.0272659915277 | 197 | 12 | 5.0152284264 | 32 | 0.033939622335 | 0.00794152254574 |
| Mapeo tienda | I1 | 209 | 4 | 4.76555023923 | 26 | 0.115980861244 | 0.0185667581693 | 209 | 0 | 4.78468899522 | 21 | 0.044019138756 | 0.0145484336699 |
| Mapeo tienda | I2 | 211 | 1 | 4.7345971564 | 12 | 0.350521327014 | 0.128517204437 | 211 | 12 | 4.68246445498 | 25 | 0.0393951848341 | 0.0147250463498 |
| Mapeo tienda | I3 | 211 | 0 | 4.73933649289 | 29 | 0.195260663507 | 0.0235673336349 | 211 | 3 | 4.72511848341 | 22 | 0.0297624556324 | 0.0138070614392 |
| R30 columnas | I1 | 189 | 2 | 5.28042328042 | 20 | 0.0795767195767 | 0.0230800207735 | 189 | 8 | 5.24867724868 | 30 | 0.0435555555556 | 0.00970981988696 |
| R30 columnas | I2 | 199 | 10 | 4.97487437186 | 20 | 0.0562814070352 | 0.0178800840868 | 199 | 1 | 5.02010050251 | 25 | 0.0446633165829 | 0.0163170967768 |
| R30 columnas | I3 | 201 | 4 | 4.9552238806 | 21 | 0.106268656716 | 0.0280724588681 | 201 | 0 | 4.97512437811 | 27 | 0.0393631840796 | 0.00877564483817 |
| R30 filas | I1 | 221 | 3 | 4.51131221719 | 15 | 0.114027149321 | 0.0510931568849 | 221 | 0 | 4.52488687783 | 27 | 0.0603939330317 | 0.0184178229449 |
| R30 filas | I2 | 182 | 2 | 5.48351648352 | 26 | 0.128571428571 | 0.0202124395053 | 182 | 11 | 5.43406593407 | 26 | 0.0907692307692 | 0.0219275609925 |
| R30 filas | I3 | 206 | 1 | 4.84951456311 | 22 | 0.102912621359 | 0.0211032553295 | 206 | 7 | 4.82038834951 | 25 | 0.0848155339806 | 0.0177729841826 |

## Comparación de muestras originales: 15 resúmenes

| Generador | Intervalo | Brechas | Racha final incompleta | Media W | Máx W | Dmax | EAM |
|---|---|---:|---:|---:|---:|---:|---:|
| Logístico uniformizado | I1 | 196 | 5 | 5.07653061224 | 23 | 0.120204081633 | 0.021969571368 |
| Logístico uniformizado | I2 | 196 | 1 | 5.09693877551 | 15 | 0.36 | 0.105856357919 |
| Logístico uniformizado | I3 | 197 | 0 | 5.07614213198 | 20 | 0.2 | 0.0272659915277 |
| Mapeo tienda | I1 | 209 | 4 | 4.76555023923 | 26 | 0.115980861244 | 0.0185667581693 |
| Mapeo tienda | I2 | 211 | 1 | 4.7345971564 | 12 | 0.350521327014 | 0.128517204437 |
| Mapeo tienda | I3 | 211 | 0 | 4.73933649289 | 29 | 0.195260663507 | 0.0235673336349 |
| R30 columnas | I1 | 189 | 2 | 5.28042328042 | 20 | 0.0795767195767 | 0.0230800207735 |
| R30 columnas | I2 | 199 | 10 | 4.97487437186 | 20 | 0.0562814070352 | 0.0178800840868 |
| R30 columnas | I3 | 201 | 4 | 4.9552238806 | 21 | 0.106268656716 | 0.0280724588681 |
| R30 filas | I1 | 221 | 3 | 4.51131221719 | 15 | 0.114027149321 | 0.0510931568849 |
| R30 filas | I2 | 182 | 2 | 5.48351648352 | 26 | 0.128571428571 | 0.0202124395053 |
| R30 filas | I3 | 206 | 1 | 4.84951456311 | 22 | 0.102912621359 | 0.0211032553295 |
| Park--Miller MINSTD | I1 | 202 | 0 | 4.9504950495 | 43 | 0.0565544554455 | 0.00739207571217 |
| Park--Miller MINSTD | I2 | 178 | 18 | 5.51685393258 | 24 | 0.0768143820225 | 0.0240448763455 |
| Park--Miller MINSTD | I3 | 179 | 3 | 5.56983240223 | 35 | 0.0764335195531 | 0.0171871565716 |

## Figuras generadas y SHA-256

Las figuras PG son composiciones verticales de tres paneles. Las copias
auxiliares y canónicas correspondientes son byte a byte idénticas.

| Archivo de referencia | SHA-256 |
|---|---|
| `graficas_auxiliares/reordenamiento/brechas_antes_despues_logistico.png` | `eae19f4f9db85e2988f79414cdb88048cd030eeb1f2b7df2503c411b0083c3da` |
| `graficas_auxiliares/reordenamiento/brechas_antes_despues_tienda.png` | `a390cf9f1cb936a1caf9d53c03da37985b4f7a1e389783844e72ab99c050aef7` |
| `graficas_auxiliares/reordenamiento/brechas_antes_despues_r30_columnas.png` | `907bfeb31c734da532ad660c77dd3de28a054d34f275f45da83bfbdfca0d0080` |
| `graficas_auxiliares/reordenamiento/brechas_antes_despues_r30_filas.png` | `208d239d96803c655c9c3a9ff6caf5c028ece0c1d7a6ef06c9b4d92fbe592d78` |
| `figuras_tesis/cientificas/reordenamiento/Log_PG.png` | `eae19f4f9db85e2988f79414cdb88048cd030eeb1f2b7df2503c411b0083c3da` |
| `figuras_tesis/cientificas/reordenamiento/Tent_PG.png` | `a390cf9f1cb936a1caf9d53c03da37985b4f7a1e389783844e72ab99c050aef7` |
| `figuras_tesis/cientificas/reordenamiento/R30_col_PG.png` | `907bfeb31c734da532ad660c77dd3de28a054d34f275f45da83bfbdfca0d0080` |
| `figuras_tesis/cientificas/reordenamiento/R30_fila_PG.png` | `208d239d96803c655c9c3a9ff6caf5c028ece0c1d7a6ef06c9b4d92fbe592d78` |
| `graficas_auxiliares/comparacion_generadores/brechas_comparacion_i1.png` | `2d3a118e1d5114c35cba6490f39b239bff2bfafd61d684ab437070acc09fcb18` |
| `graficas_auxiliares/comparacion_generadores/brechas_comparacion_i2.png` | `da83fb016299ea2e701479e2fd98feeea9a17373d5f1eefad6b9f2d5321abbd6` |
| `graficas_auxiliares/comparacion_generadores/brechas_comparacion_i3.png` | `a559c3e6d90305bfe2dbf68b8cdd3d99cf2582a56839fa45e8658ccc7de1d893` |

La inspección visual se realizó a resolución original antes de actualizar el
manifest. La primera composición vertical tenía leyendas sobredimensionadas;
se corrigió a una sola leyenda global y se revisaron de nuevo las siete
figuras. No queda una revisión visual pendiente dentro del repositorio
científico.

## CSV, baselines y archivos actualizados

CSV reproducibles:

- `graficas_auxiliares/reordenamiento/resumen_reordenamiento.csv`:
  4 filas, sólo cantidades independientes del intervalo;
- `graficas_auxiliares/reordenamiento/resumen_brechas_reordenamiento.csv`:
  12 filas;
- `graficas_auxiliares/comparacion_generadores/resumen_comparacion.csv`:
  5 filas y contenido científico previo sin cambios;
- `graficas_auxiliares/comparacion_generadores/resumen_brechas_comparacion.csv`:
  15 filas.

Baselines actualizados desde la ejecución real:

- `tests/data/reordenamiento_baseline.json`;
- `tests/data/comparacion_generadores_baseline.json`.

Archivos principales de implementación:

- `src/tesis_generacion/experimentos/parametros.py`;
- `src/tesis_generacion/experimentos/reordenamiento.py`;
- `src/tesis_generacion/experimentos/comparacion_generadores.py`;
- `src/tesis_generacion/visualizacion/reordenamiento.py`;
- `src/tesis_generacion/visualizacion/comparacion_generadores.py`;
- pruebas de experimento, visualización y CLI de ambos bloques;
- `figuras_tesis/manifest_figuras.csv`, FIG-054 a FIG-057.

## Pruebas ejecutadas y resultado

- `python3 -m unittest -v`: **8/8 OK**.
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`:
  **129 pruebas descubiertas: 123 OK y 6 verificaciones PNG opcionales
  omitidas por defecto**.
- verificación PNG estricta de reordenamiento y comparación: **6/6 OK**.
- `python3 scripts/verificar_figuras_tesis.py`: **65 entradas, 0 errores**.
- `git diff --check`: sin errores.

## Handoff a la tesis

El repositorio `EduardoLinceGomez/tesis-generacion-numeros` todavía no debe
modificarse hasta revisar y aprobar este PR. Después de la aprobación, en
`capitulos/resultados.tex` se deben actualizar exactamente estos elementos:

1. **Diseño de los experimentos:** sustituir la asignación histórica por
   `I1`, `I2`, `I3`, intervalos abiertos, longitud 0.2 y `p=0.2`.
2. **Regla 30:** reemplazar las cifras de columnas y filas por los tres casos
   de las tablas de este documento.
3. **Mapeo tienda:** reemplazar el caso único histórico por I1, I2 e I3.
4. **Mapeo logístico:** reemplazar el caso único histórico por I1, I2 e I3.
5. **Tabla de reordenamiento:** usar las 12 filas muestra por intervalo; no
   promediar los intervalos.
6. **Comparación final de generadores:** incorporar las 15 filas originales,
   incluido MINSTD, y retirar la justificación basada en intervalos distintos.
7. **Pies de figuras:** describir los tres paneles y la referencia geométrica
   común `p=0.2` para `fig:PG_log`, `fig:PG_tent` y las figuras R30.
8. **Recursos gráficos:** copiar las cuatro figuras canónicas aprobadas desde
   este repositorio y verificar sus SHA-256 antes de compilar la tesis.

## Cautelas científicas y desviaciones

- Una buena concordancia con la geométrica en estos intervalos no demuestra
  independencia; es un diagnóstico local de tiempos de espera.
- Los tres intervalos exploran regiones diferentes con la misma probabilidad,
  pero no agotan todas las formas de dependencia serial.
- No debe seleccionarse a posteriori el intervalo más favorable ni resumir los
  tres mediante una puntuación global.
- Las figuras PG usan tres paneles verticales, en lugar de horizontales, por
  legibilidad al tamaño de tesis. Esta es la única desviación de presentación
  respecto de la preferencia inicial; no hubo desviaciones metodológicas.
- La terminología pública es **racha final incompleta**.
- La prosa, tablas, pies y archivos gráficos del repositorio de la tesis siguen
  pendientes y no se modificaron en esta entrega.
